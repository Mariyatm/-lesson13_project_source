import json


def is_tag(word):
    return word.startswith("#")


def get_tag(word):
    return word.replace("#","").replace("!","")


def read_json(path):
    with open(path, "r") as f:
        data = json.load(f)
    return data


def get_all_tags(posts):
    tags = set()
    for post in posts:
        for word in post["content"].split():
            if is_tag(word):
                tags.add(get_tag(word))
    return tags


def get_posts_by_tags(tag, posts):
    tag_posts = []
    for post in posts:
        if "#" + tag in post["content"]:
            tag_posts.append(post)
    return  tag_posts


def add_post(path, post):
    posts = read_json(path)
    with open(path, "w") as f:
        posts.append(post)
        json.dump(posts, f, ensure_ascii=False, indent=4)
