# RAG Doc QnA

A Retrieval-Augmented Generation (RAG) based Document Question Answering system.
This project allows users to upload documents (PDF, Audio, Video) and ask
questions that are answered strictly based on the uploaded content.

---

## 🚀 Features

- Upload PDF documents
- Ask natural language questions on uploadedthey ask for documents
- Answers are generated using Retrieval-Augmented Generation (RAG)
- Uses vector embeddings for semantic search
- Dockerized backend
- Simple React frontend

---

## 🧠 What is RAG in this project?

This system follows the **Retrieval-Augmented Generation (RAG)** approach.

Instead of directly answering questions from a language model’s training data:
1. The uploaded document is split into chunks
2. Each chunk is converted into embeddings
3. Relevant chunks are retrieved using vector similarity search
4. These retrieved chunks are passed to the LLM
5. The LLM generates an answer grounded in the document content

This ensures factual, document-based answers.

---

## 🧱 Architecture

