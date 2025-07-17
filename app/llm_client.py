import google.generativeai as genai
import httpx
import json
import sys

# Set your Gemini API Key here
genai.configure(api_key="AIzaSyANZqiFk73hag0hEVeiqYO8TH4rpzhAU2w")

model = genai.GenerativeModel(
    model_name="gemini-2.5-pro",
    tools=[
        {
            "function_declarations": [
                {
                    "name": "register_user",
                    "description": "Register a user with name, email, and date of birth",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "email": {"type": "string"},
                            "dob": {"type": "string"},
                        },
                        "required": ["name", "email", "dob"],
                    },
                },
                {
                    "name": "get_registrations",
                    "description": "Get all registered users",
                    "parameters": {"type": "object", "properties": {}},
                },
            ]
        }
    ],
)

chat = model.start_chat(history=[])

def handle_tool_call(name, args):
    if name == "register_user":
        print(f"📨 Registering user: {args}")
        try:
            resp = httpx.post("http://localhost:8000/register", json=dict(args))
            resp.raise_for_status()
            return f"✅ {args['name']} registered successfully."
        except Exception as e:
            return f"❌ Failed to register user: {str(e)}"

    elif name == "get_all_users":
        print("📨 Fetching all registrations...")
        try:
            resp = httpx.get("http://localhost:8000/registrations")
            resp.raise_for_status()
            users = resp.json()
            if not users:
                return "📂 No users found."
            return "\n".join([f"{u['name']} ({u['email']}) - {u['dob']}" for u in users])
        except Exception as e:
            return f"❌ Failed to fetch users: {str(e)}"

def run_gemini_chat(prompt):
    response = chat.send_message(prompt)

    if response.candidates[0].content.parts[0].function_call:
        tool = response.candidates[0].content.parts[0].function_call
        name = tool.name
        args = tool.args
        result = handle_tool_call(name, args)
        print("🤖 Gemini Response:\n", result)
    else:
        print("🤖 Gemini Response:\n", response.text)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python app/llm_client.py 'Your prompt here'")
    else:
        prompt = " ".join(sys.argv[1:])
        run_gemini_chat(prompt)
