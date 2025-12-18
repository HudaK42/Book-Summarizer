# 📚 Intelligent Book Summarization Platform

## Project Overview

The **Intelligent Book Summarization Platform** is a full‑stack web application built using **Flask (backend)** and **Streamlit (frontend)**. It enables users to upload books or documents, preprocess textual content, and manage their library efficiently with search, filtering, sorting, and pagination features. The architecture follows RESTful principles and is designed to be modular, scalable, and easy to extend in the future.

This project is suitable for academic evaluation as well as real‑world use cases involving document processing and summarization workflows.

---

## Key Features

* 🔐 Secure user registration and login (session‑based authentication)
* 📤 Upload documents (PDF, DOCX, TXT)
* 🧹 Text extraction and preprocessing pipeline
* 🔍 Search books by title or author
* 🔃 Sort books (Newest, Oldest, Alphabetical A–Z)
* 🧮 Pagination for large book collections
* 📝 Summary generation workflow (pipeline ready)
* 🗑️ Book management actions (view details, delete)

---

## Technology Stack

* **Backend:** Flask (Python)
* **Frontend:** Streamlit
* **Database:** SQLite
* **Text Processing:** langdetect, regex
* **Authentication:** Flask Sessions
* **API Style:** RESTful APIs

---

## Project Structure (Simplified)

```
project-root/
│
├── backend/
│   ├── auth_routes.py
│   ├── upload_routes.py
│   ├── book_routes.py
│   ├── text_extractor.py
│   ├── text_preprocessor.py
│   └── app.py
│
├── frontend/
│   ├── app.py
│   ├── dashboard.py
│   ├── auth.py
│   └── pages/
│       ├── upload.py
│       ├── my_books.py
│       └── summaries.py
│
├── utils/
│   ├── database.py
│   └── init_db.sql
│
├── config/
│   └── config.py
│
├── init_database.py
├── requirements.txt
├── .gitignore
├── .env 
└── README.md
```

---

## Virtual Environment Setup

### Step 1: Create a Virtual Environment

```bash
python -m venv venv
```

### Step 2: Activate the Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

---

## Install Required Dependencies

Ensure the virtual environment is activated, then run:

```bash
pip install -r requirements.txt
```

### Core Dependencies

* flask
* streamlit
* requests
* langdetect
* python-docx
* PyPDF2

---

## To generate the SECRET KEY use the following code and store in the file .env
import secrets
print(secrets.token_urlsafe(32))

## Running the Application

### Step 1: Start the Flask Backend

```bash
cd backend
python app.py
```

The backend server will run at:

```
http://127.0.0.1:5000
```

---

### Step 2: Start the Streamlit Frontend

Open a **new terminal**, activate the virtual environment again, then run:

```bash
cd frontend
streamlit run app.py
```

The frontend application will be available at:

```
http://localhost:8501
```

---

## Application Workflow

1. User logs in or registers
2. User uploads a document or pastes text
3. Text is extracted and passed through the preprocessing pipeline
4. Cleaned text is chunked and stored
5. Books can be searched, filtered, sorted, and paginated
6. Summarization pipeline can be triggered (future extension)

---




