from flask import Flask, request, render_template
import os
import cv2
from werkzeug.utils import secure_filename
from deeplearning import test_model, yolo_predictions, net

app = Flask(__name__)

UPLOAD_FOLDER = 'static/upload'
PREDICT_FOLDER = 'static/predict'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PREDICT_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part in the request", 400
        file = request.files['file']
        if file.filename == '':
            return "No file selected for uploading", 400
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            
            # Run your detection and text extraction
            image = cv2.imread(file_path)
            result_img, text_list = yolo_predictions(image, net)
            result_img_path = os.path.join(PREDICT_FOLDER, filename)
            cv2.imwrite(result_img_path, result_img)

            return render_template('index.html', upload=True, upload_image=filename, text=text_list, no=len(text_list))
    return render_template('index.html', upload=False)

if __name__ == "__main__":
    app.run(debug=True)



























# from flask import Flask, render_template, request
# import os 
# from deeplearning import object_detection
# import pytesseract

# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# # webserver gateway interface
# app = Flask(__name__)

# BASE_PATH = os.getcwd()
# UPLOAD_PATH = os.path.join(BASE_PATH,'static/upload/')


# @app.route('/',methods=['POST','GET'])
# def index():
#     if request.method == 'POST':
#         upload_file = request.files['image_name']
#         filename = upload_file.filename
#         path_save = os.path.join(UPLOAD_PATH,filename)
#         upload_file.save(path_save)
#         text_list = object_detection(path_save,filename)
        
#         print(text_list)

#         return render_template('index.html',upload=True,upload_image=filename,text=text_list,no=len(text_list))

#     return render_template('index.html',upload=False)


# if __name__ =="__main__":
#     app.run(debug=True)