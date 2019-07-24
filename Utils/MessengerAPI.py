import os
import requests
import json

def send_message(recipient_id, response):

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
            "text": response
        }

    })

    # data = json.dumps({
    #     "recipient": {
    #         "id": recipient_id
    #     },
    #     "message": {
    #         "attachment":{
    #           "type":"template",
    #           "payload":{
    #             "template_type":"generic",
    #             "elements":[
    #                {
    #                 "title":"Welcome!",
    #                 "image_url":"https://wallpapercave.com/iron-man-4k-wallpapers",
    #                 "subtitle":"I am iron man!",
    #                 "default_action": {
    #                   "type": "web_url",
    #                   "url": "https://google.com",
    #                   "webview_height_ratio": "tall",
    #                 },
    #                 "buttons":[
    #                   {
    #                     "type":"web_url",
    #                     "url":"https://morning-headland-59802.herokuapp.com/index",
    #                     "title":"View Website",
    #                     "webview_height_ratio": "compact",
    #                     "messenger_extensions" : True
    #                   },{
    #                      "type": "web_url",
    #                      "url": "https://google.com",
    #                      "title": "View Website",
    #                      "webview_height_ratio": "tall"
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
    #     }
    # })

    vvv = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=EAAiXW5BCIMgBAKGspMXEuOdxtwHIZCTGOOfGNwnpE5CnFYj7ZAbzRhojkx0yAMS7Ca9lrQ64HuZAlfebs5nlKHJg9IQ0106hZBm7J5DxXN7jRoiieeRkwHARw8fNznyuXrteKnSW7dIWarLZCcFQaGfQ2vbFYJ9ZAMZBSr9SSnquwbuX7AZBbvQnFkCyT4MwVIcZD", params=params, headers=headers, data=data)
    print(vvv.text)
