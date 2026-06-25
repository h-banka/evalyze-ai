# EvalyzeAI
AI-Powered Multilingual Video Interview & Workforce Assessment Platform

## Overview
EvalyzeAI is an AI-driven video interview assessment platform designed for scalable workforce screening and candidate evaluation. The system conducts AI-led interview sessions, records candidate responses, transcribes speech using OpenAI Whisper, evaluates communication quality, and classifies candidates into actionable workforce categories.

The platform is designed to support multilingual and mobile-first interview experiences for blue-collar, semi-skilled, and polytechnic workforce assessment.

---

## Features

### AI-Led Interview Workflow
- Predefined AI interview questions
- Webcam-based interview recording
- Multi-question interview flow

### AI Video Analysis
- Speech-to-text transcription using OpenAI Whisper
- Automated transcript generation
- Audio extraction from video interviews

### Candidate Assessment
- Relevance scoring
- Clarity scoring
- Confidence scoring
- Authenticity scoring

### Candidate Classification
- Job Ready
- Needs Training
- Low Confidence
- Fraud Detection

### Frontend
- Clean and responsive UI
- Mobile-friendly interface
- Real-time interview flow

---

## Architecture / Workflow

1. Candidate starts interview in frontend
2. Webcam and microphone recording begins
3. Candidate answers AI-generated questions
4. Interview video is uploaded to FastAPI backend
5. Backend extracts audio using MoviePy
6. OpenAI Whisper generates transcript
7. AI evaluation logic calculates assessment scores
8. Final classification and transcript are displayed

---

## Tech Stack

### Frontend
- HTML
- JavaScript

### Backend
- FastAPI
- Python

### AI / Processing
- OpenAI Whisper
- MoviePy
- OpenCV
- Torch

### Other Tools
- Uvicorn
- FFmpeg
- Python venv

---

## Project Structure

```bash
evalyze-ai/
│
├── backend/
│   ├── app/
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── result.html
│   ├── styles.css
│   └── script.js
│
└── README.md
