from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "Alexa Skill Server is Running"

@app.route("/", methods=["POST"])
def webhook():
    return jsonify({
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": "Hello from your Alexa skill on Render!"
            },
            "shouldEndSession": False
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
@app.route('/', methods=['POST'])
def alexa_webhook():
    data = request.get_json()

    intent = None
    try:
        intent = data['request']['intent']['name']
    except:
        pass

    if data['request']['type'] == "LaunchRequest":
        return jsonify(build_response("Hi! My Buddy is online and ready to talk!"))

    elif intent == "JokeIntent":
        joke = random.choice([
            "Why don’t scientists trust atoms? Because they make up everything!",
            "What do you call fake spaghetti? An impasta.",
            "Why did the scarecrow win an award? Because he was outstanding in his field."
        ])
        return jsonify(build_response(joke))

    elif intent == "AdviceIntent":
        advice = random.choice([
            "Don't be afraid to fail. It's how we grow.",
            "Always believe in yourself.",
            "Be kind. Everyone’s fighting a battle you can’t see."
        ])
        return jsonify(build_response(advice))

    elif intent == "StoryIntent":
        story = "Once upon a time, there was a curious little robot who learned to talk like a human. And now, you're chatting with it!"
        return jsonify(build_response(story))

    elif intent == "MyBuddyIntent":
        return jsonify(build_response("Hey buddy! I'm here. What would you like to do — joke, story, advice, or just talk?"))

    else:
        return jsonify(build_response("Sorry, I didn't catch that. Try asking for a joke, a story, or some advice."))

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
