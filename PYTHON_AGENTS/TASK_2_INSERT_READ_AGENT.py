from dotenv import load_dotenv
import os 
import requests
import google.generativeai as genAI 


# ENV setup ---------------------------------------------------------

load_dotenv() 

# configure API 
MY_API_KEY = os.getenv("GEMINI_API_KEY")

genAI.configure(api_key=MY_API_KEY)


# AUTO DETECTED MODEL ---------------------

def auto_detected_model():
    for model in genAI.list_models():
        if "generateContent" in model.supported_generation_methods:
            print(f" Using {model.name} model ")
            return genAI.GenerativeModel(model.name)
    raise Exception("No GenAI model Available ")


model = auto_detected_model()



# API CONFIGURATION --------------------------------

USER_API = "https://6955f8b0b9b81bad7af1d95c.mockapi.io/api/users"

def fetchUserRecord():
    response = requests.get(USER_API)
    response.raise_for_status()
    return response.json()

def insertUserRecord(newData):
    response = requests.post(USER_API,json=newData)
    response.raise_for_status()
    return response.json()

# context builder -----------------------------
def context_builder(user_records):
    records = [] 

    for user in user_records:
        records.append(f"""
                Name : {user.get("name")}
                Subject : {user.get("subject")}
                Score : {user.get("score")}
                City : {user.get("city")}
            """)
        
    return "\n".join(records)

# LLM Call --------------
def llm_decide_action(user_question):
    response = model.generate_content(user_question)
    return response.text 


# collect new records for user
def collect_new_record():
    print("Please Enter new User Detailes ::")
    return {
        "name" : input("Enter name : "),
        "subject":input("Enter subject : "),
        "score": int(input("Enter score : ")),
        "city" : input("Enter city : "),
        "age" : int(input("Enter age : "))
    }

# Agentic AI (Observe -> Reason -> Act)

def agentic_ai(user_question):

    # first we have to decide action 
    action = llm_decide_action(user_question)

    if action == "insert":
        new_user = collect_new_record()
        insertUserRecord(new_user)
        return f"Successfully record added !!"
    
    elif action == "read":
        users = fetchUserRecord() 
        context = context_builder(users)

        final_prompts = f""" 
                        user data ::: {context}
                        """
        return llm_decide_action(final_prompts)
    # print("AGENT DECISION ::: ",action)

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