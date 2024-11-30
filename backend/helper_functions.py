import json
import os

# Filepath for the JSON file where posts will be stored
POSTS_FILE = 'posts.json'


def read_posts():
    """
    Reads the list of posts from the JSON file.

    Returns:
        list: A list of posts loaded from the file, or an empty list if the file does not exist or
              there is an error reading it.
    """
    if not os.path.exists(POSTS_FILE):
        return []

    try:
        with open(POSTS_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def write_posts(posts):
    """
    Writes the list of posts to the JSON file.

    Args:
        posts (list): A list of post data to be saved to the file.

    Raises:
        Exception: If there is an error writing to the file.
    """
    try:
        with open(POSTS_FILE, 'w') as f:
            json.dump(posts, f, indent=4)
    except IOError:
        raise Exception("Error writing to the posts file.")
