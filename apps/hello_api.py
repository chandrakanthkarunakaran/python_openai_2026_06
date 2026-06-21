"""Minimal Flask Hello World API."""

from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/")
def hello():
    return jsonify({"message": "Hello, World!"})


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
