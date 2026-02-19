from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta
from pydantic import BaseModel
import os

from query import query
from db import insert_data


# ----------------------------
# Flask App Configuration
# ----------------------------
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret") 

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=False, 
    SESSION_COOKIE_SAMESITE="Lax",
)
app.permanent_session_lifetime = timedelta(days=7)


# ----------------------------
# Constants & Models
# ----------------------------
SYSTEM_PROMPT = (
    "You are AbariBot, an assistant. "
    "Only answer questions related to Abari. "
    "You are linked to a vector database about Abari. "
    "Do not answer unrelated questions. User question: "
)


class Prompt(BaseModel):
    prompt: str
    info: str


# ----------------------------
# Routes
# ----------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_message = request.form.get("user_message", "").strip()
        if not user_message:
            return redirect(url_for("index"))

        # Build and query prompt
        full_prompt = SYSTEM_PROMPT + user_message
        bot_response = query(full_prompt)

        # Update session conversation
        conversation = session.get("conversation", [])
        conversation.append({"user": user_message, "bot": bot_response})
        session["conversation"] = conversation
        session.permanent = True  # Keep session alive

        # Store interaction in database
        insert_data(Prompt(prompt=user_message, info=bot_response))

        return redirect(url_for("index"))

    # GET request
    return render_template("abariBotBis.html", conversation=session.get("conversation", []))


# ----------------------------
# Main Entry Point
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True)
