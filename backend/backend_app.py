from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """
    Retrieve all blog posts.
    :return: A JSON response containing the list of all blog posts.
    """
    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add_post():
    """
    Add a new blog post.
    The endpoint expects a JSON object in the request body with the keys:
        - title: The title of the new post (required).
        - content: The content of the new post (required).
    :return:
        - A JSON object representing the newly added post with a unique ID.
        - A 400 Bad Request error if title or content is missing.
        - A 201 Created status code if the post is successfully added.
    """
    data = request.get_json()

    # Input validation
    if not data or not data.get("title") or not data.get("content"):
        return jsonify({"error": "Both 'title' amd 'content' are required."}), 400

    # Generate a unique ID
    new_id = max(post['id'] for post in POSTS) + 1 if POSTS else 1

    # Create the new post
    new_post = {
        "id": new_id,
        "title": data["title"],
        "content": data["content"],
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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
