import os

# folder to store uploaded files
FILES_DIR = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "files")
)


def save_file(uploaded_file):
    """helper function to save documents to disk"""
    file_path = os.path.join(FILES_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path
