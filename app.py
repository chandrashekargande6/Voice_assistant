from flask import Flask, request, jsonify, render_template
from groq import Groq

app = Flask(__name__)

# Initialize Groq client with your API key
client = Groq(api_key="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")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"response": "⚠️ Please provide a message."})

    try:
        # Call Groq API
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # fast + free-tier friendly model
            messages=[{"role": "user", "content": user_message}]
        )

        ai_message = response.choices[0].message.content
        return jsonify({"response": ai_message})

    except Exception as e:
        return jsonify({"response": f"⚠️ Error: {str(e)}"})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))  # Render gives PORT automatically
    app.run(host="0.0.0.0", port=port, debug=True)
