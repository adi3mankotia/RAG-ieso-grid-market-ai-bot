import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


def keyword_route(question: str) -> str:
    """
    Python handles obvious questions.
    If the question is hard/ambiguous, return 'unclear'
    so Gemini can decide.
    """

    q = question.lower().strip()

    
    grid_status_phrases = [
        "how does the grid look",
        "how does the grid look like",
        "how is the grid looking",
        "how is the electricity system looking",
        "grid status",
        "system status",
        "how is the grid",
        "how is ontario's grid",
        "how is ontario grid",
    ]

    if any(phrase in q for phrase in grid_status_phrases):
        return "hybrid"

    live_keywords = [
        "current",
        "right now",
        "latest",
        "today",
        "tomorrow",
        "now",
        "live",
        "real-time",
        "realtime",
    ]

    data_keywords = [
        "mw",
        "megawatt",
        "megawatts",
        "load",
        "demand",
        "price",
        "day-ahead",
        "day ahead",
        "supply mix",
        "fuel mix",
        "generation",
        "generating",
        "producing",
        "power being used",
        "electricity being used",
    ]

    document_keywords = [
        "what is",
        "what does",
        "explain",
        "define",
        "definition",
        "meaning",
        "how does",
        "why",
        "rules",
        "market rules",
        "overview",
        "role",
        "purpose",
        "describe",
    ]

    wants_live = any(keyword in q for keyword in live_keywords)
    wants_data = any(keyword in q for keyword in data_keywords)
    wants_docs = any(keyword in q for keyword in document_keywords)

    # Very obvious API question
    if wants_live and wants_data and not wants_docs:
        return "api"

    # Very obvious hybrid question
    if wants_live and wants_data and wants_docs:
        return "hybrid"

    # Very obvious document question
    if wants_docs and not wants_data:
        return "documents"

    # Ambiguous cases go to Gemini
    # Example: "What is Ontario price?"
    # Example: "What is day-ahead pricing?"
    # Example: "Is demand high?"
    if wants_docs and wants_data:
        return "unclear"

    if wants_data and not wants_live:
        return "unclear"

    return "unclear"


def gemini_route(question: str) -> str:
    """
    Gemini handles hard/unclear routing decisions.
    """

    load_dotenv()

    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY is missing. Add it to your .env file.")

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0
    )

    prompt = f"""
You are a routing classifier for an IESO electricity market chatbot.

Classify the user's question into exactly ONE route:

api = The user wants current, live, recent, or numerical IESO data.
Examples:
- current Ontario demand
- current price
- today's demand
- real-time price
- day-ahead price for tomorrow
- current supply mix
- current fuel mix
- how much power is Ontario using right now

documents = The user wants definitions, explanations, background, rules, purpose, or concepts.
Examples:
documents = The user wants definitions, explanations, background, rules, purpose, or concepts.
Examples:
- what does IESO do
- what does Ontario price mean
- explain day-ahead pricing
- what does zonal price mean
- how does Ontario's electricity market work
- what are market rules

hybrid = The user wants both current/live data and explanation.
Examples:
- explain the current Ontario price
- what does today's demand mean
- how does the grid look today
- summarize the current supply mix
- is the current demand high or low
- what is the price
- what is the Ontario price

Return only one word:
api
documents
hybrid

User question:
{question}
"""

    try:
        response = llm.invoke(prompt)
        route = response.content.strip().lower()

        if route in ["api", "documents", "hybrid"]:
            return route

        return "documents"

    except Exception as e:
        print(f"Gemini routing failed: {e}")
        return "documents"


def route_question(question: str) -> str:
    """
    Main router:
    1. Python handles clear questions.
    2. Gemini handles hard/unclear questions.
    """

    route = keyword_route(question)

    if route != "unclear":
        return route

    print("Python router was unsure, asking Gemini...")
    return gemini_route(question)


if __name__ == "__main__":
    print("Testing IESO router...")
    print("Type 'exit' to quit.")

    while True:
        user_question = input("\nAsk a question to route: ")

        if user_question.lower() in ["exit", "quit", "q"]:
            print("Goodbye.")
            break

        selected_route = route_question(user_question)
        print(f"Route selected: {selected_route}")