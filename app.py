from flask import Flask, request, render_template, send_from_directory, jsonify
from pathlib import Path
import os, json
from functions import *

POST_PATH = "posts.json"
UPLOAD_FOLDER = os.path.join("uploads", "images")

app = Flask(__name__, static_folder="static")
app.config['JSON_AS_ASCII'] = False

@app.route("/")
def page_index():
    posts = read_json(POST_PATH)
    tags = get_all_tags(posts)
    return render_template("index.html", tags=tags)


@app.route("/tag")
def page_tag():
    tag = request.args.get("tag")
    posts = read_json(POST_PATH)
    tag_posts = get_posts_by_tags(tag, posts)
    return render_template("post_by_tag.html", tag=tag, posts=tag_posts)


@app.route("/post", methods=["GET", "POST"])
def page_post_create():
    if request.method == "GET":
        return render_template("post_form.html")
    if request.method == "POST":
        file = request.files['picture']
        if file.filename == '':
            return "ошибка загрузки"
        path = Path(os.path.abspath(__file__)).parent
        file.save(path.joinpath(UPLOAD_FOLDER, file.filename))
        content = request.form.get("content")

        pic_path = "uploads/" + file.filename
        add_post(POST_PATH, {"pic": pic_path, "content": content})

        return render_template("post_uploaded.html", path=pic_path, content=content)


@app.route("/uploads/<path:path>")
def static_dir(path):
    return send_from_directory(UPLOAD_FOLDER, path)


if __name__ == "__main__":
    os.chdir(Path(os.path.abspath(__file__)).parent)
    app.run()

