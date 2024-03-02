import json
from httpx import AsyncClient
import requests
from app.schemas import Response
import random
import math


API = "196545763551645"
URL = "https://graph.facebook.com/v18.0/237284509471319/messages"
CODE = ""

def generate():
    a =  random.randint(1000, 9999)

    global CODE
    CODE = a
    return str(a)



def sendMessage(number:int):
    code = generate()


    data = json.dumps({
     "messaging_product": "whatsapp",
     "recipient_type": "individual",
     "to": "+78"+str(number),
     "type": "template",
     "template": {
       "name": "sending_msg_auth",
       "language": {
          "code": "ru"
    },
      "components": [
      {
        "type": "body",
        "parameters": [
          {
            "type": "text",
            "text": code
          }
        ]
      },
      {
        "type": "button",
        "sub_type": "url",
        "index": "0",
        "parameters": [
          {
            "type": "text",
            "text": code
          }
        ]
      }
    ]
  }
}
    )




    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer EAATZCc3Y9atgBO41Qk4SXjVPZB2NOdEssZA8b3ZAmZCAd9RntKBsBA2hws7zUltxW459ZBhf7oGWvt6ZA0ni21zGQnhKhOEQSlVRvphN4IPYVMjG4MNPZB6rdzH4fLC7YkUC4JuoCs2M4Pyc2ktCd9csX663tAhcVAofVTjrGKRrQhLIxQYbS9KHChtJTmP80lweYoz0fJ6x8VJeltFO"}
    responce = requests.post(url=URL, data=data, headers=headers)
    print(json.dumps(data))
    return Response(code = responce.status_code, status= "Send",message=responce.text)

def verify(codeS):
    print(CODE)
    if str(codeS).__eq__(CODE):
        return True
    else:
        return False