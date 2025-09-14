from flask import Flask,render_template,request
app=Flask("__name__")

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/submit",methods=["GET","POST"])
def submit():
    username=request.form["username"]
    password=request.form["password"]

    valid_users={
        "prajakta":"123",
        "Jatin":"123456"
    }

    if username in valid_users and password==valid_users[username]:
        return render_template("welcome.html",name = username )
    else:
        return "Invalid credentials"