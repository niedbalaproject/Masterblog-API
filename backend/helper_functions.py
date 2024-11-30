import json
import os

# Filepath for the JSON file where posts will be stored
POSTS_FILE = 'posts.json'


# Function to read the posts from the JSON file
def read_posts():
    # If the file does not exist, return an empty list
    if not os.path.exists(POSTS_FILE):
        return []

    try:
        with open(POSTS_FILE, 'r') as f:
            # Load the JSON data from the file
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        # If there's an error reading or decoding the file, return an empty list
        return []


# Function to write posts to the JSON file
def write_posts(posts):
    try:
        with open(POSTS_FILE, 'w') as f:
            # Write the posts list as JSON data to the file
            json.dump(posts, f, indent=4)
    except IOError:
        # If there's an error writing to the file, raise an exception
        raise Exception("Error writing to the posts file.")
