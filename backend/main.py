from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Literal
from dotenv import load_dotenv, dotenv_values
from pathlib import Path
import logging
import os
import time
import fitz
from groq import Groq

# ------------------------
# Logging
# ------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ------------------------
# ENV LOADING (PRODUCTION SAFE)
# ------------------------
BASE_DIR = Path(__file__).resolve().parent
env_path = BASE_DIR / ".env"

env_data = dotenv_values(env_path)
print("DEBUG ENV FILE:", env_data)

load_dotenv(dotenv_path=env_path, override=True)

api_key = os.getenv("GROQ_API_KEY")

print("ENV PATH:", env_path)
print("API KEY FOUND:", bool(api_key))

# ------------------------
# Groq Client
# ------------------------
client = None

if api_key:
    try:
        client = Groq(api_key=api_key)
        print("Groq client initialized")
    except Exception as e:
        print("Groq initialization failed:", e)
        client = None
else:
    print("No API key found - AI features disabled")

# ------------------------
# FastAPI setup
# ------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------
# Constants
# ------------------------
ALLOWED_EXTENSIONS = {".pdf", ".txt", ".md"}
MAX_TEXT_LENGTH = 12000
GROQ_MODEL = "llama-3.1-8b-instant"
MAX_RETRIES = 3

# ------------------------
# Root
# ------------------------
@app.get("/")
def read_root():
    return {
        "message": "Backend working",
        "ai_enabled": client is not None
    }

# ------------------------
# Extract text
# ------------------------
async def extract_text(file: UploadFile) -> str:
    ext = os.path.splitext(file.filename or "")[1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {ext}"
        )

    content = await file.read()

    if ext == ".pdf":
        doc = fitz.open(stream=content, filetype="pdf")
        text = "\n".join(page.get_text("text") for page in doc)
        doc.close()
        return text

    return content.decode("utf-8", errors="replace")

# ------------------------
# Groq call with retry
# ------------------------
def call_groq(prompt: str) -> str:
    if not client:
        raise HTTPException(
            status_code=503,
            detail="AI service is not configured (missing API key)"
        )

    last_error = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logger.info("Groq attempt %d/%d", attempt, MAX_RETRIES)
            response = client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
            )
            return response.choices[0].message.content or ""

        except Exception as e:
            last_error = e
            logger.warning("Groq attempt %d failed: %s", attempt, e)

            if attempt < MAX_RETRIES:
                wait = 2 ** attempt  # 2s, 4s backoff
                logger.info("Retrying in %ds...", wait)
                time.sleep(wait)

    logger.error("All Groq attempts failed: %s", last_error)
    raise HTTPException(
        status_code=502,
        detail=f"AI service failed after {MAX_RETRIES} attempts: {str(last_error)}"
    )

# ------------------------
# Summarizer
# ------------------------
def summarize_text(text: str, length: str, focus: str) -> str:
    prompt = f"""
You are a professional document summarizer.

TASK:
Summarize the document below.

RULES:
- Length: {length}
- Focus: {focus}
- Use bullet points
- Do not add external information
- Be concise and structured

TEXT:
{text[:MAX_TEXT_LENGTH]}
"""
    return call_groq(prompt)

# ------------------------
# API endpoint
# ------------------------
@app.post("/summarize")
async def summarize(
    file: UploadFile = File(...),
    length: Literal["short", "medium", "long"] = Form(...),
    focus: str = Form(default="key points"),
):
    try:
        text = await extract_text(file)

        if not text.strip():
            raise HTTPException(
                status_code=400,
                detail="No readable text found in file"
            )

        truncated = len(text) > MAX_TEXT_LENGTH

        summary = summarize_text(text, length, focus)

        return {
            "summary": summary,
            "truncated": truncated,
            "ai_enabled": client is not None
        }

    except HTTPException:
        raise

    except Exception as e:
        logger.error("Unexpected error: %s", e)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )