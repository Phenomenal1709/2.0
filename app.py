import streamlit as st
from urllib.parse import urlparse
import requests
import os

# GitHub personal access token (replace 'your_token_here' with your actual token)
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# Headers for authenticated requests
HEADERS = {
    'Authorization': f'token {GITHUB_TOKEN}'
}

# Function to fetch Java files from the repository
def get_content_for_repo(owner, repo):
    java_files = []
    try:
        # GitHub API endpoint URL
        url = f"https://api.github.com/repos/{owner}/{repo}/contents"
        
        # Make a GET request to fetch the contents of the repository
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()  # Raise an exception for 4XX or 5XX status codes
        
        # Extract file and directory information from the response
        items = response.json()
        
        # Iterate through each item in the repository
        for item in items:
            if item["type"] == "file" and item["name"].endswith(".java"):
                # Store the file path for display
                java_files.append(item["path"])
            elif item["type"] == "dir":
                # Recursively fetch content for files in subdirectories
                java_files.extend(get_content_for_directory(owner, repo, item["path"]))
        
        print("Content fetched successfully.")
    except requests.RequestException as e:
        print(f"Error fetching content for the repository: {e}")
        raise
    return java_files

# Function to fetch Java files from a directory
def get_content_for_directory(owner, repo, path):
    java_files = []
    try:
        # GitHub API endpoint URL for a specific directory
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
        
        # Make a GET request to fetch the contents of the directory
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()  # Raise an exception for 4XX or 5XX status codes
        
        # Extract file and directory information from the response
        items = response.json()
        
        # Iterate through each item in the directory
        for item in items:
            if item["type"] == "file" and item["name"].endswith(".java"):
                # Store the file path for display
                java_files.append(item["path"])
            elif item["type"] == "dir":
                # Recursively fetch content for files in subdirectories
                java_files.extend(get_content_for_directory(owner, repo, item["path"]))
    except requests.RequestException as e:
        print(f"Error fetching content for the directory: {e}")
        raise
    return java_files

# Streamlit UI
st.title('FETCH YOUR REPOSITORY')

# Input field for GitHub repository URL
repo_url = st.text_input('GitHub Repository URL', 'https://github.com/SAP-samples/cloud-cap-samples-java')

# Initialize session state
if 'java_files' not in st.session_state:
    st.session_state.java_files = []
if 'selected_file' not in st.session_state:
    st.session_state.selected_file = None
if 'selected_option' not in st.session_state:
    st.session_state.selected_option = None

# Fetch and display Java files when button is clicked
if st.button('Fetch Java Files'):
    try:
        parsed_url = urlparse(repo_url)
        owner, repo = parsed_url.path.strip('/').split('/')
        st.session_state.java_files = get_content_for_repo(owner, repo)
        st.session_state.selected_file = None
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching repository contents: {e}")

# Dropdown for Java files
if st.session_state.java_files:
    st.write("### Select a Java File:")
    st.session_state.selected_file = st.selectbox("Java Files", st.session_state.java_files)

# Dropdown for options
options = ["Engineering", "Architect", "Client"]
if st.session_state.java_files:
    st.write("### Select a Persona:")
    st.session_state.selected_option = st.selectbox("Options", options)

import streamlit as st

# Define a function to generate a unique URL for redirection
def generate_redirect_url(base_url, params):
    param_str = "&".join([f"{key}={value}" for key, value in params.items()])
    return f"{base_url}?{param_str}"

# Display selected file and option with redirection button
if st.session_state.selected_file and st.session_state.selected_option:
    st.write(f"You selected file: :green[{st.session_state.selected_file}]")
    st.write(f"You selected option: :green[{st.session_state.selected_option}]")
    st.write("Click the button below to proceed:")
    
    # Button for redirection
    st.button("Redirect to Google")
       
        
       
# import streamlit as st
# from urllib.parse import urlparse
# import requests
# import os

# # GitHub personal access token (replace 'your_token_here' with your actual token)
# GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# # Headers for authenticated requests
# HEADERS = {
#     'Authorization': f'token {GITHUB_TOKEN}'
# }

# # Global list to store Java file paths
# java_files = []

# def get_content_for_repo(owner, repo):
#     try:
#         # GitHub API endpoint URL
#         url = f"https://api.github.com/repos/{owner}/{repo}/contents"
        
#         # Make a GET request to fetch the contents of the repository
#         response = requests.get(url, headers=HEADERS)
#         response.raise_for_status()  # Raise an exception for 4XX or 5XX status codes
        
#         # Extract file and directory information from the response
#         items = response.json()
        
#         # Iterate through each item in the repository
#         for item in items:
#             if item["type"] == "file" and item["name"].endswith(".java"):
#                 # Extract file name and content
#                 file_name = item["name"]
#                 content = requests.get(item["download_url"], headers=HEADERS).text
                
#                 # Save content to a text file
#                 save_content_to_file(file_name, content)
#                 # Store the file path for display
#                 java_files.append(item["path"])
#             elif item["type"] == "dir":
#                 # Recursively fetch content for files in subdirectories
#                 get_content_for_directory(owner, repo, item["path"])
        
#         print("Content saved successfully.")
#     except requests.RequestException as e:
#         print(f"Error fetching content for the repository: {e}")
#         raise

# def get_content_for_directory(owner, repo, path):
#     try:
#         # GitHub API endpoint URL for a specific directory
#         url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
        
#         # Make a GET request to fetch the contents of the directory
#         response = requests.get(url, headers=HEADERS)
#         response.raise_for_status()  # Raise an exception for 4XX or 5XX status codes
        
#         # Extract file and directory information from the response
#         items = response.json()
        
#         # Iterate through each item in the directory
#         for item in items:
#             if item["type"] == "file" and item["name"].endswith(".java"):
#                 # Extract file name and content
#                 file_name = item["name"]
#                 content = requests.get(item["download_url"], headers=HEADERS).text
                
#                 # Save content to a text file
#                 save_content_to_file(file_name, content)
#                 # Store the file path for display
#                 java_files.append(item["path"])
#             elif item["type"] == "dir":
#                 # Recursively fetch content for files in subdirectories
#                 get_content_for_directory(owner, repo, item["path"])
#     except requests.RequestException as e:
#         print(f"Error fetching content for the directory: {e}")
#         raise

# def save_content_to_file(file_name, content):
#     try:
#         # Create a folder named "Files" if it doesn't exist
#         if not os.path.exists("Files"):
#             os.makedirs("Files")
        
#         # Write content to a text file using UTF-8 encoding
#         with open(f"Files/{file_name}", "w", encoding="utf-8") as file:
#             file.write(content)
#     except Exception as e:
#         print(f"Error saving content to file: {e}")
#         raise

# # Streamlit UI
# st.title('GitHub Repository Java Files')

# repo_url = st.text_input('GitHub Repository URL', 'https://github.com/SAP-samples/cloud-cap-samples-java')

# # Fetch and display Java files when button is clicked
# if st.button('Fetch Java Files'):
#     java_files = []  # Reset the global list
#     try:

#         parsed_url = urlparse(repo_url)
#         owner, repo = parsed_url.path.strip('/').split('/')
#         # Call the function to fetch file content
#         get_content_for_repo(owner, repo)
#         if java_files:
#             st.write("### Java Files:")
#             for file in java_files:
#                 st.text(file)
#         else:
#             st.info('No Java files found in the specified repository.')
#     except requests.exceptions.RequestException as e:
#         st.error(f"Error fetching repository contents: {e}")
