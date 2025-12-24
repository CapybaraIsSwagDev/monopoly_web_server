from flask import Flask, request, jsonify
import random
import string
import time

app = Flask(__name__)

lobbies = {}  # code -> {ip, port, timestamp}

def generate_code():
    chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    return "".join(random.choice(chars) for _ in range(5))

@app.route("/host", methods=["POST"])
def host():
    code = generate_code()
    ip = request.remote_addr
    port = request.json.get("port")

    lobbies[code] = {
        "ip": ip,
        "port": port,
        "time": time.time()
    }

    return jsonify({"code": code})

@app.route("/join")
def join():
    code = request.args.get("code")
    lobby = lobbies.get(code)

    if not lobby:
        return jsonify({"error": "Invalid code"}), 404

    return jsonify({
        "ip": lobby["ip"],
        "port": lobby["port"]
    })

@app.route("/")
def health():
    return "Lobby server running"

if __name__ == "__main__":
    app.run()
