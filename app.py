#!/usr/bin/env python3
"""
The-Magician: Web Interface
Flask server for playing the game in a browser.
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
import secrets
import json
import logging
from pathlib import Path

from src.auth import AccountManager
from src.config.settings import Settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# Load configuration
config = Settings()

# Initialize account manager
account_manager = AccountManager()

# Load character data
DATA_DIR = Path(__file__).parent / "data"


def load_character_data(character: str) -> dict:
    """Load character base data."""
    char_file = DATA_DIR / "characters" / f"{character}_base.json"
    if char_file.exists():
        with open(char_file) as f:
            return json.load(f)
    return {}


@app.route("/")
def index():
    """Main menu."""
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login page."""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if username and password:
            # Use authentication system
            success, message, session_token = account_manager.login(username, password)

            if success:
                session["username"] = username
                session["session_token"] = session_token
                session["logged_in"] = True
                return redirect(url_for("character_select"))
            else:
                return render_template("login.html", error=message)
        else:
            return render_template("login.html", error="Please enter username and password")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Registration page."""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        # Use authentication system
        success, message, user_data = account_manager.register(username, email, password)

        if success:
            # Auto-login after registration
            success_login, _, session_token = account_manager.login(username, password)
            if success_login:
                session["username"] = username
                session["session_token"] = session_token
                session["logged_in"] = True
                return redirect(url_for("character_select"))
        else:
            return render_template("register.html", errors=[message])

    return render_template("register.html")


@app.route("/character-select", methods=["GET", "POST"])
def character_select():
    """Character/path selection."""
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    if request.method == "POST":
        character = request.form.get("character")
        if character in ["tomas", "pug"]:
            session["character"] = character
            session["character_data"] = load_character_data(character)
            return redirect(url_for("play"))

    return render_template("character_select.html", username=session.get("username"))


@app.route("/play", methods=["GET", "POST"])
def play():
    """Main gameplay."""
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    if not session.get("character"):
        return redirect(url_for("character_select"))

    character = session.get("character")
    character_data = session.get("character_data", {})
    message = None

    if request.method == "POST":
        command = request.form.get("command", "").strip().lower()

        if command == "help":
            message = "Available commands: look, inventory, stats, help, menu"
        elif command == "look":
            if character == "tomas":
                message = "You stand in the courtyard of Castle Crydee. The sound of wooden practice swords clashing echoes from the training grounds. Swordmaster Fannon is drilling the soldiers."
            else:
                message = "You are in Kulgan's study, surrounded by books and scrolls. The smell of old parchment fills the air. Your master is away, giving you time to practice your cantrips."
        elif command == "inventory":
            items = character_data.get("starting_inventory", [])
            item_list = ", ".join([f"{i['item']} x{i['quantity']}" for i in items])
            message = f"Inventory: {item_list}"
        elif command == "stats":
            stats = character_data.get("base_stats", {})
            stat_list = ", ".join([f"{k.title()}: {v}" for k, v in stats.items()])
            message = f"Stats: {stat_list}"
        elif command == "menu":
            return redirect(url_for("index"))
        else:
            message = f"Unknown command: '{command}'. Type 'help' for available commands."

    return render_template(
        "play.html",
        character=character,
        character_data=character_data,
        username=session.get("username"),
        message=message
    )


@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    """Request password reset."""
    if request.method == "POST":
        email = request.form.get("email", "").strip()

        if email:
            # Generate reset URL (will be used in email)
            reset_url = url_for("reset_password", _external=True)
            success, message = account_manager.request_password_reset(email, reset_url)

            return render_template("forgot_password.html", success=message)
        else:
            return render_template("forgot_password.html", error="Please enter your email")

    return render_template("forgot_password.html")


@app.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    """Reset password with token."""
    if request.method == "POST":
        token = request.form.get("token", "").strip()
        new_password = request.form.get("new_password", "").strip()
        confirm_password = request.form.get("confirm_password", "").strip()

        if new_password != confirm_password:
            return render_template("reset_password.html", error="Passwords do not match", token=token)

        success, message = account_manager.reset_password(token, new_password)

        if success:
            return render_template("reset_password.html", success=message)
        else:
            return render_template("reset_password.html", error=message, token=token)

    # GET request - show form with token from URL
    token = request.args.get("token", "")
    return render_template("reset_password.html", token=token)


@app.route("/forgot-username", methods=["GET", "POST"])
def forgot_username():
    """Request username reminder."""
    if request.method == "POST":
        email = request.form.get("email", "").strip()

        if email:
            success, message = account_manager.request_username_reminder(email)
            return render_template("forgot_username.html", success=message)
        else:
            return render_template("forgot_username.html", error="Please enter your email")

    return render_template("forgot_username.html")


@app.route("/logout")
def logout():
    """Logout and clear session."""
    # Invalidate session token if exists
    if "username" in session and "session_token" in session:
        account_manager.logout(session["username"], session["session_token"])

    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    print("=" * 60)
    print("  THE MAGICIAN - Web Interface")
    print("  Open in browser: http://localhost:5000")
    print("=" * 60)
    app.run(host="0.0.0.0", port=5000, debug=True)
