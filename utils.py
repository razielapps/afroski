import os
from werkzeug.utils import secure_filename
import uuid

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png', 'gif'}

def save_image(file, folder):
    if not allowed_file(file.filename):
        return None

    ext = file.filename.rsplit('.', 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    filename = secure_filename(filename)

    path = os.path.join('static/uploads', folder)
    os.makedirs(path, exist_ok=True)

    file_path = os.path.join(path, filename)
    file.save(file_path)

    return filename
