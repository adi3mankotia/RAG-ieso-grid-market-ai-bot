import os
from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI


VECTOR_STORE_FOLDER = "vector_store"
COLLECTION_NAME = "ieso_documents"


def answer_from_documents(question: str) -> str:
    load_dotenv()

    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY is missing. Add it to your .env file.")

    if not os.path.exists(VECTOR_STORE_FOLDER):
        raise FileNotFoundError(
            "vector_store folder not found. Run python build_vector_db.py first."
        )

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db = Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=VECTOR_STORE_FOLDER,
        embedding_function=embeddings
    )

    retriever = db.as_retriever(search_kwargs={"k": 4})
    relevant_docs = retriever.invoke(question)

    if not relevant_docs:
        return "I could not find relevant information in the IESO documents."

    context = "\n\n".join(
        [
            f"Source: {doc.metadata.get('source', 'Unknown source')}\n"
            f"Page: {doc.metadata.get('page', 'Unknown page')}\n"
            f"Content: {doc.page_content}"
            for doc in relevant_docs
        ]
    )

    prompt = f"""
You are an IESO Grid Market AI Copilot.

Answer the user's question using only the IESO document context below.
If the answer is not in the context, say that the documents do not provide enough information.

Keep the answer clear and friendly.

IESO document context:
{context}

User question:
{question}
"""

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0
    )

    response = llm.invoke(prompt)

    return response.content


if __name__ == "__main__":
    print("Testing IESO document chatbot...")
    print("Type 'exit' to quit.")

    while True:
        user_question = input("\nAsk a document question: ")

        if user_question.lower() in ["exit", "quit", "q"]:
            print("Goodbye.")
            break

        answer = answer_from_documents(user_question)

        print("\nChatbot answer:")
        print(answer)