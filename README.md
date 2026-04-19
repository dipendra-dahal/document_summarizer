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

---

## Backend Setup (FastAPI)

### 1. Navigate to backend

```bash
cd backend

### 1. Navigate to backend
### 1. Navigate to backend
### 1. Navigate to backend
### 1. Navigate to backend
### 1. Navigate to backend
