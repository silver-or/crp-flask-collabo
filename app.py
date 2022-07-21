from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

import os

UPLOAD_FOLDER = './save/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def render_file():
    return render_template('upload.html')

@app.route('/fileUpload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'file uploaded successfully'
    else:
        return render_file('upload.html')

if __name__ == '__main__':
    app.run(debug=True)