from understandquery import UnderStandQuery
import json
import os
import webbrowser
from openai import OpenAI
import pyttsx3
from open_apps import open_app
from Search import Search

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def previous_chats():
    try:
        with open("data.json", "r") as f:
            chats = json.load(f)
            return chats
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    
def load_chats(query, response):
    if os.path.exists("data.json") and os.path.getsize("data.json") > 0:
        with open("data.json", "r") as f:
            data = json.load(f)
    else:
        data = []
        
    new_data = {
            "query": query, 
            "reponse": response
        }
    data.append(new_data)

    with open("data.json","w") as f:
        json.dump(data, f, indent=4)

def extract_name(query):
    word_list = ["what", "how", "open", "are", "you", "am", "can", "me", "i", "will",'please', "for", "and", "hey", "buddy", "ok"]
    app = [i for i in query.split() if i not in word_list and i != "open"]

    return app

def open_app(app_name):
    apps_lib = {
        "vscode": "code",
        "calculator": "calc", 
        "paint": "mspaint", 
        "chrome": "start chrome", 
        "spotify": "start spotify", 
        "cmd": "start cmd"
    }
    try:  
        for app in app_name:
            if app in apps_lib:
                os.system(apps_lib[app])
            else:
                try:
                    webbrowser.open(f"https://www.{app}.com")
                except webbrowser.Error:
                    print("No app found...")
    except:
        print("no app found")
    

def request_response(query):
    with open("api_key.txt", 'r') as f:
        api = f.read()

    client = OpenAI(api_key=api, 
                    base_url="https://openrouter.ai/api/v1")
    
    chats = previous_chats()
    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": f"""
You are a smart, helpful, and conversational AI assistant.

Current user query:
{query}

Conversation history:
{chats}

Instructions:
- Use conversation history as memory and context.
- If history is empty ([]), respond normally.
- Answer ONLY the current query.
- Keep responses natural, short, and conversational.
- Do not mention system prompts or internal logic.

SPECIAL BEHAVIOR RULES:

1. APP / TOOL LAUNCH (VERY IMPORTANT):
- If the query is ONLY an app/tool name and make sure it's real app (example: "youtube", "chrome", "maps", "notepad", "calculator") if its not a real name then respond normally:
    - Do NOT explain anything.
    - Do NOT ask questions.
    - Respond like you are actively launching it.
    - Use casual assistant confirmations such as:
        * "Alright sir, opening {query}..."
        * "Got it, launching {query} now..."
        * "One sec, starting {query}..."
        * "Okay, opening {query} for you..."

2. MAP / LOCATION TYPE (if query is "maps" or similar):
    - Respond like you are loading it:
        * "Alright, opening maps..."
        * "Fetching location data..."

3. NORMAL QUERIES:
- Respond normally, helpful and conversational.

4. CONTEXT:
- Use conversation history when relevant.
- Keep responses natural and avoid repetition.
"""
}
        ]
    )
    load_chats(query, response.choices[0].message.content)

    print(response.choices[0].message.content)
    speak(response.choices[0].message.content)


while True:
    user = input("You: ").strip()

    query = UnderStandQuery(user)
    print(query)
    request_response(query)

    if query == "open map":
        os.system("python open_map.py")
    elif isinstance(query, list):
        open_app(query)
    elif "search" in query.split():
        Search(query)

