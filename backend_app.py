from flask import Flask

app = Flask(__name__)

@app.route("/login")
def login():
    return "Login Page"

@app.route("/")
def home():
    return "Backend App Running"

if __name__ == "__main__":
    app.run(port=9000)