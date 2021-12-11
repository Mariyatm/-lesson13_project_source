from flask import Flask, request, render_template, send_from_directory, jsonify
from pathlib import Path
import os, json
from functions import is_tag, get_tag

POST_PATH = "posts.json"
UPLOAD_FOLDER = os.path.join("uploads", "images")

app = Flask(__name__, static_folder="static")
app.config['JSON_AS_ASCII'] = False

@app.route("/")
def page_index():
    with open(POST_PATH, "r") as f:
        posts = json.load(f)
    tags = set()
    for post in posts:
        for word in post["content"].split():
            if is_tag(word):
                tags.add(get_tag(word))
    return render_template("index.html", tags=tags)


@app.route("/tag")
def page_tag():
    tag = request.args.get("tag")
    with open(POST_PATH, "r") as f:
        posts = json.load(f)
    tag_posts = []
    for post in posts:
        if "#"+tag in post["content"]:
            tag_posts.append(post)
    print(tag_posts)
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

        pic_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(POST_PATH, "r") as f:
            posts = json.load(f)
        with open(POST_PATH, "w") as f:
            posts.append({"pic": pic_path, "content": content})
            json.dump(posts, f, ensure_ascii=False, indent=4)

        return render_template("post_uploaded.html", path=pic_path, content=content)


@app.route("/uploads/<path:path>")
def static_dir(path):
    return send_from_directory("uploads", path)


if __name__ == "__main__":
    os.chdir(Path(os.path.abspath(__file__)).parent)
    app.run()

