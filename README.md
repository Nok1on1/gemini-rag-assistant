# Disclaimer

**Mainly made because Node.js currently doesn't have enough support for Gemini with LangChain for RAG. (Need this for other Project)**

# GeminiRAG

A Retrieval-Augmented Generation (RAG) assistant using Google Gemini, FastAPI, and MongoDB Atlas.

## Features
- User authentication with JWT (access and refresh tokens)
- Secure password hashing with bcrypt
- Document ingestion and vector storage using LangChain and MongoDB Atlas Vector Search
- Retrieval-augmented question answering (RAG) with Gemini LLM
- Chat history per user
- FastAPI backend with modular routes and middleware

## Project Structure
```
main.py                  # FastAPI app entry point
requirements.txt         # Python dependencies
controllers/             # Business logic (auth, RAG, etc.)
middlewares/             # Custom FastAPI middleware (JWT, cookies)
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
- `POST /auth/signIn` — User login (sets JWT cookies)
- `POST /gemini/loadRagData` — Ingest RAG documents
- `PUT /gemini/extractRagData` — Query with RAG (requires login)
- `GET /gemini/getHistory` — Get user chat history

## Notes
- Passwords are hashed with bcrypt (compatible with JS bcrypt)
- JWT tokens are stored in HTTP-only cookies
- Only verified users can log in
- The assistant only responds in Georgian and follows strict output rules

## License
MIT
