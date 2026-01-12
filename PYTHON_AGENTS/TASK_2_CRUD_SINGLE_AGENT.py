from dotenv import load_dotenv
import os
import requests
import google.generativeai as genAI

# --------------------------------------------------------------
# ENV SETUP
load_dotenv()
MY_API_KEY = os.getenv("GEMINI_API_KEY")

genAI.configure(api_key=MY_API_KEY)

# --------------------------------------------------------------
# AUTO DETECT MODEL
def auto_detecting_model():
    for model in genAI.list_models():
        if "generateContent" in model.supported_generation_methods:
            print(f"Using model: {model.name}")
            return genAI.GenerativeModel(model.name)
    raise Exception("No GenAI model available")

model = auto_detecting_model()

# --------------------------------------------------------------
# API CONFIG
USER_API = "https://6955f8b0b9b81bad7af1d95c.mockapi.io/api/users"

def fetchUserRecord():
    response = requests.get(USER_API)
    response.raise_for_status()
    return response.json()

def insertUserRecord(newData):
    response = requests.post(USER_API, json=newData)
    response.raise_for_status()
    return response.json()

# --------------------------------------------------------------
# CONTEXT BUILDER
def context_builder(user_records):
    records = []

    for user in user_records:
        records.append(f"""
Name   : {user.get("name")}
Subject: {user.get("subject")}
Score  : {user.get("score")}
City   : {user.get("city")}
Age    : {user.get("age")}
""")

    return "\n".join(records)

# --------------------------------------------------------------
# LLM CALL
def llm_ask_prompt(prompt):
    response = model.generate_content(prompt)
    return response.text

# --------------------------------------------------------------
# LLM DECISION MAKER (AGENT BRAIN)
def llm_decide_action(user_question):
    decision_prompt = f"""
You are an AI controller.

Decide the correct action.

Available actions:
READ_USERS   -> viewing, analyzing, or asking questions about users
INSERT_USER  -> adding or creating a new user

User question:
{user_question}

Respond with ONLY one action name.
"""

    response = model.generate_content(decision_prompt)
    return response.text.strip()

# --------------------------------------------------------------
# COLLECT USER INPUT (ONLY WHEN REQUIRED)
def collect_new_user_data():
    print("\nEnter new user details:")
    return {
        "name": input("Name: "),
        "subject": input("Subject: "),
        "score": int(input("Score: ")),
        "city": input("City: "),
        "age": int(input("Age: "))
    }

# --------------------------------------------------------------
# AGENTIC AI (OBSERVE → REASON → ACT)
def agentic_ai(user_question):

    # OBSERVE & DECIDE
    action = llm_decide_action(user_question)
    print(f"\n[Agent Decision]: {action}\n")

    # ACT - INSERT
    if action == "INSERT_USER":
        new_user = collect_new_user_data()
        saved_user = insertUserRecord(new_user)
        return f"✅ User added successfully!\n{saved_user}"

    # ACT - READ
    elif action == "READ_USERS":
        users = fetchUserRecord()
        context = context_builder(users)

        final_prompt = f"""
Answer the user's question using ONLY the data below.

User Question:
{user_question}

User Data:
{context}
"""
        return llm_ask_prompt(final_prompt)

    else:
        return "❌ Unable to understand the request."

# --------------------------------------------------------------
# MAIN LOOP
print("#################### WELCOME TO AGENTIC AI #####################")

while True:
    question = input("\nAsk your question (type 'quit' to exit): ")
    if question.lower() == "quit":
        break

    print("\nAI RESPONSE:\n")
    print(agentic_ai(question))
    print("*" * 60)
