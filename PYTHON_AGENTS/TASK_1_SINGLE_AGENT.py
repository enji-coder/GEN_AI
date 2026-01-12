"""  
API KEY : ACCESS STEPS :
------------------------------------
Note : to generate new api key we can get new api key from 

    https://aistudio.google.com/

    create project and generate api key 
----------------------------------------
pip install python-dotenv

import os 
from dotenv import load_env

load_env() 

api_key = os.getenv("my-api-key")
------------------------------------
------------------------------------
for api access we have to install request package for python 

#pip install requests 

for genai we have to install google-generativeai 

#pip install google-generativeai 


"""
from dotenv import load_dotenv
import os 

import requests
import google.generativeai as genAI 

load_dotenv() # loading .env file content here 

# --------------------------------------------------------------
# step 1 : loading API secret key 

MY_API_KEY =  os.getenv("GEMINI_API_KEY")
genAI.configure(api_key=MY_API_KEY)

# --------------------------------------------------------------
# step 2 : we have to fetch models of genAI - so, auto detecting models 

def auto_detecting_model():
    for model in genAI.list_models():
        if "generateContent" in model.supported_generation_methods:
            print(f" working with this model : {model.name}")
            return genAI.GenerativeModel(model.name)
    raise Exception("No GenAi model Available for this key")


model = auto_detecting_model()
# print(model)

# --------------------------------------------------------------
# step 3 : User api :: 
USER_API = "https://6955f8b0b9b81bad7af1d95c.mockapi.io/api/users"

def fetchUserRecord():
    response = requests.get(USER_API)
    response.raise_for_status() #If the API request failed, stop the program and show the error clearly.
    return response.json() 

# print(fetchUserRecord()) # it will display all records from api 


# --------------------------------------------------------------
# step 4 : prepare context 
def context_builder(user_records):
    records = [] 

    for user in user_records:
        person_name = user.get("name","unknown")
        subject = user.get("subject","")
        score = user.get("score","")
        city = user.get("city","")
        age = user.get("age","")

        records.append(f"""
                    person name : {person_name}
                    subject : {subject}
                    score : {score}
                    city : {city}
                    age : {age}

                    """)

    return "\n".join(records)

# --------------------------------------------------------------
# step 5 : LLM CALL (Large Language Model) 

def llm_ask_prompt(prompt):
    response = model.generate_content(prompt)
    return response.text 


# --------------------------------------------------------------
# step 6 ::: Agentic AI (Observe -> Reason -> Act )

def agentic_ai(user_question):
    # observe 
    # so, fetch all records first of all 

    all_users = fetchUserRecord() 

    #reason 
    context = "Use the following users data only to answer questions : \n "+context_builder(all_users)

    final_prompt = (
        f"Your question is : {user_question} \n",
        f"Your Answer is : {context} \n",
    )

    # ACT 
    return llm_ask_prompt(final_prompt)


print("#################### WELCOME TO MY AGENTIC AI #####################")
status = True 
while status: 
    question = input("Ask your question : ")
    if question.lower() == "quit":
        status = False
    
    print("\n  AI RESPONSE   \n")
    print(agentic_ai(question))
    print("*"*50)










