import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import whisper

UPLOAD_FOLDER = r"c:\proyectos\Python\speechToText\Backend\uploads"
ALLOWED_EXTENSIONS = {'mp3', 'mp4'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Nombre de la carpeta donde se guardaran los documentos
@app.route("/upload", methods = ["POST"])
def upload():
        # check if the post request has the file part
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
         # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filePath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filePath)
            
            model = whisper.load_model('base')
            result = model.transcribe(filePath, language="es")
            
            return {
                "text": result['text']
            }, 200
        
@app.route("/run", methods = ["POST"])
def run():
    
    model = whisper.load_model("base")
    result = model.transcribe('./uploads/audio.mp3')

    return result["text"]
        
if __name__ == "__main__":
    app.run()


