from fastmcp import Client
from google import genai 
import asyncio
import os 
from dotenv import load_dotenv

load_dotenv()

# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

# The Client automatically uses StreamableHttpTransport for HTTP URLs
async def gemini_chat_model(user_message:str):
    mcp_client = Client("http://127.0.0.1:8000/mcp")
    gemini_client = genai.Client(api_key=GEMINI_API_KEY)

    async with mcp_client:
        response = await gemini_client.aio.models.generate_content(
            model="gemini-1.5-flash-latest",
            contents=user_message,
            config=genai.types.GenerateContentConfig(
                tools=[mcp_client.session],
                temperature=0.2,
            )
        )
        return response.text
        
async def main():
    print("Talk to the Gemini LLM (type 'exit' to quit):")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        result = await gemini_chat_model(user_input)
        print("Gemini:", result)

if __name__ == "__main__":
    asyncio.run(main()) 
