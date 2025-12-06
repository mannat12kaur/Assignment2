import os
from datetime import datetime
from flask import Flask, request, send_from_directory, render_template_string

app = Flask(__name__)

# Folder where uploaded images will be stored
UPLOAD_FOLDER = os.path.join(app.root_path, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/", methods=["GET"])
def index():
    """
    Show the most recent uploaded image.
    The page refreshes every 30 seconds.
    """
    files = sorted(os.listdir(UPLOAD_FOLDER))
    latest = files[-1] if files else None

    html = """
    <!doctype html>
    <html>
    <head>
        <title>Image Viewer</title>
        <meta http-equiv="refresh" content="30">
        <style>
            body { font-family: Arial, sans-serif; text-align: center; margin-top: 40px; }
            img { max-width: 90vw; max-height: 80vh; border: 1px solid #ccc; }
        </style>
    </head>
    <body>
        <h1>Latest Uploaded Image</h1>
        {% if latest %}
            <p>File: {{ latest }}</p>
            <img src="/uploads/{{ latest }}" alt="Latest image">
        {% else %}
            <p>No images uploaded yet.</p>
        {% endif %}
    </body>
    </html>
    """
    return render_template_string(html, latest=latest)


@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    """
    Serve files from the uploads directory.
    """
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route("/upload", methods=["POST"])
def upload():
    """
    Endpoint to receive an uploaded image file.
    Expects a multipart/form-data POST with field name 'image'.
    """
    file = request.files.get("image")
    if not file:
        return "No file field named 'image' in request", 400

    # Give each file a timestamp-based name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Try to keep original extension if possible
    ext = os.path.splitext(file.filename)[1] or ".png"
    filename = f"{timestamp}{ext}"

    save_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(save_path)

    return "OK", 200


if __name__ == "__main__":
    # Run on port 5000 so we can later use `ngrok http 5000`
    app.run(host="0.0.0.0", port=5000, debug=True)
