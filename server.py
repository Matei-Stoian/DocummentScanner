import os
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from Scanner import Scanner

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
UPLOAD_FOLDER = 'static/uploads/'
SAVED_FOLDER = 'static/outputs/'

for f in os.listdir(UPLOAD_FOLDER):
    os.remove(os.path.join(UPLOAD_FOLDER, f))

for f in os.listdir(SAVED_FOLDER):
    os.remove(os.path.join(SAVED_FOLDER, f))

app = Flask(__name__)
app.secret_key = "secret_key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SAVED_FOLDER'] = SAVED_FOLDER


def allowed_file(filname):
    return '.' in filname and filname.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def upload_form():
    return render_template('upload_form.html')


@app.route("/",  methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']

    if file.headers == '':
        flash('No image selected for uploading')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        Scanner(os.path.join(app.config['UPLOAD_FOLDER'], filename), filename)
        flash('Image successfully uploaded and displyed below')
        return render_template('upload_form.html', filename=filename)
    else:
        flash('Allowd image types are -> .png, .jpg, .jpeg')
        return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='outputs/'+filename), code=301)


if __name__ == '__main__':
    app.run(debug=True)
