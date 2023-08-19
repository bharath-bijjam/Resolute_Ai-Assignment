from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from FaceUtils import findFace
from deepface import DeepFace
import pickle
import os

server = Flask(__name__)

upload_folder = os.path.join('static', 'uploads')
db_path = os.path.join(upload_folder, "representations_facenet.pkl")
 
server.config['UPLOAD'] = upload_folder

@server.route('/', methods=['GET'])
def home():
    return render_template("index.html")

@server.route('/register',methods=['GET','POST'])
def register():
    if request.method == "GET":
        return render_template('registration_form.html')
    
    elif request.method == "POST":

        if "img" not in request.files:
            return (
                render_template(
                "info.html",
                status_message="No file selected"
                )
            )
        

        file = request.files['img']

        if file.filename == "":
            return (
                render_template(
                "info.html",
                status_message="No file selected"
                )
            )
        
        filename = secure_filename(file.filename)
        imagepath = os.path.join(upload_folder, filename)
        
        file.save(imagepath)

        try:
            os.remove(db_path)
        except Exception:
            pass

        try:
            findFace(imagepath)
        except Exception:
            return render_template(
                "info.html",
                status_message="No Face detected in the Image"
            )

        return render_template(
            "info.html",
            status_message="Your Face has been registerd"
        )
    

@server.route('/recognize',methods=['POST','GET'])
def recognize():
    if request.method == "POST":

        if "img" not in request.files:
            return (
                render_template(
                "info.html",
                status_message="No file selected"
                )
            )
        

        file = request.files['img']

        if file.filename == "":
            return (
                render_template(
                "info.html",
                status_message="No file selected"
                )
            )
        


        temp_path = os.path.join(upload_folder, "temp.jpg")

        image = request.files['img'].read()

        f = open(temp_path, 'wb')
        f.write(image)
        f.close()
        
        is_registered = findFace(temp_path)
       

        if is_registered:
            return render_template(
                "info.html",
                status_message="Your Face has been recognized"
            )
        else:
            return render_template(
                "info.html",
                status_message="Your Face has not verified"
            )
    else:
        return render_template("index.html")

if __name__ == '__main__':
    server.run(debug=False, port=8000)