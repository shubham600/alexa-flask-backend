from flask import Flask, request, jsonify
import openai
import os
import random

app = Flask(name)
openai.api_key = os.environ.get("OPENAI_API_KEY")

user_memory = {}

def build_response(text): return { "version": "1.0", "response": { "outputSpeech": { "type": "PlainText", "text": text }, "shouldEndSession": False } }

@app.route("/", methods=["POST"]) def alexa_skill(): data = request.get_json() intent = None session_id = data.get("session", {}).get("user", {}).get("userId", "anonymous")

kotlin
Copy
Edit
if data["request"]["type"] == "LaunchRequest":
    return jsonify(build_response("Hey! I'm your buddy. What would you like to do?"))

if data["request"]["type"] == "IntentRequest":
    intent = data["request"]["intent"]["name"]

    # 🧠 Memory: Store favorite color
    if intent == "RememberColorIntent":
        try:
            color = data["request"]["intent"]["slots"]["color"]["value"]
            user_memory[session_id] = {"favorite_color": color}
            return jsonify(build_response(f"Okay, I’ll remember that your favorite color is {color}."))
        except:
            return jsonify(build_response("Hmm, I didn’t catch the color. Can you say it again?"))

    # 🧠 Recall favorite color
    elif intent == "RecallColorIntent":
        color = user_memory.get(session_id, {}).get("favorite_color", None)
        if color:
            return jsonify(build_response(f"You told me your favorite color is {color}."))
        else:
            return jsonify(build_response("I don’t remember your favorite color yet. Please tell me!"))

    # 😂 Jokes
    elif intent == "JokeIntent":
        jokes = [
            "Why did the tomato turn red? Because it saw the salad dressing!",
            "Why don't scientists trust atoms? Because they make up everything!",
            "What do you call fake spaghetti? An impasta!"
        ]
        return jsonify(build_response(random.choice(jokes)))

    # 💡 Advice
    elif intent == "AdviceIntent":
        advice = [
            "Always believe in yourself.",
            "Stay hydrated and get enough sleep.",
            "Never stop learning — every day is a chance to grow."
        ]
        return jsonify(build_response(random.choice(advice)))

    # 📖 Stories
    elif intent == "StoryIntent":
        stories = [
            "Once upon a time, a tiny bird dreamed of flying to the moon...",
            "In a faraway land, a clever fox outwitted a greedy lion...",
            "Long ago, a girl found a magical pebble that glowed in the dark..."
        ]
        return jsonify(build_response(random.choice(stories)))

    # 🧑‍🤝‍🧑 MyBuddyIntent
    elif intent == "MyBuddyIntent":
        return jsonify(build_response("Hey there! I'm your buddy. How can I help today?"))

    # 🤖 ChatGPT-style Q&A
    elif intent == "ChatGPTIntent":
        try:
            question = data["request"]["intent"]["slots"]["question"]["value"]
        except:
            question = ""

        if question:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful, friendly AI assistant."},
                        {"role": "user", "content": question}
                    ]
                )
                answer = response["choices"][0]["message"]["content"]
            except:
                answer = "Oops, something went wrong while contacting ChatGPT."
        else:
            answer = "Can you please ask your question again?"

        return jsonify(build_response(answer))

return jsonify(build_response("Sorry, I didn’t understand that. Try asking in a different way!"))
