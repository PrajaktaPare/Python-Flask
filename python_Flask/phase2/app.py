from flask import Flask,render_template

app=Flask("__name__")

@app.route("/")
def jinja():
    return render_template("jinja.html",name="prajakta",is_topper=True,subjects=['maths','science'])