import openai
import os
import random
from flask import Flask, request, jsonify

# Set OpenAI API key from environment
openai.api_key = os.environ.get("OPENAI_API_KEY")

app = Flask(__name__)
user_memory = {}

def build_response(text):
    return {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": text
            },
            "shouldEndSession": False
        }
    }

@app.route('/', methods=['POST'])
def alexa_skill():
    data = request.get_json()

    intent = None
    session_id = data.get("session", {}).get("user", {}).get("userId", "anonymous")

    # Handle LaunchRequest
    if data["request"]["type"] == "LaunchRequest":
        return jsonify(build_response("Hey! I'm your buddy. What would you like to do?"))

    if data["request"]["type"] == "IntentRequest":
        intent = data['request']['intent']['name']

        if intent == "RememberColorIntent":
            try:
                color = data['request']['intent']['slots']['color']['value']
                user_memory[session_id] = {"favorite_color": color}
                return jsonify(build_response(f"Okay, I’ll remember that your favorite color is {color}."))
            except:
                return jsonify(build_response("Hmm, I didn’t catch the color. Can you say it again?"))

        elif intent == "RecallColorIntent":
            color = user_memory.get(session_id, {}).get("favorite_color", None)
            if color:
                return jsonify(build_response(f"You told me your favorite color is {color}."))
            else:
                return jsonify(build_response("I don’t remember your favorite color yet. Please tell me!"))

        elif intent == "JokeIntent":
            jokes = [
                "Why did the tomato turn red? Because it saw the salad dressing!",
                "Why don't scientists trust atoms? Because they make up everything!",
                "What do you call fake spaghetti? An impasta!"
            ]
            return jsonify(build_response(random.choice(jokes)))

        elif intent == "AdviceIntent":
            advice = [
                "Always believe in yourself.",
                "Stay hydrated and get enough sleep.",
                "Never stop learning — every day is a chance to grow."
            ]
            return jsonify(build_response(random.choice(advice)))

        elif intent == "StoryIntent":
            stories = [
                "Once upon a time, a tiny bird dreamed of flying to the moon...",
                "In a faraway land, a clever fox outwitted a greedy lion...",
                "Long ago, a girl found a magical pebble that glowed in the dark..."
            ]
            return jsonify(build_response(random.choice(stories)))

        elif intent == "MyBuddyIntent":
            return jsonify(build_response("Hey there! I'm your buddy. How can I help today?"))

        elif intent == "ChatGPTIntent":
            try:
                question = data['request']['intent']['slots']['question']['value']
            except:
                question = ""

            if question:
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are My Buddy, a friendly, fun, helpful companion who talks casually like a buddy. You remember things told to you earlier in the conversation."},
                            {"role": "user", "content": question}
                        ],
                        temperature=0.8,
                        max_tokens=200
                    )
                    answer = response.choices[0].message.content.strip()
                except Exception as e:
                    print(f"OpenAI Error: {e}")
                    answer = "Oops! My brain glitched talking to the AI. Can you ask again?"
            else:
                answer = "Hmm, I didn’t catch that. Can you repeat your question?"

            return jsonify(build_response(answer))

    # Default fallback
    return jsonify(build_response("Sorry, I didn’t understand that. Try asking in a different way!"))
