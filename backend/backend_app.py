from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post.", "author": "Alice", "date": "2023-06-01"},
    {"id": 2, "title": "Second post", "content": "This is the second post.", "author": "Bob", "date": "2023-06-02"},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """
    Return the list of all blog posts, optionally sorted by title, content, author, or date.

    Query parameters:
        - sort: The field to sort by, can be "title", "content", "author", or "date".
        - direction: The sort order, can be "asc" for ascending or "desc" for descending.

    If no sort parameters are provided, the posts are returned in their original order.
    """
    # Get the sort and direction parameters from the request
    sort_field = request.args.get('sort', '').lower()  # default to empty string if not provided
    direction = request.args.get('direction', '').lower()

    # Validate sort_field and direction
    if sort_field and sort_field not in ['title', 'content', 'author', 'date']:
        return jsonify({"error": "Invalid sort field. Must be 'title', 'content', 'author', or 'date'."}), 400

    if direction and direction not in ['asc', 'desc']:
        return jsonify({"error": "Invalid direction. Must be 'asc' or 'desc'."}), 400

    # Sort the posts if sort and direction are provided
    if sort_field and direction:
        if sort_field == 'date':
            POSTS.sort(key=lambda post: datetime.strptime(post['date'], '%Y-%m-%d'), reverse=True)
        else:
            POSTS.sort(key=lambda post: post[sort_field].lower(), reverse=True)

    # return the posts
    return jsonify(POSTS)


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """
    Searches for blog posts by title, content, author, and/or date based on query parameters.
    Query Parameters:
        - title: The title to search for.
        - content: The content to search for.
        - author: The author to search for.
        - date: The date to search for.
    :return: A list of posts where the title, content, author, or date matches the search term.
    """
    # Get the search parameters from the request
    title_query = request.args.get('title', '').lower()  # default to empty string if not provided
    content_query = request.args.get('content', '').lower()
    author_query = request.args.get('author', '').lower()
    date_query = request.args.get('date', '').lower()

    # Filter posts based on title, content, author, or date
    filtered_posts = [
        post for post in POSTS
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
    Expects JSON input:
    {
        "title": "<title>",
        "content": "<content>",
        "author": "<author>",
    }
    :return:
        - A JSON object representing the newly added post with a unique ID.
        - A 400 Bad Request error if title or content is missing.
        - A 201 Created status code if the post is successfully added.
    """
    data = request.get_json()

    # Check if the required fields are in the request
    title = data.get('title')
    content = data.get('content')
    author = data.get('author', 'Unknown Author')  # Default to 'Unknown Author' if not provided
    date = data.get('date', datetime.now().strftime('%Y-%m-%d'))

    # Input validation
    if not title or not content:
        return jsonify({"error": "Missing required data: title, or content."}), 400

    # Create the new post
    new_post = {
        "id": max(post["id"] for post in POSTS) + 1 if POSTS else 1,
        "title": title,
        "content": content,
        "author": author,
        "date": date
    }
    POSTS.append(new_post)

    # Return the new post with a 201 Created status
    return jsonify(new_post), 201


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """
    Delete a blog post by its ID.
    :param post_id: (int): The ID of the new post to delete, provided in the URL.
    :return:
        - A JSON response with a success message and a 200 OK status if the post exists
        and is deleted.
        - A 404 Not Found error if no post with the given ID exists.
    """
    # Find the post by ID
    post_to_delete = next((post for post in POSTS if post['id'] == post_id), None)

    if post_to_delete is None:
        # Return a 404 error, if no post is found
        return jsonify({"error": f"Post with id {post_id} not found."}), 404

    # Remove the post from the list
    POSTS.remove(post_to_delete)

    # Return a success message with a 200 OK status
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
    :return:
        JSON object with the updated post details or an error message.
        - Status 200 OK: Post updated successfully.
        - Status 404 Not Found: If the post with the given ID does not exist.
    """
    data = request.get_json()

    # Find the post by id
    post = next((post for post in POSTS if post['id'] == post_id), None)
    if not post:
        return jsonify({"error": f"Post with id {post_id} not found"}), 404

    # Validate date format if provided
    if "date" in data:
        try:
            datetime.strptime(data["date"], '%Y-%m-%d')
        except ValueError:
            return jsonify({"error": "Invalid date format. Use 'YYYY-MM-DD"}), 400

    # Update the fields (retain current values if not provided)
    post["title"] = data.get("title", post["title"])
    post["content"] = data.get("content", post["content"])
    post["author"] = data.get("author", post["author"])
    post["date"] = data.get("date", post["date"])

    return jsonify(post), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
