-- USERS TABLE
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    role TEXT CHECK(role IN ('admin', 'user')) NOT NULL DEFAULT 'user'
);

--Books Table
CREATE TABLE IF NOT EXISTS books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    author TEXT,
    original_text TEXT NOT NULL,
    file_type TEXT,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);



-- SUMMARIES TABLE
CREATE TABLE IF NOT EXISTS summaries (
    summary_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    summary_text TEXT NOT NULL,
    summary_length TEXT CHECK(summary_length IN ('short','medium','long')),
    summary_style TEXT CHECK(summary_style IN ('paragraphs','bullets')),
    chunk_summaries TEXT,     -- stored as JSON string
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processing_time REAL,
    FOREIGN KEY (book_id) REFERENCES books(book_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- INDEXES FOR PERFORMANCE
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_books_user_id ON books(user_id);
CREATE INDEX IF NOT EXISTS idx_summaries_book_id ON summaries(book_id);






-- Only add the new column
ALTER TABLE books
ADD COLUMN file_path TEXT;



