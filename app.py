from flask import Flask, render_template, request, url_for, redirect
import json

app = Flask(__name__)

@app.route('/')
def index():
    with open("data.json", "r") as fileobj:
        blog_posts = json.load(fileobj)

    return render_template("index.html", posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        new_post_data = {
            "author": request.form.get("author"),
            "title": request.form.get("title"),
            "content": request.form.get("content")
        }

        with open("data.json", "r") as fileobj:
            blog_posts = json.load(fileobj)

        new_post_data["id"] = len(blog_posts) + 1

        blog_posts.append(new_post_data)

        with open("data.json", "w") as fileobj:
            json.dump(blog_posts, fileobj, indent=4)
        return redirect(url_for("index"))
    return render_template("add.html")


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    with open('data.json', 'r') as fileobj:
        blog_posts = json.load(fileobj)

    new_blog_posts = [post for post in blog_posts if post['id'] != post_id]

    with open("data.json", "w") as fileobj:
        json.dump(new_blog_posts, fileobj, indent=4)

    return redirect(url_for("index"))


def fetch_post_by_id(post_id):
    """Searches for a post using its ID in the JSON file."""
    with open("data.json", "r") as fileobj:
        blog_posts = json.load(fileobj)

    for post in blog_posts:
        if post["id"] == post_id:
            return post
    return None


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    post = fetch_post_by_id(post_id)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        with open('data.json', 'r') as fileobj:
            blog_posts = json.load(fileobj)

        for post in blog_posts:
            if post["id"] == post_id:
                post["author"] = request.form.get("new_author")
                post["title"] = request.form.get("new_title")
                post["content"] = request.form.get("new_content")
                break
        with open("data.json", "w") as fileobj:
            json.dump(blog_posts, fileobj, indent=4)

        return redirect(url_for("index"))

    return render_template("update.html", post=post)


@app.route('/like/<int:post_id>', methods=['POST'])
def like(post_id):
    with open('data.json', 'r') as fileobj:
        blog_posts = json.load(fileobj)

    for post in blog_posts:
        if post['id'] == post_id:
            post['likes'] = post.get('likes', 0) + 1
            break

    with open('data.json', 'w') as fileobj:
        json.dump(blog_posts, fileobj, indent=4)

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
