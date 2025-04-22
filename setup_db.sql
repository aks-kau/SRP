-- Create database
CREATE DATABASE papers;

-- Connect to the database
\c papers

-- Enable pgvector extension
CREATE EXTENSION vector;

-- Create tables
CREATE TABLE papers (
    paper_id UUID PRIMARY KEY,
    title TEXT NOT NULL,
    abstract TEXT NOT NULL,
    year INT NOT NULL
);

CREATE TABLE paper_embeddings (
    paper_id UUID PRIMARY KEY REFERENCES papers(paper_id),
    embedding vector(1024)
); 