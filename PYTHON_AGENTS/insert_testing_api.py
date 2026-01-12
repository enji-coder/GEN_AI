import requests

USER_API = "https://6955f8b0b9b81bad7af1d95c.mockapi.io/api/users"


def insertUserRecord(newData):
    response = requests.post(USER_API,json = newData)
    response.raise_for_status() 
    return response.json()


newData = {
    "name": "SHREYA GHOSHAL 2",
    "subject": "Python",
    "id": "12",
    "score": 98,
    "city": "Ahmedabad",
    "age": 30
}

print(insertUserRecord(newData))    

    
