from fastapi import Request
from pymongo import AsyncMongoClient, MongoClient
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain_core.documents import Document
from langchain.chains import retrieval
from dotenv import load_dotenv
from pydantic import BaseModel
from bson import ObjectId
from typing import List
import os

from langchain.chains import LLMChain
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from utils.databaseUtils import (
    convert_mongo_history_to_langchain,
    convert_objectid,
)

load_dotenv()

AsyncClient = AsyncMongoClient(os.getenv("MONGO_CONNECTION_STRING"))
Client = MongoClient(os.getenv("MONGO_CONNECTION_STRING"))

dbName = "Gragnily"

rag_collection_name = "ragFiles"
rag_collection = Client[dbName][rag_collection_name]

history_collection_name = "ghistories"
history_collection = AsyncClient[dbName][history_collection_name]

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-exp-03-07",
    google_api_key=os.getenv("GEMINI_API_KEY"),  # type: ignore
)

system_config = (
    "You are a book assistant on site Gragnily chatting to user like a friend on WhatsApp. "
    "Your name is ია and you are female. "
    "You can only speak Georgian. "
    "Your output should only be plain text. "
    "You are allowed to use any emojis. "
    "You are not allowed to swear (in Georgian too). "
    "You are not allowed to use any attachments, code blocks, markdown, documents, "
    "HTML tags, images, videos, links, audio, or files."
)


class ragData(BaseModel):
    text: str
    source: str


def LoadData(rag_data_list: List[ragData]):
    documents = [
        Document(page_content=rag_data.text, metadata={"source": rag_data.source})
        for rag_data in rag_data_list
    ]

    MongoDBAtlasVectorSearch.from_documents(
        documents, embeddings, collection=rag_collection
    )

    return "Data loaded successfully"


class UserInput(BaseModel):
    text: str


async def query_data(Input: UserInput, request: Request):

    answer = ""

    user_id = getattr(request.state, "user_id", None)
    if user_id is None:
        return {"error": "User Not Logged In"}

    user_id = ObjectId(user_id)
    query = Input.text

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0,
    )

    user_doc = await history_collection.find_one({"user_id": user_id})
    history_data = user_doc.get("history", [])[-30:] if user_doc else []
    history = convert_mongo_history_to_langchain(history_data)

    # Step 1: Decide if retrieval is needed
    classifier_prompt = (
        "Determine whether the following user query requires specific document knowledge "
        "from a database to answer accurately. Answer 'yes' or 'no' only.\n\n"
        f'Query: "{query}"\n'
        "Answer:"
    )
    decision = llm.invoke(classifier_prompt)

    print(f"Decision: {decision.content}")

    if "yes" in decision.content:  # type: ignore

        prompt = ChatPromptTemplate(
            [
                SystemMessagePromptTemplate.from_template(system_config),
                *history,
                SystemMessagePromptTemplate.from_template("{context}"),
                HumanMessagePromptTemplate.from_template("{input}"),
            ]
        )

        vectorStore = MongoDBAtlasVectorSearch(
            rag_collection,  # type: ignore
            embeddings,
            index_name="gragnily_rag",
            embedding_key="embedding",
        )

        docs = vectorStore.similarity_search(query, k=1)
        context = docs[0].page_content if docs else "No matching document found."

        retriever = vectorStore.as_retriever()

        combine_docs_chain = create_stuff_documents_chain(llm, prompt)
        qa = retrieval.create_retrieval_chain(retriever, combine_docs_chain)

        answer = qa.invoke({"input": query, "context": context})

        answer = answer.get("answer")  # type: ignore
    else:
        prompt = ChatPromptTemplate(
            [
                SystemMessagePromptTemplate.from_template(system_config),
                *history,
                HumanMessagePromptTemplate.from_template("{input}"),
            ]
        )

        llm_chain = LLMChain(llm=llm, prompt=prompt)
        context = "No documents used for this query."
        answer = llm_chain.invoke({"input": query, "context": context})

        answer = answer.get("text")

    await history_collection.update_one(
        {"user_id": user_id},
        {
            "$push": {
                "history": {
                    "$each": [
                        {"role": "user", "parts": [{"text": Input.text}]},
                        {"role": "model", "parts": [{"text": answer}]},
                    ]
                }
            }
        },
        upsert=True,
    )

    return answer, context


async def get_history(request: Request):
    user_id = getattr(request.state, "user_id", None)

    if user_id is None:
        return {"error": "User Not Logged In"}
    try:

        user_id = ObjectId(user_id)
        # Find the history document for this user only
        found = await history_collection.find_one({"user_id": user_id})
        if not found:
            return {"error": "No history found"}
        history = found.get("history")
        return convert_objectid(history)
    except Exception as e:
        return {"error": str(e)}
