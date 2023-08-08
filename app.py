from flask import Flask, session, request, jsonify
from flask_cors import CORS, cross_origin
import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import DirectoryLoader
from flask_session import Session
from langchain.chat_models import ChatOpenAI
import openai
import chromadb
from chromadb.config import Settings
from langchain.embeddings import GPT4AllEmbeddings
from gpt4all import GPT4All

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)
app.secret_key = "your_secret_key"
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


openai.api_key = os.getenv("OPENAI_API_KEY")
embeddings = GPT4AllEmbeddings()
client = chromadb.PersistentClient(path="persist/")
vectorstore = Chroma(
    client=client, collection_name="newcol", embedding_function=embeddings
)

session_manager = {}


@app.route("/ask", methods=["GET"])
def hello_world():
    qa = None
    session_id = request.headers.get("uuid")
    if session_id not in session_manager:
        memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )
        llm = OpenAI(temperature=0.9, model="text-davinci-003")
        qa = ConversationalRetrievalChain.from_llm(
            llm,
            vectorstore.as_retriever(),
            memory=memory,
        )
        session_manager[session_id] = qa
    else:
        qa = session_manager[session_id]
    query = request.args.get("query")
    result = qa({"question": query})
    session_manager[session_id] = qa
    return jsonify({"answer": result["answer"]})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("3000"))
