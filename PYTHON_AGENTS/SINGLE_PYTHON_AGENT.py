"""   
steps to understand 

step1 :::   user ask question 
                |
                V 

step 2 :::  Agent  (Reasoning)

                |
                V 

step 3 ::   Fetch api  e.g.  Mockapi.io

                |
                V 

step 4 :::   convert into structured data 

                |
                V 
step 5 :::  Gemini LLM (Explanation/Answer)
                |
                V 
            Final smart ANswer

e.g.  Questions like 

Which product is cheapest?
List all products with price
Furniture under 3000
Which category has highest price product?
Suggest best value furniture


here are working with users 

https://6955f8b0b9b81bad7af1d95c.mockapi.io/api/users

"""
import requests    # pip install requests
import google.generativeai as genai  #pip install google-generativeai

#---------step 1 ::: GEMNI API KEY 
GEMINI_API_KEY = "AIzaSyAV2Nt12m35bWwZ55HZH7_D2CpfAb4iL_w"
genai.configure(api_key=GEMINI_API_KEY)   # configure this key 


#---------step 2 ::: Auto detect working model for gemini model 
def get_working_model():
    for m in genai.list_models():
        if "generateContent" in m.supported_generation_methods:
            print(f"Using this gemini model : {m.name}")
            return genai.GenerativeModel(m.name)
    raise Exception("No Gemini Model Available for this API Key")

model = get_working_model()


# --------step 3 ::: API use - USER API 
USER_API = "https://6955f8b0b9b81bad7af1d95c.mockapi.io/api/users"

def fetchUserRecord():
    response = requests.get(USER_API)
    response.raise_for_status()  #If the API request failed, stop the program and show the error clearly.
    return response.json()

# print("------>>> ",fetchUserRecord())

# user = {
#     "name": "Anjali Patel",
#     "subject": "Python",
#     "score": 98,
#     "city": "Ahmedabad",
#     "age": 30
# }

# def insertRecord():
#     request = requests.post(USER_API,json=user)
#     request.raise_for_status()
#     return request.json()

# print("\n\n")
# print("------->>>> ",insertRecord())


#-----step 4 : Context builder (FIXED AS per real api schema)
def prepare_context(users):
    lines = []

    for u in users:
        person_name = u.get("name","unknown")
        subject = u.get("subject","")
        score = u.get("score","")
        city = u.get("city","")
        age = u.get("age","")

        lines.append(f""" 
                person name : {person_name}
                subject : {subject}
                score : {score}
                city : {city}
                age : {age}
            """)
        
    return "\n".join(lines)
    
#----STEP 5 ::: LLM CALL 
def ask_LLM(prompt):
    response = model.generate_content(prompt)
    return response.text

#---STEP 6 ::: AGENTIC AI (OBSERVE -> REASON -> ACT)
def agentic_ai(user_question):
    #observe 
    users = fetchUserRecord()

    #reason 
    context ="Use the following users data ONLY to answer questions: \n"+prepare_context(users)

    final_prompt = (
        "HEY, I M SUPER AI AGENT GIVING YOU RESULT \n\n",
        f"Your Question is : {user_question} \n",
        f"Your ANswer is :: {context} \n",
        "You can ask any questions to me :) "
    )

    #ACT 
    return ask_LLM(final_prompt)


print("\n\n\n############ WELCOME TO AGENTIC AI ################ \n")
print("\n Type 'exit' to stop ")

while True:
    question = input("Ask your Question : ")
    if question.lower() == "exit":
        break

    print("\n AI AGENT REPLY :::: \n")
    print(agentic_ai(question))
    print("-"*60)
    
