from flask import Flask, request

app = Flask(__name__)


@app.route("/", methods=["GET"])
def kek():
    if request.method == 'GET':
        return "Hello! Please, give me my mail...\n"


@app.route("/robots.txt", methods=["GET"])
def robots():
    return "User-agent: *\nDisallow: /postbox\n"


@app.route("/postbox", methods=["POST"])
def postbox():
    if request.method == 'POST':
        return "Thanks! kks{thanks_f0r_m@1l}\n"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
