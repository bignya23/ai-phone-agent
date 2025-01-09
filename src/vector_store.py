
from langchain.tools import Tool
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
import os
from langchain.schema import Document
from langchain.text_splitter import CharacterTextSplitter

def vector_index():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

    vector_store = InMemoryVectorStore(embeddings)

    content = ""
    with open("product_info.txt", "r") as f:
        content = f.read()
    # print(content)

    text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=100,  # Maximum characters in a chunk
    chunk_overlap=10  # Overlap between chunks for better context
)

    chunks = text_splitter.split_text(content)

    vector_store = FAISS.from_texts(texts=chunks, embedding=embeddings)

    vector_store.save_local("vector_store/knowledge_base")


if __name__ == "__main__":
    vector_index()
  