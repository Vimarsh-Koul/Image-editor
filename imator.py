from flask import send_from_directory
from markupsafe import escape
import os,time,shutil
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import sqlite3 as lite


UPLOAD_FOLDER = '/home/harsh/Documents/Image-editor/static/UPLOAD_FOLDER'
ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = '3a33686984f59acd653d57db8bb526ce'

# deleting already present folders from my UPLOAD_FOLDER
for filename in os.listdir(UPLOAD_FOLDER):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    shutil.rmtree(file_path)

# using this variable as global to enter data in our database
ans=0

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

            # no need for this now !!!
            #  file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            

            # adding data to the database
            con = lite.connect('test.db')
            with con:
                cur = con.cursor()
                global ans
                if ans==0:
                    cur.execute("DROP TABLE IF EXISTS uploads")
                    cur.execute("CREATE TABLE uploads(id TEXT, name TEXT);")
                ans=ans+1

                # preventing my code from entering a pre existing file detail in my database again
                count =0
                cur.execute("SELECT * FROM uploads")
                rows = cur.fetchall()
                for row in rows:
                    if row [1]==filename:
                        count =1
                        ans= ans-1
                        flash(u'An image already exists with this name','danger')
                        break
                if count ==0 :
                    cur.execute("INSERT INTO uploads VALUES(?,?)",(ans ,filename))

                    ans2= str(ans)
                    path = os.path.join(UPLOAD_FOLDER, ans2)
                    os.mkdir(path)
                    file.save(os.path.join(path, filename))
                    flash(u'Image added','success')

                    #cur.execute("DROP TABLE IF EXISTS " + ans2)
                    #cur.execute("CREATE TABLE" + ans2+"(id TEXT, name TEXT);")
                    #time = time.time()
                    #ur.execute("INSERT INTO" +ans2+ "VALUES(?,?)",(ans, time ,filename))


            return render_template('index.html')
        else:
            flash('wrong format','danger')
            return render_template('index.html')

    return render_template('index.html')

@app.route("/editor/", methods =['GET','POST'])
def editor():
    if request.method == 'POST':
        file_id=request.form['text']
        return redirect(url_for('uploaded_file', file_id = file_id))

    message = "Enter URL in open button to open Image"
    return render_template('editor.html', message=message)

@app.route("/faq/")
def faq():
    return render_template('faq.html')

@app.route('/editor/<file_id>/',methods =['GET','POST'])
def uploaded_file(file_id):
    if request.method == 'POST':
        file_id=request.form['text']

        con = lite.connect('test.db')
        with con:
            cur=con.cursor()
            cur.execute("select * FROM uploads")

            while True:
                row = cur.fetchone()
                if row == None:
                    break
                if row[0] == file_id:
                    filename= row[1]
                    return redirect(url_for('uploaded_file' , file_id=file_id))
            message = "Enter valid ID"
            return render_template('editor.html' , message=message)
    else :
        con = lite.connect('test.db')
        with con:
            cur=con.cursor()
            cur.execute("select * FROM uploads")

            while True:
                row = cur.fetchone()
                if row == None:
                    break
                if row[0] == file_id:
                    filename= row[1]
                    return render_template('editor.html',filename=filename, file_id = file_id)
            message = "Enter valid ID"
            return render_template('editor.html', message = message)

if __name__ == '__main__':
    app.run(debug=True)
