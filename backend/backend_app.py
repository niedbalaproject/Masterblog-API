from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post", "author": "Sara Black", "date": "2023-05-20"},
    {"id": 2, "title": "Second post", "content": "This is the second post.", "author": "Jane Smith", "date": "2023-06-25"},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """
    Return the list of all blog posts, optionally sorted by title, content, author, or date.

    Query parameters:
        - sort: The field tp sort by, can be "title", "content", "author", or "date".
        - direction: The sort order, can be "asc" for ascending or "desc" for descending.

    If no sort parameters are provided, the posts are returned in their original order.
    """
    # Get the sort and direction parameters from the request
    sort_field = request.args.get('sort', '').lower()  # default to empty string if not provided
    direction = request.args.get('direction', '').lower()

    # Validate sort_field and direction
    valid_sort_fields = ['title', 'content', 'author', 'date']
    if sort_field and sort_field not in valid_sort_fields:
        return jsonify({"error": f"Invalid sort field. Must be one of {valid_sort_fields}."}), 400

    if direction and direction not in ['asc', 'desc']:
        return jsonify({"error": "Invalid direction. Must be 'asc' or 'desc'."}), 400

    # Sort the posts if sort and direction are provided
    if sort_field and direction:
        reverse = direction == 'desc'

        # Handle date sorting by converting date string to datetime object
        if sort_field == 'date':
            POSTS.sort(key=lambda post: datetime.strptime(post[sort_field], "%Y-%m-%d"), reverse=reverse)
        else:
            POSTS.sort(key=lambda post: post[sort_field].lower(), reverse=reverse)

    # return the posts
    return jsonify(POSTS), 200


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """
    Searches for blog posts by title, content, author, or date based on query parameters.
    :return: A list of posts where the title or content matches the search term.
    """
    # Get the search parameters from the request
    title_query = request.args.get('title', '').lower()  # default to empty string if not provided
    content_query = request.args.get('content', '').lower()
    author_query = request.args.get('author', '').lower()
    date_query = request.args.get('date', '')

    # Filter posts based on title or content
    filtered_posts = [
        post for post in POSTS if (
            title_query in post['title'].lower() or
            content_query in post['content'].lower() or
            author_query in post['author'].lower() or
            date_query in post['date']
        )]

    return jsonify(filtered_posts), 200


@app.route('/api/posts', methods=['POST'])
def add_post():
    """
    Add a new blog post.
    The endpoint expects a JSON object in the request body with the keys:
        - title: The title of the new post (required).
        - content: The content of the new post (required).
        - author: The author of the new post.
        - date: The date of the new post.
    :return:
        - A JSON object representing the newly added post with a unique ID.
        - A 400 Bad Request error if title or content is missing.
        - A 201 Created status code if the post is successfully added.
    """
    data = request.get_json()

    # Input validation
    if not data or not data.get("title") or not data.get("content") or not data.get('author') or not data.get('date'):
        return jsonify({"message": "Missing required fields."}), 400

    try:
        # ensure the date is in the correct format
        datetime.strptime(data['date'], "%Y-%m-%d")
    except ValueError:
        return jsonify({"message": "Invalid date format, use YYYY-MM-DD"}), 400

    # Create the new post
    new_post = {
        "id": len(POSTS) + 1,
        "title": data["title"],
        "content": data["content"],
        "author": data['author'],
        "date": data['date']
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
    Update an existing blog post. Only 'title', 'content', 'author', and 'date' are allowed.
    :return:
        JSON object with the updated post details or an error message.
        - Status 200 OK: Post updated successfully.
        - Status 404 Not Found: If the post with the given ID does not exist.
    """
    post_to_update = next((post for post in POSTS if post['id'] == post_id), None)
    if post_to_update is None:
        return jsonify({"error": f"Post with id {post_id} not found."}), 404

    data = request.get_json()

    # Update fields if present in the request
    if 'title' in data:
        post_to_update['title'] = data['title']
    if 'content' in data:
        post_to_update['content'] = data['content']
    if 'author' in data:
        post_to_update['author'] = data['author']
    if 'date' in data:
        try:
            # Ensure the data is in the correct format
            datetime.strptime(data['date'], "%Y-%m-%d")
            post_to_update['date'] = data['date']
        except ValueError:
            return jsonify({"message": "Invalid date format, use YYYY-MM-DD"}), 400

    return jsonify(post_to_update), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
