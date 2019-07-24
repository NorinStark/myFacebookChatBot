import json
import os
import sys
from Utils import MessengerAPI

from pymongo import MongoClient
from flask import Flask, request

from Utils.MessengerAPI import send_message

app = Flask(__name__)

#Setting Environment for MongoDB
MONGO_URI = 'mongodb://NorinStark:123456Nr@ds251877.mlab.com:51877/heroku_jqdp5fwm'
mongo = MongoClient(MONGO_URI)
db = mongo["heroku_jqdp5fwm"]  #connect with the database's name


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200

# @app.route('/index')
# def index():
#     return render_template("index.html")

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

                        msg = db["first1234"]
                        memo = db["memory"]
                        message = msg.find({"keyword": message_text})
                        print(message_text)

                        try:
                            try:
                                        is_user_memo = memo.find({"sender_id": sender_id})
                                        print('erererer')
                                        for item in is_user_memo:
                                            for key, value in item.items():
                                                if value == 'null':
                                                    response = key
                                                    memo.update_one({"sender_id": sender_id}, {"$set": {key: message_text}})
                                                    break

                                        message = msg.find({"keyword": response})
                                        for msg in message:
                                            output = msg['response']
                                        send_message(sender_id, output)
                                        print('finish')

                            except Exception as e:
                                        print('memo failed')
                                        print(e)

                            for items in message:
                                        response = items["response"]

                            if items["type"] == "memory":
                                        memo.insert({"sender_id": sender_id})

                                        for keyword in response:
                                            memo.update({"sender_id": sender_id}, {"$set": {keyword: "null"}})
                                        null_keyword = memo.find({"sender_id": sender_id})
                                        print("0000>")

                                        for item in null_keyword:
                                            for key, value in item.items():
                                                if value == 'null':
                                                    response = key
                                                    break
                                        print('We are looking for ', response)
                                        message = msg.find({"keyword": response})
                                        for msg in message:
                                            output = msg['response']
                                        send_message(sender_id, output)
                                        print('finish')

                        except Exception as e:
                            print(e)

                        # send_message(sender_id, response)


                    elif messaging_event.get("delivery"):  # delivery confirmation
                        pass
                    elif messaging_event.get("optin"):  # optin confirmation
                        pass
                    elif messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message

                        pass

        return "ok", 200

    except Exception as e:
        return "ok", 200
        print(e)

    return "ok", 200
if __name__ == '__main__':
    app.run(DEBUG=True)
