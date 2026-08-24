from pathlib import Path
import webbrowser

from router import route_question
from rag_engine import answer_from_documents
from gridstatus_client import answer_from_gridstatus


BASE_DIR = Path(__file__).resolve().parent


def open_intro_website():
    """
    Opens the local intro website when the program starts.
    """
    website_path = BASE_DIR / "website" / "index.html"

    print(f"Looking for website at: {website_path}")

    if website_path.exists():
        webbrowser.open(website_path.as_uri())
        print("Website opened successfully.")
    else:
        print("Website file not found. Skipping website launch.")


def answer_hybrid_question(question: str) -> str:
    api_answer = answer_from_gridstatus(question)

    document_question = (
        "Explain the IESO market concept related to this question in simple terms: "
        + question
    )

    document_answer = answer_from_documents(document_question)

    return (
        "Live IESO Data:\n"
        f"{api_answer}\n\n"
        "Document-Based Explanation:\n"
        f"{document_answer}"
    )


def main():
    open_intro_website()

    print("=" * 70)
    print("Ontario Grid Market AI Copilot")
    print("=" * 70)
    print("The intro website should now be open in your browser.")
    print("Ask questions about IESO price, demand, supply mix, generators, or market concepts.")
    print("Type 'exit' to quit.")
    print("=" * 70)

    while True:
        question = input("\nAsk a question: ").strip()

        if question.lower() in ["exit", "quit", "q"]:
            print("Goodbye.")
            break

        if not question:
            print("Please enter a question.")
            continue

        try:
            route = route_question(question)
            print(f"\nRoute selected: {route}")

            if route == "api":
                answer = answer_from_gridstatus(question)

            elif route == "documents":
                answer = answer_from_documents(question)

            elif route == "hybrid":
                answer = answer_hybrid_question(question)

            else:
                answer = answer_from_documents(question)

            print("\nChatbot answer:")
            print(answer)

        except Exception as e:
            print("\nSomething went wrong:")
            print(e)


if __name__ == "__main__":
    main()