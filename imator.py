from flask import send_from_directory
from markupsafe import escape
import os,time,shutil,wget,urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template,jsonify
from werkzeug.utils import secure_filename
import sqlite3 as lite
from PIL import Image,ImageDraw
from math import sin,cos,pi

file_path_1 = os.path.abspath(os.getcwd())
file_path_2 = os.path.join(file_path_1,'static')

UPLOAD_FOLDER = os.path.join(file_path_2,'UPLOAD_FOLDER')
DOWNLOADED_IMAGES = os.path.join(file_path_2,'DOWNLOADED_IMAGES')
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
                    cur.execute("DROP TABLE IF EXISTS operations")
                    cur.execute("CREATE TABLE operations(id INTEGER PRIMARY KEY,image_id INTEGER, operation_name TEXT, operation_id INTEGER);")
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

                    ans2= str(ans)
                    path = os.path.join(UPLOAD_FOLDER, ans2)
                    os.mkdir(path)
                    filename2 = "1_" +filename
                    file.save(os.path.join(path, filename2))
                    flash(u'Image added','success')

                    cur.execute("INSERT INTO uploads VALUES(?,?)",(ans ,filename))
                    cur.execute("INSERT INTO operations(image_id,operation_name,operation_id) VALUES(?,?,?)",(ans ,'upload',1))

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

            cur.execute("select * FROM operations")
            value = 1
            while True:
                row = cur.fetchone()
                if row == None:
                    break
                if row[1] == int(file_id):
                    value = value +1

            cur.execute("select * FROM uploads")
            while True:
                row = cur.fetchone()
                if row == None:
                    break
                if row[0] == file_id:
                    filename= row[1]
                    filename2 = str(value-1) +"_" + filename 
                    return render_template('editor.html',filename=filename2, file_id = file_id)
            message = "Enter valid ID"
            return render_template('editor.html', message = message)

@app.route("/editor/<file_id>/1",methods=['GET','POST'])
def implementation(file_id):
    
    con = lite.connect('test.db')
    with con:
        cur=con.cursor()
        cur.execute("select * FROM operations")

        value = 1
        while True:
            row = cur.fetchone()
            if row == None:
                break
            if row[1] == int(file_id):
                value = value +1

        cur.execute("select * FROM uploads")

        while True:
            row = cur.fetchone()
            if row == None:
                break
            if row[0] == file_id:
                filename= row[1]

        path = os.path.join(UPLOAD_FOLDER, file_id)
        filename3 = str(value-1) +"_" + filename 
        path2 = os.path.join(path,filename3)
        file = Image.open(path2)
        file2 = file.copy()

        # parameters that we will get from ajax to apply changes through this function
        feature= str(request.form['a'])
        # parameters end

        # code for this particular operation start
        if(feature == 'rotate-left'):
            file2 = file2.transpose(Image.ROTATE_90)
        elif(feature == 'rotate-right'):
            file2 = file2.transpose(Image.ROTATE_270)
        elif(feature == 'horizontal-flip'):             # complete
            input_pixels = file2.load()

            # Create output image
            output_image = Image.new("RGB", file2.size)
            draw = ImageDraw.Draw(output_image)

            # Copy pixels
            for x in range(output_image.width):
                for y in range(output_image.height):
                    xp = file2.width - x - 1
                    draw.point((x, y), input_pixels[xp, y])

            file2 = output_image
        elif(feature == 'vertical-flip'):                 # complete
            input_pixels = file2.load()

            # Create output image
            output_image = Image.new("RGB", file2.size)
            draw = ImageDraw.Draw(output_image)

            # Copy pixels
            for x in range(output_image.width):
                for y in range(output_image.height):
                    yp = file2.height - y -1
                    draw.point((x, y), input_pixels[x, yp])

            file2 = output_image
        elif(feature == 'greyscale'):                      # complete
            file5 = file2.load()
            [width,height] = list(file2.size)
            for i in range(0,width):
                for j in range(0,height):
                    r,g,b,a=list(file5[i,j])
                    l  = int(0.2126*r+0.7152*g+0.0722*b)
                    valuee=(l,l,l,a)
                    file5[i,j]=valuee
        elif(feature == 'save'):
            path_download = os.path.join(DOWNLOADED_IMAGES,filename)
            file2.save(path_download)


        # code ends

        filename4 = str(value) + "_" + filename
        path3 = os.path.join(path,filename4)
        file2.save(path3) 

        cur.execute("INSERT INTO operations(image_id,operation_name,operation_id) VALUES(?,?,?)",(file_id ,feature,value))

    return jsonify(result = filename4)

if __name__ == '__main__':
    app.run(debug=True)