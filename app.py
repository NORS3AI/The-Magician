#!/usr/bin/env python3
"""
The-Magician: Web Interface
Flask server for playing the game in a browser.
"""

from flask import Flask, render_template, request, redirect, url_for, session
import secrets
import json
from pathlib import Path

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

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
            # Demo mode - accept any credentials
            session["username"] = username
            session["logged_in"] = True
            return redirect(url_for("character_select"))
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

        errors = []
        if len(username) < 3:
            errors.append("Username must be at least 3 characters")
        if "@" not in email:
            errors.append("Please enter a valid email")
        if len(password) < 8:
            errors.append("Password must be at least 8 characters")

        if errors:
            return render_template("register.html", errors=errors)

        # Demo mode - accept registration
        session["username"] = username
        session["logged_in"] = True
        return redirect(url_for("character_select"))

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


@app.route("/logout")
def logout():
    """Logout and clear session."""
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    print("=" * 60)
    print("  THE MAGICIAN - Web Interface")
    print("  Open in browser: http://localhost:5000")
    print("=" * 60)
    app.run(host="0.0.0.0", port=5000, debug=True)
