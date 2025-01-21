from flask import Flask, render_template, request

app = Flask(__name__)
posts = []

@app.route("/")
def index():
    return render_template("index.html", posts=posts)

@app.route("/new", methods=["GET", "POST"])
def new_post():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        posts.append({"title": title, "content": content})
        return render_template("index.html", posts=posts)
    return render_template("new.html")

app.run(debug=True)
