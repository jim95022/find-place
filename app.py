from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from detect_landmarks import detect_landmarks
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="money0-c11ce91689a6.json"

UPLOAD_FOLDER = '/tmp/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

class place():

    def __init__(self):
        self.lng = 0
        self.lat = 0
        self.desc = 'None'

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    try:
        place.lat, place.lng, place.desc = detect_landmarks(app.config['UPLOAD_FOLDER'] + filename)
        return render_template('place.html', place=place)
    except:
        return render_template('fail.html')

if __name__ == "__main__":
    app.run()