from flask import Flask, request, redirect, url_for, flash, render_template
from werkzeug.utils import secure_filename
from pathlib import Path

app = Flask(__name__)

app.secret_key = "smart-file-organizer"


# File categories
FILE_CATEGORIES = {
    "Images": [
        ".jpg", ".jpeg", ".png", ".gif",
        ".bmp", ".webp"
    ],

    "Documents": [
        ".pdf", ".doc", ".docx", ".txt",
        ".ppt", ".pptx", ".xls", ".xlsx", ".csv"
    ],

    "Videos": [
        ".mp4", ".mkv", ".avi",
        ".mov", ".webm"
    ],

    "Audio": [
        ".mp3", ".wav", ".aac",
        ".ogg", ".flac"
    ],

    "Archives": [
        ".zip", ".rar", ".7z",
        ".tar", ".gz"
    ],

    "Programs": [
        ".py", ".java", ".cpp",
        ".c", ".html", ".css"
    ]
}


# Find file category
def get_category(filename):

    extension = Path(filename).suffix.lower()

    for category, extensions in FILE_CATEGORIES.items():

        if extension in extensions:
            return category

    return "Others"


# Create unique file name
def get_unique_path(path):

    if not path.exists():
        return path

    counter = 1

    while True:

        new_name = f"{path.stem}_{counter}{path.suffix}"

        new_path = path.parent / new_name

        if not new_path.exists():
            return new_path

        counter += 1


# Home page
@app.route("/")
def home():

    return render_template("index.html")


# Organize files
@app.route("/organize", methods=["POST"])
def organize():

    files = request.files.getlist("files")

    if not files:

        flash("No files selected.")

        return redirect(url_for("home"))


    organized_count = 0


    for file in files:

        if not file or file.filename == "":
            continue


        filename = secure_filename(
            file.filename
        )


        if not filename:
            continue


        category = get_category(
            filename
        )


        folder = (
            Path("organized_files")
            / category
        )


        folder.mkdir(
            parents=True,
            exist_ok=True
        )


        destination = folder / filename


        destination = get_unique_path(
            destination
        )


        file.save(destination)


        organized_count += 1


    flash(
        f"{organized_count} file(s) organized successfully."
    )


    return redirect(
        url_for("home")
    )


# Start Flask server
if __name__ == "__main__":

    print("Smart File Organizer Started!")

    print(
        "Open Chrome: "
        "http://127.0.0.1:5000"
    )

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
)
