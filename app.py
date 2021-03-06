import os, sys
from flask import Flask, request
from pymessenger.bot import Bot
import nutritionsearch, decoder, response, json


from flask import Flask, request
import requests

app = Flask(__name__)

ACCESS_TOKEN = "EAAECxaoUf2UBAL987CccjNQxbpomeZCoPeaVCzFDKgbEUfwPhWaUmuMTGmylUiC3wXZCFbe5sNAbO5IBbl5onfftWQAPNMsUeGDpBACcKpeZAdU653TFnGSzvXIYmVLEYxNv69gTtaCTOP6azs4Sa7nPhq0WaO1LUNkbOfLPgZDZD"


def reply(user_id, msg):
    data = {
        "recipient": {"id": user_id},
        "message": {"text": msg}
    }
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
    print(resp.content)


@app.route('/', methods=['POST'])
def handle_incoming_messages():
    data = request.json
    sender = data['entry'][0]['messaging'][0]['sender']['id']
    message = data['entry'][0]['messaging'][0]['message']['text']
    print("Message coming in is", message)
    if message == 'check':
    	with open('users.json', 'r') as f:
    		users = json.load(f)['users']
    		# print("users object", users)
    		for user in users:
    			# print(user)
    			if user['id'] == sender:
    				respond = "Current calories: " + str(int(user['caloriesT'])) + " calories" + "\nTotal calories: " + str(user['caloriesG']) + " calories" + "\nCalories remaining: " + str(int(user['caloriesG']) - int(user['caloriesT'])) + " calories"
    	print(respond)
    elif message == 'reset':
    	with open('users.json', 'r') as f:
    		data = json.load(f)
    		users = data['users']
    		for user in users:
    			if user['id'] == sender:
    				user['caloriesT'] = 0
    				respond = "Your total calories have been reset to 0."
    	with open('users.json', 'w') as f:
    		f.write(json.dumps(data))
    elif 'setgoal' in message:
    	newgoal = message.split()[1]
    	with open('users.json', 'r') as f:
    		data = json.load(f)
    		users = data['users']
    		for user in users:
    			if user['id'] == sender:
    				user['caloriesG'] = newgoal
    				respond = "Your new goal is " + newgoal + " calories."
    	with open('users.json', 'w') as f:
    		f.write(json.dumps(data))
    elif message == 'help':
    	respond = "Input: Be sure each food's phrase is separated by a comma.\nCheck current stats: 'check'\nReset: 'reset'\nSet a new goal: 'setgoal' <Number>"
    else:
    	respond = response.getResponse(sender, nutritionsearch.get_meals(message))
    reply(sender, respond)

    return "ok"


if __name__ == '__main__':
    app.run(debug=True)
