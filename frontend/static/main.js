// Function that runs once the window is fully loaded
window.onload = function() {
    // Attempt to retrieve the API base URL from the local storage
    var savedBaseUrl = localStorage.getItem('apiBaseUrl');
    // If a base URL is found in local storage, load the posts
    if (savedBaseUrl) {
        document.getElementById('api-base-url').value = savedBaseUrl;
        loadPosts();
    }
}

// Function to fetch all the posts from the API and display them on the page
function loadPosts() {
    // Retrieve the base URL from the input field and save it to local storage
    var baseUrl = document.getElementById('api-base-url').value;
    localStorage.setItem('apiBaseUrl', baseUrl);

    // Use the Fetch API to send a GET request to the /posts endpoint
    fetch(baseUrl + '/posts')
        .then(response => response.json())  // Parse the JSON data from the response
        .then(data => {  // Once the data is ready, we can use it
            console.log("Posts fetched:", data); // Log to ensure we are getting the data

            // Clear out the post container first
            const postContainer = document.getElementById('post-container');
            postContainer.innerHTML = '';

            // For each post in the response, create a new post element and add it to the page
            data.forEach(post => {
                const postDiv = document.createElement('div');
                postDiv.className = 'post';
                postDiv.innerHTML = `
                    <h2>${post.title}</h2>
                    <p>${post.content}</p>
                    <p><b>Author:</b> ${post.author}</p>
                    <p><b>Date:</b> ${post.date}</p>
                    <div class="post-buttons">
                        <button class="delete-btn" onclick="deletePost(${post.id})">Delete</button>
                        <button class="edit-btn" onclick="editPost(${post.id})">Edit</button>
                    </div>`;
                postContainer.appendChild(postDiv);
            });

            // Show the "Add Post" form again after posts are loaded
            document.getElementById('add-post-container').style.display = 'block';
            document.getElementById('edit-post-container').style.display = 'none';
            document.getElementById('post-container').style.display = 'block';
        })
        .catch(error => console.error('Error:', error));  // If an error occurs, log it to the console
}

// Function to send a POST request to the API to add a new post
function addPost() {
    var baseUrl = document.getElementById('api-base-url').value;
    var postTitle = document.getElementById('post-title').value;
    var postContent = document.getElementById('post-content').value;
    var postAuthor = document.getElementById('post-author').value || "Unknown author";
    var postDate = document.getElementById('post-date').value;

    let postPayload = {
        title: postTitle,
        content: postContent,
        author: postAuthor
    };

    if (postDate) {
        postPayload.date = postDate;
    }

    fetch(baseUrl + '/posts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(postPayload)
    })
    .then(response => response.json())
    .then(post => {
        console.log('Post added:', post);
        loadPosts(); // Reload the posts after adding a new one
    })
    .catch(error => console.error('Error:', error));  // If an error occurs, log it to the console
}

// Function to send a DELETE request to the API to delete a post
function deletePost(postId) {
    var baseUrl = document.getElementById('api-base-url').value;

    fetch(baseUrl + '/posts/' + postId, {
        method: 'DELETE'
    })
    .then(response => {
        console.log('Post deleted:', postId);
        loadPosts(); // Reload the posts after deleting one
    })
    .catch(error => console.error('Error:', error));  // If an error occurs, log it to the console
}

// Function to populate the edit form with the current post data
function editPost(postID) {
    var baseUrl = document.getElementById('api-base-url').value;

    fetch(baseUrl + '/posts/' + postID)
        .then(response => response.json())
        .then(post => {
            document.getElementById('update-title').value = post.title;
            document.getElementById('update-content').value = post.content;
            document.getElementById('update-author').value = post.author;
            document.getElementById('update-date').value = post.date;
            document.getElementById('update-post-id').value = post.id;

            // Hide the "Add Post" form and show the "Edit Post" form
            document.getElementById('add-post-container').style.display = 'none';
            document.getElementById('edit-post-container').style.display = 'block';
            document.getElementById('post-container').style.display = 'none';
        })
        .catch(error => console.error('Error:', error));
}

// Function to send a PUT request to the API to update the post
function updatePost() {
    var baseUrl = document.getElementById('api-base-url').value;
    var postID = document.getElementById('update-post-id').value;
    var postTitle = document.getElementById('update-title').value;
    var postContent = document.getElementById('update-content').value;
    var postAuthor = document.getElementById('update-author').value || "Unknown author";
    var postDate = document.getElementById('update-date').value;

    let updatedData = {
        title: postTitle,
        content: postContent,
        author: postAuthor
    };

    if (postDate) {
        updatedData.date = postDate;
    }

    fetch(baseUrl + '/posts/' + postID, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updatedData)
    })
    .then(response => response.json())
    .then(post => {
        console.log('Post updated:', post);
        loadPosts(); // Reload the posts after updating
    })
    .catch(error => console.error('Error:', error));
}

// Function to cancel editing and go back to the main view
function cancelEdit() {
    document.getElementById('add-post-container').style.display = 'block';
    document.getElementById('edit-post-container').style.display = 'none';
    document.getElementById('post-container').style.display = 'block';
}
