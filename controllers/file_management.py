from models.file import File

def upload_file(file):
    # Logic để upload file
    # Tạo một đối tượng File và lưu trữ thông tin
    uploaded_file = File(name=file.filename, size=file.content_length, pieces=[])
    # Thêm logic để lưu file vào server
    return {"message": "File uploaded successfully", "file": uploaded_file.name}

def download_file(file_name):
    # Logic để download file
    return {"message": f"Downloading {file_name}"}