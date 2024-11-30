from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
from helper_functions import read_posts, write_posts

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """
    Retrieve a list of all blog posts, optionally sorted by title, content, author, or date.

    Query parameters:
        - sort: The field to sort by (can be "title", "content", "author", or "date").
        - direction: The sort order, can be "asc" for ascending or "desc" for descending.

    Returns:
        - A list of posts, sorted according to the query parameters, or in their original order if no sorting is specified.
    """
    posts = read_posts()

    sort_field = request.args.get('sort', '').lower()
    direction = request.args.get('direction', '').lower()

    if sort_field and sort_field not in ['title', 'content', 'author', 'date']:
        return jsonify({"error": "Invalid sort field. Must be 'title', 'content', 'author', or 'date'."}), 400

    if direction and direction not in ['asc', 'desc']:
        return jsonify({"error": "Invalid direction. Must be 'asc' or 'desc'."}), 400

    if sort_field and direction:
        if sort_field == 'date':
            posts.sort(key=lambda post: datetime.strptime(post['date'], '%Y-%m-%d'), reverse=(direction == 'desc'))
        else:
            posts.sort(key=lambda post: post[sort_field].lower(), reverse=(direction == 'desc'))

    return jsonify(posts)


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """
    Search for blog posts by title, content, author, and/or date based on query parameters.

    Query Parameters:
        - title: Title to search for.
        - content: Content to search for.
        - author: Author to search for.
        - date: Date to search for.

    Returns:
        - A list of posts where title, content, author, or date matches the search term.
    """
    posts = read_posts()
    title_query = request.args.get('title', '').lower()
    content_query = request.args.get('content', '').lower()
    author_query = request.args.get('author', '').lower()
    date_query = request.args.get('date', '').lower()

    filtered_posts = [
        post for post in posts
        if title_query in post['title'].lower() or
        content_query in post['content'].lower() or
        author_query in post['author'].lower() or
        date_query in post['date'].lower()
    ]

    return jsonify(filtered_posts)


@app.route('/api/posts', methods=['POST'])
def add_post():
    """
    Add a new blog post.

    Expects JSON input in the format:
    {
        "title": "<title>",
        "content": "<content>",
        "author": "<author>",
    }

    Returns:
        - A JSON object representing the newly added post with a unique ID.
        - A 400 Bad Request error if title or content is missing.
        - A 201 Created status code if the post is successfully added.
    """
    data = request.get_json()

    title = data.get('title')
    content = data.get('content')
    author = data.get('author', 'Unknown Author')
    date = data.get('date', datetime.now().strftime('%Y-%m-%d'))

    if not title or not content:
        return jsonify({"error": "Missing required data: title, or content."}), 400

    posts = read_posts()

    new_post = {
        "id": max(post["id"] for post in posts) + 1 if posts else 1,
        "title": title,
        "content": content,
        "author": author,
        "date": date
    }
    posts.append(new_post)
    write_posts(posts)

    return jsonify(new_post), 201


@app.route('/api/posts/<int:post_id>', methods=['GET'])
def get_single_post(post_id):
    """
    Retrieve a single blog post by its ID.

    Args:
        post_id (int): The ID of the post to retrieve.

    Returns:
        - The post with the specified ID if found.
        - A 404 Not Found error if no post with the given ID exists.
    """
    posts = read_posts()

    post = next((post for post in posts if post['id'] == post_id), None)

    if post:
        return jsonify(post), 200
    else:
        return jsonify({"error": f"Post with ID {post_id} not found."}), 404


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """
    Delete a blog post by its ID.

    Args:
        post_id (int): The ID of the post to delete.

    Returns:
        - A success message if the post is deleted.
        - A 404 Not Found error if the post with the given ID does not exist.
    """
    posts = read_posts()
    post_to_delete = next((post for post in posts if post['id'] == post_id), None)

    if post_to_delete is None:
        return jsonify({"error": f"Post with id {post_id} not found."}), 404

    posts.remove(post_to_delete)
    write_posts(posts)

    return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 200


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """
    Update an existing blog post with new data.

    Expected JSON input:
    {
        "title": "<new_title>",
        "content": "<new content>",
        "author": "<new author>",
        "date": "<new date>"  # Optional; must be in 'YYYY-MM-DD' format
    }

    Returns:
        - The updated post details if the post is successfully updated.
        - A 404 Not Found error if no post with the given ID exists.
        - A 400 Bad Request error if the date format is incorrect.
    """
    data = request.get_json()

    posts = read_posts()
    post = next((post for post in posts if post['id'] == post_id), None)
    if not post:
        return jsonify({"error": f"Post with id {post_id} not found"}), 404

    if "date" in data:
        try:
            datetime.strptime(data["date"], '%Y-%m-%d')
        except ValueError:
            return jsonify({"error": "Invalid date format. Use 'YYYY-MM-DD'"}), 400

    post["title"] = data.get("title", post["title"])
    post["content"] = data.get("content", post["content"])
    post["author"] = data.get("author", post["author"])
    post["date"] = data.get("date", post["date"])

    write_posts(posts)

    return jsonify(post), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
