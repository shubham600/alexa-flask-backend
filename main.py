intent = None
session_id = data.get("session", {}).get("user", {}).get("userId", "anonymous")

# Handle LaunchRequest (when user opens the skill without saying anything)
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

        responses = {
            "moon": "The moon is Earth’s only natural satellite. It controls tides and lights the night sky.",
            "cat": "Cats are small carnivorous mammals known for agility, curiosity, and purring.",
            "ai": "AI stands for Artificial Intelligence, which allows machines to think and learn like humans.",
            "sun": "The sun is a massive ball of gas that provides light and heat to our solar system."
        }

        answer = "Hmm, I’m still learning! But that’s an interesting question."
        for key in responses:
            if key in question.lower():
                answer = responses[key]

        return jsonify(build_response(answer))

# Fallback response
return jsonify(build_response("Sorry, I didn’t understand that. Try asking in a different way!"))
