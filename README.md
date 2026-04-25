# Movie Recommendation API

A simple and powerful Movie Recommendation System built using Python and FastAPI.  
It suggests similar movies based on user ratings using collaborative filtering.

---

## Features

- Recommend similar movies
- Search movies by keyword
- View dataset statistics
- Fast and scalable API using FastAPI
- Based on Collaborative Filtering (Cosine Similarity)

---

## Tech Stack

- Python
- FastAPI
- Pandas

---

## How It Works

This project uses Collaborative Filtering:
- It analyzes user ratings
- Finds similarity between movies
- Recommends movies with similar rating patterns

We use Cosine Similarity to compute similarity between movies.

---

## API Endpoints

### 1. Recommend Movies
GET /recommend?movie_name=Inception&limit=10

Returns a list of similar movies

---

### 2. Search Movies
GET /search?q=inception

Returns matching movie titles

---

### 3. Statistics
GET /stats

Returns dataset statistics

---

## Project Structure

.
├── main.py           # FastAPI entry point  
├── services.py       # Business logic  
├── ml_manager.py     # Model loading (Singleton)  
├── schemas.py        # Data models  
├── utils.py          # Decorators  
├── interfaces.py     # Interfaces (DIP)  
├── ui.html           # Simple UI  
├── similarity_df.pkl # Precomputed similarity matrix  

---

## Run the Project

pip install -r requirements.txt  
uvicorn main:app --reload  

Open in browser:  
http://127.0.0.1:8000/docs  

---

## Dataset

- MovieLens Dataset  
- Preprocessed into a similarity matrix  

---

## Architecture

- Layered Architecture  
- FastAPI (API Layer)  
- Service Layer (Business Logic)  
- Data Layer (Model Manager)  
- Utility Layer (Decorators)  

---

## Author

Ismail elahmar

---

## Future Improvements

- Add content-based filtering (genre, description)  
- Add user authentication  
- Deploy API online  
