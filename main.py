from flask import Flask, render_template,request, flash
from werkzeug.utils import secure_filename
from rembg import remove
import numpy as np
import os
import cv2
UPLOAD_FOLDER='uploads'
ALLOWED_EXTENSIONS={'png','jpg','gif','jpeg'}

app = Flask(__name__)
app.debug=False
app.secret_key = 'super secret key'


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


   
    
    
def processImage(filename,operation):

    print(f"the operation is {operation} and filename is {filename}")
     
    img=cv2.imread(f"uploads/{filename}")
    match operation:
        case "cpng":
            newFilename=f"static/{filename.split('.')[0]}.png"
            cv2.imwrite(newFilename, img)
            return newFilename
        case "cjpg":
            newFilename=f"static/{filename.split('.')[0]}.jpg"
            cv2.imwrite(newFilename, img)
            return newFilename
        case "cjpeg":
            newFilename=f"static/{filename.split('.')[0]}.jpeg"
            cv2.imwrite(newFilename, img)
            return newFilename    
        case "crem":
            input_path = f"uploads/{filename}"
            output_path = f"static/{filename}"
            input = cv2.imread(input_path)
            output = remove(input)
            cv2.imwrite(output_path, output)
             
             
            return output_path
    pass
@app.route('/')
def home():
    return render_template("index.html")

 
@app.route("/edit",methods=["GET","POST"])
def edit():
    if request.method=="POST":
        operation=request.form.get("operation")
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return "error no file"
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return "no file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new=processImage(filename, operation)
            flash(f" <a href='/{new}' target = _blank>Your image has been processed and is available here</a>")
            return render_template("index.html")
       
    return render_template("index.html")

