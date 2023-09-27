import os

from flask import Flask, json, request, Response
from flask_api import status
from werkzeug.utils import secure_filename

from converters.image_converter import ImageConverter

UPLOAD_FOLDER = "~/Test"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/image_coverter/generate", methods=["POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            description = '{"Error": "No file argument passed"}'
            return Response(
                response=description,
                status=status.HTTP_400_BAD_REQUEST,
                mimetype="application/json",
            )
        file = request.files["file"]
        if not (file and allowed_file(file.filename)):
            description = {"Error": f'No file or extension not in {ALLOWED_EXTENSIONS}'}
            return Response(
                response=json.dumps(description),
                status=status.HTTP_400_BAD_REQUEST,
                mimetype="application/json",
            )
        else:
            filename = secure_filename(file.filename)
            file.save(filename)

            cols = request.args.get("cols", type=int)
            scale = request.args.get("scale", type=float)
            more_levels = request.args.get("more_levels", type=bool)

            ic = ImageConverter()
            ascii_image = ic.convert_data(filename, cols, scale, more_levels)
            response = {"ProcessedImage": ascii_image}
            os.remove(filename)
            return Response(
                response=json.dumps(response),
                status=status.HTTP_200_OK,
                mimetype="application/json",
            )
    return """
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    """
