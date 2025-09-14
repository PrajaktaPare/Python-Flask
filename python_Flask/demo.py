# from flask import Flask
# app=   Flask(__name__)

# @app.route("/")
# def home ():
#     return "Hello"



from flask import Flask,redirect,Response, url_for,request,session

app=Flask(__name__)
app.secret_key = "super_secret_123456"


@app.route("/",methods=["GET","POST"])
def login():
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        if username=="admin" and password=="123":
            session["user"]=username
            return redirect(url_for("welcome")) 
        else:
            return Response("Invalid-credentials ",mimetype="text/plain")
    return '''
            
            <h3>Login</h3>
            <form method="POST">
            username:<input type="text" name="username"><br>
            password:<input type="password" name="password"><br>
             <input type="submit" value="login">
            </form>




'''


@app.route("/welcome")
def welcome():
    if "user" in session:
        print("DEBUG → Session contains:", session["user"])
        return f'''
        <h2>welcome,{session["user"]}!</h2>
        <a href={url_for("logout")} >logout</a>'''
    return redirect(url_for("login"))



@app.route("/logout")
def logout():
    session.pop("user",None)
    return redirect(url_for("login"))

