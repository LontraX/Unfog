from flask import Flask, request, jsonify
from api import whatsapp
import os
from agents import agents

app = Flask(__name__)

@app.route('/webhook', methods=['GET','POST'])
def webhook():
    if request.method == 'GET':
        # Webhook verification
        verify_token = os.getenv("WHATSAPP_ACCESS_TOKEN")
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if mode and token:
            if mode == 'subscribe' and token == verify_token:
                print("Webhook verified successfully.")
                return challenge, 200
            else:
                return "Verification failed.", 403
    else:
        data = request.get_json()
        print("Webhook received data:", data)

        if 'entry' in data:
            for entry in data['entry']:
                for change in entry.get('changes', []):
                    value = change.get('value', {})
                    messages = value.get('messages', [])
                    for message in messages:
                        sender = message.get('from')  # User's phone number
                        message_text = message.get('text', {}).get('body')
                        agent_response = agents.do_stuff(message=message_text)

                        if message_text:
                            whatsapp.send_message(sender,agent_response)
    return jsonify(status="success"), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)
    