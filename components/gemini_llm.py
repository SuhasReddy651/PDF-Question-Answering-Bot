from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()


def get_gemini_response(query: str, context: str = "") -> str:
    """
    Sends a query to Gemini with optional context and returns the response.
    """
    try:
        prompt = f"""Answer the following based on the given context.\n
        Context: {context}\n
        User: {query}
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=-1)
            )
        )

        return response.text.strip()

    except Exception as e:
        return f"❌ Gemini Error: {e}"
