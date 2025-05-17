# Disclaimer

**Mainly made because Node.js currently doesn't have enough support for Gemini with LangChain for RAG. (Needed for another project)**

# GeminiRAG

A Retrieval-Augmented Generation (RAG) assistant using Google Gemini, FastAPI, and MongoDB Atlas.

## Features
- Document ingestion and vector storage using LangChain and MongoDB Atlas Vector Search
- Retrieval-augmented question answering (RAG) with Gemini LLM
- Chat history per user
- FastAPI backend with modular routes

## Project Structure
```
main.py                  # FastAPI app entry point
README.md                # Project documentation
requirements.txt         # Python dependencies
controllers/             # Business logic (auth, RAG, etc.)
routes/                  # FastAPI route definitions
utils/                   # Utility functions (history conversion, etc.)

```

## Setup
1. **Clone the repository**
2. **Create a virtual environment**
   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```
4. **Configure environment variables**
   - Create a `.env` file in the project root with:
     ```env
     MONGO_CONNECTION_STRING=your_mongodb_connection_string
     GEMINI_API_KEY=your_gemini_api_key
     JWT_SECRET_KEY=your_jwt_secret
     ENV=development
     ```

## Running the App
```powershell
uvicorn main:app --reload
```

## API Endpoints
- `POST /gemini/loadRagData` — Ingest RAG documents
- `PUT /gemini/extractRagData` — Query with RAG (requires login)
- `GET /gemini/getHistory` — Get user chat history

## Notes
- The assistant only responds in Georgian and follows strict output rules

## .gitignore Highlights
- `.env` and `.venv/` are excluded for security and cleanliness
- `__pycache__/` and other generated files are ignored

## License
MIT
