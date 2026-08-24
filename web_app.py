from pathlib import Path
import webbrowser
from threading import Timer
import os

from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_from_directory
from langchain_google_genai import ChatGoogleGenerativeAI

from router import route_question
from rag_engine import answer_from_documents
from gridstatus_client import answer_from_gridstatus


BASE_DIR = Path(__file__).resolve().parent
WEBSITE_DIR = BASE_DIR / "website"

app = Flask(__name__, static_folder=str(WEBSITE_DIR), static_url_path="")


def summarize_hybrid_answer(question: str, api_answer: str, document_answer: str) -> str:
    """
    Uses Gemini to combine the GridStatus live data answer and the document/RAG answer
    into one clean response.
    """

    load_dotenv()

    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY is missing. Add it to your .env file.")

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0
    )

    prompt = f"""
You are an Ontario Grid Market AI Copilot.

The user asked:
{question}

Live IESO/GridStatus data:
{api_answer}

Document-based explanation:
{document_answer}

Write ONE clean answer for the user.

Rules:
- Do not separate the answer into "Live IESO Data" and "Document-Based Explanation."
- Do not include raw table formatting unless absolutely necessary.
- Start with the most important number or finding.
- If there is a price, include the value and unit $/MWh.
- If there is demand/load, include the value and unit MW.
- If there is fuel mix, summarize the major fuel types only.
- Then briefly explain what the result means in simple terms.
- Keep it concise, professional, and beginner-friendly.
- Do not say "Hello there."
"""

    response = llm.invoke(prompt)
    return response.content


def answer_hybrid_question(question: str) -> str:
    """
    Hybrid answer:
    1. Gets live/recent IESO data from GridStatus
    2. Gets document explanation from Chroma/RAG
    3. Uses Gemini to summarize both into one clean answer
    """

    api_answer = answer_from_gridstatus(question)

    document_question = (
        "Explain the IESO market concept related to this question in simple terms: "
        + question
    )

    document_answer = answer_from_documents(document_question)

    try:
        return summarize_hybrid_answer(question, api_answer, document_answer)

    except Exception as e:
        return (
            "I was able to retrieve the live data and document explanation, "
            "but I could not summarize them into one response.\n\n"
            f"Error: {e}\n\n"
            "Live IESO Data:\n"
            f"{api_answer}\n\n"
            "Document-Based Explanation:\n"
            f"{document_answer}"
        )


@app.route("/")
def home():
    return send_from_directory(WEBSITE_DIR, "index.html")


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True) or {}
    question = data.get("question", "").strip()

    if not question:
        return jsonify({
            "route": "none",
            "answer": "Please enter a question."
        })

    try:
        route = route_question(question)

        if route == "api":
            answer = answer_from_gridstatus(question)

        elif route == "documents":
            answer = answer_from_documents(question)

        elif route == "hybrid":
            answer = answer_hybrid_question(question)

        else:
            answer = answer_from_documents(question)

        return jsonify({
            "route": route,
            "answer": answer
        })

    except Exception as e:
        return jsonify({
            "route": "error",
            "answer": f"Something went wrong: {e}"
        })


def open_browser():
    webbrowser.open("http://127.0.0.1:5000")


if __name__ == "__main__":
    if not WEBSITE_DIR.exists():
        raise FileNotFoundError("website folder not found.")

    Timer(1, open_browser).start()
    app.run(host="127.0.0.1", port=5000, debug=False)