import os

def detect_file_type(file_name):
    ext = file_name.lower().split(".")[-1]

    if ext == "pdf":
        return "pdf"
    elif ext == "docx":
        return "docx"
    else:
        raise ValueError("Unsupported file type")


def save_uploaded_file(uploaded_file, save_path):
    os.makedirs(save_path, exist_ok=True)

    file_path = os.path.join(save_path, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path