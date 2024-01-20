from flask import Flask,render_template,request,flash
from werkzeug.utils import secure_filename
from PIL import Image
import os
import cv2 as cv

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'gif'}

app = Flask(__name__)
app.secret_key = 'the random string'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def processImage(filename,operation):
    print(f'the operation is {operation} and ')
    img=cv.imread(f"uploads/{filename}")
    match operation:
        case "cgray":
            imgProcessed=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
            cv.imwrite(f"static/{filename}",imgProcessed)
            new_filename=f"static/{filename}"
            return new_filename
        case "cpng":
            im = Image.open(f"uploads/{filename}")
            im.save(f"static/{filename.split('.')[0]}.png","PNG")
            new_filename=f"static/{filename.split('.')[0]}.png"
            return new_filename
        case "cjpg":
             im = Image.open(f"uploads/{filename}")
             im.save(f"static/{filename.split('.')[0]}.jpg","JPEG")
             new_filename=f"static/{filename.split('.')[0]}.jpg"
             return new_filename
        case "cwebp":
            im = Image.open(f"uploads/{filename}")
            im.save(f"static/{filename.split('.')[0]}.webp","WEBP")
            new_filename=f"static/{filename.split('.')[0]}.webp"
            return new_filename
    pass

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact_us')
def contact_us():
    return render_template("contact.html")

@app.route('/edit',methods=['GET','POST'])
def edit():
    if request.method=="POST":
        operation=request.form.get("operation")
        print(operation)
        if 'file' not in request.files:
            flash('No file part')
            return "error"
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return "error"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new=processImage(filename,operation)
            flash(f"Your image has been processed and is avaialable <a href='/{new}'>here</a>")
            return render_template('index.html')


app.run(debug=True)