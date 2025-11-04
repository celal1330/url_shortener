"""
TinyURL-ish Flask App
Just a small side project to shorten URLs — nothing fancy.
"""

from flask import Flask, render_template, request, redirect, jsonify
import os, json, random, string
from datetime import datetime

app = Flask(__name__)

# TODO: Maybe move to a DB later? For now let's just keep it simple.
DATA_FILE = "urls.json"

def read_data():
    # reads the JSON file (if it exists)
    if os.path.isfile(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except Exception as e:
                print("Error reading file:", e)
                return {}
    return {}

def write_data(data):
    # overwrites the file completely each time
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def make_code(length=6):
    # NOTE: This could probably use uuid or hash, but random is fine for now
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))

@app.route("/")
def home():
    # Main landing page — just shows the form
    return render_template("index.html")

@app.route("/shorten", methods=["POST"])
def create_short():
    url = request.form.get("url")
    custom = request.form.get("custom_code", "").strip()

    if not url:
        return jsonify({"error": "Please provide a URL."}), 400

    data = read_data()

    # Handle custom code if provided
    if custom:
        if custom in data:
            # Already exists, not good
            return jsonify({"error": "That short code already exists."}), 400
        code = custom
    else:
        # Generate until we get a unique one (probably fine for small scale)
        code = make_code()
        while code in data:
            code = make_code()

    # just in case someone reuses the same URL — don’t overthink this
    data[code] = {
        "original_url": url,
        "created_at": datetime.now().isoformat(),
        "clicks": 0
    }

    write_data(data)

    # Construct the full short URL
    short_link = request.host_url + code
    return jsonify({
        "short_url": short_link,
        "short_code": code,
        "original_url": url
    })

@app.route("/<code>")
def go_to_url(code):
    urls = read_data()
    if code in urls:
        urls[code]["clicks"] = urls[code].get("clicks", 0) + 1  # probably safe
        write_data(urls)
        return redirect(urls[code]["original_url"])
    else:
        # Maybe log this later
        return render_template("404.html"), 404

@app.route("/stats/<code>")
def stats(code):
    all_data = read_data()
    entry = all_data.get(code)
    if not entry:
        return jsonify({"error": "Short code not found"}), 404

    return jsonify({
        "short_code": code,
        "original_url": entry["original_url"],
        "created_at": entry["created_at"],
        "clicks": entry["clicks"]
    })

@app.route("/api/all")
def list_all():
    # Might remove this in production — too open
    everything = read_data()
    return jsonify(everything)

if __name__ == "__main__":
    # Note: debug mode ON, don’t forget to turn off later!
    app.run(debug=True, port=5000)
