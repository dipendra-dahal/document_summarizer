# Document Summarizer

## Overview

Document Summarizer is a full-stack web application that allows users to upload documents and generate AI-powered summaries.

The project uses:
- **Frontend:** React + TypeScript + Vite
- **Backend:** FastAPI (Python)
- **AI Model:** Groq API using `llama-3.1-8b-instant`
- **Supported Files:** PDF, TXT, MD

Users can upload a file, choose summary length, and define a focus area (for example: key points, technical summary, important highlights).

---

## Features

- Upload `.pdf`, `.txt`, and `.md` files
- Extract text from uploaded documents
- AI-generated summaries using Groq LLM
- Select summary length:
  - Short
  - Medium
  - Long
- Custom focus input for targeted summaries
- Retry logic for API failures
- File validation and error handling
- FastAPI backend with CORS support

---

## Project Structure

```text
document_summarizer/
│
├── backend/
│   ├── main.py
│   ├── .env
│   └── .venv/
│
├── frontend/
│   └── vite-project/
│       ├── src/
│       ├── public/
│       ├── package.json
│       └── vite.config.ts
│
└── README.md
```

---

## Backend Setup (FastAPI)

### 1. Navigate to backend

```bash
cd backend
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
```
### 3. Activate Virutal environment
Windows

```bash
.venv\scripts\activate
```

Linux/MacOS

```bash
source .venv/bin/activate
```

### 4. Install dependencies



```bash
pip install fastapi uvicon python-multipart python-dotenv pymupdf groq
```
### 5. Create .env file

GROQ_API_KEY=your_key_here

### 6. Run backend Server
```bash
uvicon main:app --reload
```
backend runs at : 
```
http://localhost:8000
```
---
## Frontend Setup (React + Vite)
### 1. Navigate to frontend

```bash
cd frontend/vite-project
```

### 2. Install dependencies

```bash
npm install
```
### 3. Start development server
Windows

```bash
npm run dev
```
frontend run at
```bash
http://localhost:5173
```
---
## API Endpoint

### POST /summarize
Uploads a document and returns an AI-generated summary.

Form Data
Field	> Type  > Required	> Description  
file	>File   >	Yes	      >PDF, TXT, or MD file  
length>	String>	Yes	      > short / medium / long  
focus >	String>	No	      >Summary focus area  
---
##Notes
*Maximum text sent to AI is limited to 12,000 characters
*Large files are automatically truncated before summarization
*If no Groq API key is provided, AI features are disabled
*Backend includes retry logic with exponential backoff for API failures
---
##Future Improvements
*Drag and drop file upload
*Summary download option
*Multiple document support
*Authentication system
*Summary history
*Export summary as PDF
*Better UI/UX improvements
---
## Limitations of the Application

1. **Limited File Format Support**  
   Currently, the application only supports `.pdf`, `.txt`, and `.md` files. Other commonly used formats like `.docx`, `.pptx`, and `.xlsx` are not supported.

2. **Text Length Restriction**  
   The backend limits the maximum text sent to the AI model to 12,000 characters. Large documents are truncated, which may cause important information to be missed in the summary.

3. **Dependency on Internet and API Availability**  
   Since the summarization relies on the Groq API, the application requires a stable internet connection and API availability. If the API is down, summarization will fail.

4. **No User Authentication**  
   The application does not currently include login or user account functionality, so users cannot save their summaries or access previous uploads.

5. **No Summary Export Feature**  
   Users can view summaries on-screen, but there is no option to download or export the summary as PDF, Word, or text files.

6. **Single Document Processing Only**  
   The system can process only one document at a time. Users cannot upload multiple files together for combined summarization.
---
