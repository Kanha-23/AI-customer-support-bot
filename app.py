from flask import Flask, request, jsonify, render_template, session, redirect
from agent import run_agent

app = Flask(__name__)
app.secret_key = "supersecret"


@app.route("/")
def home():
    if "customer_id" not in session:
        return redirect("/login")
    return render_template("chat.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        customer_id = request.form.get("customer_id")

        # store in session
        session["customer_id"] = customer_id
        session["session_data"] = {}

        return redirect("/")

    return render_template("login.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    session_data = session.get("session_data", {"messages": []}) # Ensure list exists
    customer_id = session.get("customer_id")

    response = run_agent(user_message, session_data, customer_id)

    session["session_data"] = session_data
    session.modified = True # Important for nested dictionaries/lists in sessions
    return jsonify({"response": response})

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)