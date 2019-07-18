import os
import sys
import json
import requests

from pymongo import MongoClient
from flask import Flask, request, render_template

app = Flask(__name__)

MONGO_URI = 'mongodb://NorinStark:123456Nr@ds251877.mlab.com:51877/heroku_jqdp5fwm'
client = MongoClient(MONGO_URI)
messages = client["heroku_jqdp5fwm"] #database

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200

@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/blog/<int:postID>')
def show_blog(postID):
   return 'Blog Number %d' % postID

@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events
    try:

        data = request.get_json()
        print(data)

        if data["object"] == "page":

            for entry in data["entry"]:
                for messaging_event in entry["messaging"]:

                    if messaging_event.get("message"):  # someone sent us a message

                        sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                        recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                        message_text = messaging_event["message"]["text"]  # the message's text

                        # msg = messages["first1234"]  # colelction
                        # message = msg.find({"keyword": message_text})
                        # print('here')
                        # print(message)
                        # for thing in message:
                        #     print('========>',thing['respone'])
                        #
                        # response = thing['respone']

                        # response = {"message" : {
                        #         "attachment":{
                        #           "type":"template",
                        #           "payload":{
                        #             "template_type":"generic",
                        #             "elements":[
                        #                {
                        #                 "title":"Welcome!",
                        #                 "image_url":"",
                        #                 "subtitle":"The true is... I am iron man!",
                        #                 "default_action": {
                        #                   "type": "web_url",
                        #                   "url": "https://google.com",
                        #                   "webview_height_ratio": "tall",
                        #                 },
                        #                 "buttons":[
                        #                   {
                        #                     "type":"web_url",
                        #                     "url":"https://google.com",
                        #                     "title":"View Website"
                        #                   },{
                        #                     "type":"postback",
                        #                     "title":"Start Chatting",
                        #                     "payload":"DEVELOPER_DEFINED_PAYLOAD"
                        #                   }
                        #                 ]
                        #               }
                        #             ]
                        #           }
                        #         }
                        #       }
                        # }
                        #
                        #
                        send_message(sender_id)

                    if messaging_event.get("delivery"):  # delivery confirmation
                        pass
                    if messaging_event.get("optin"):  # optin confirmation
                        pass
                    if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                        pass

        return "ok", 200

    except Exception as e:
        return "ok", 200
        print(e)

def send_message(recipient_id):

    params = {
        "access_token=": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment":{
              "type":"template",
              "payload":{
                "template_type":"generic",
                "elements":[
                   {
                    "title":"Welcome!",
                    "image_url":"https://wallpapercave.com/iron-man-4k-wallpapers",
                    "subtitle":"I am iron man!",
                    "default_action": {
                      "type": "web_url",
                      "url": "https://google.com",
                      "webview_height_ratio": "tall",
                    },
                    "buttons":[
                      {
                        "type":"web_url",
                        "url":"https://morning-headland-59802.herokuapp.com/index",
                        "title":"View Website",
                        "webview_height_ratio": "compact",
                        "messenger_extensions" : True
                      },{
                         "type": "web_url",
                         "url": "https://google.com",
                         "title": "View Website",
                         "webview_height_ratio": "tall"
                      },{
                        "type":"postback",
                        "title":"Start Chatting",
                        "payload":"DEVELOPER_DEFINED_PAYLOAD"
                      }
                    ]
                  }
                ]
              }
            }
        }
    })

    vvv = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=EAAiXW5BCIMgBAKGspMXEuOdxtwHIZCTGOOfGNwnpE5CnFYj7ZAbzRhojkx0yAMS7Ca9lrQ64HuZAlfebs5nlKHJg9IQ0106hZBm7J5DxXN7jRoiieeRkwHARw8fNznyuXrteKnSW7dIWarLZCcFQaGfQ2vbFYJ9ZAMZBSr9SSnquwbuX7AZBbvQnFkCyT4MwVIcZD", params=params, headers=headers, data=data)
    print(vvv.text)
    return "ok", 200
if __name__ == '__main__':
    app.run(DEBUG=True)
