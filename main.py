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
