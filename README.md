# RAG Doc QnA

A **Retrieval-Augmented Generation (RAG)** based Document Question Answering system that allows users to upload **PDF, Audio, and Video files** and ask contextual questions from the content.

The system extracts text from uploaded files, converts it into embeddings, retrieves relevant context using semantic search, and generates accurate answers using the **FLAN-T5 language model**.



## 🚀 Features

- 📄 Upload **PDF documents**
- 🎧 Upload **Audio files (MP3/WAV)** with automatic transcription
- 🎥 Upload **Video files (MP4)** with audio extraction + transcription
- 🔍 Semantic search using vector embeddings
- 🤖 Context-aware answers using **FLAN-T5**
- 🌐 Clean React-based frontend
- 🐳 Fully Dockerized backend
- 📦 REST APIs built with FastAPI



## 🧠 Architecture Overview

1. **File Upload**
   - PDF → Text extraction
   - Audio/Video → Transcription using Whisper
2. **Text Processing**
   - Text chunking
   - Embedding generation
3. **Retrieval**
   - Relevant chunks fetched using semantic similarity
4. **Answer Generation**
   - FLAN-T5 generates answers using retrieved context



## 🛠 Tech Stack

### Backend
- Python
- FastAPI
- Sentence-Transformers
- FLAN-T5 (HuggingFace)
- Whisper (Audio/Video Transcription)
- FAISS (Vector Search)
- Docker

### Frontend
- React (Vite)
- HTML / CSS
- Fetch API



## 📂 Project Structure

