from flask import send_from_directory
from markupsafe import escape
import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/home/harsh/Documents/Image-editor/static/UPLOAD_FOLDER'
ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = '3a33686984f59acd653d57db8bb526ce'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET' , 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash(u'No file part','danger')
            return render_template('index.html')
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash(u'No selected file','danger')
            return render_template('index.html')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash(u'Image added','success')
            return render_template('index.html')
    return render_template('index.html')

@app.route("/editor/", methods =['GET','POST'])
def editor():
    if request.method == 'POST':
        filename=request.form['text']
        return redirect(url_for('uploaded_file',filename=filename))
    return render_template('editor.html')

@app.route("/faq/")
def faq():
    return render_template('faq.html')

@app.route('/editor/<filename>/',methods =['GET','POST'])
def uploaded_file(filename):
    if request.method == 'POST':
        filename=request.form['text']
        return redirect(url_for('uploaded_file',filename=filename))
    return render_template('editor.html',filename=filename)
    

if __name__ == '__main__':
    app.run(debug=True) 

