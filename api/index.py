from flask import Flask, request, send_file, jsonify
import os
import PyPDF2




app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}


UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Existing code
upload_dir = app.config['UPLOAD_FOLDER']


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def hello():
    return 'Hello'

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        ecommerce_value = request.form.get('Ecommerce')
        setting_two_value = request.form.get('settingTwo')
        print(ecommerce_value,setting_two_value)
        # print(request)
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No selected file'})

        if file and allowed_file(file.filename):
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            else:
                print("Path Exsisits")

            filepath = os.path.join(upload_dir, file.filename)
            
            

            try:
                file.save(filepath)
                
                # Read the PDF file line by line
                with open(filepath, "rb") as f:
                    pdf_reader = PyPDF2.PdfReader(f)
                    
                    # Crop each page of the PDF file
                    for page_number in range(len(pdf_reader.pages)):
                        page = pdf_reader.pages[page_number]
                        cropbox = (100, 100, 100, 100)
                        page.cropbox = cropbox

                    # Save the cropped PDF file
                    with open(f"{filepath}-cropped.pdf", "wb") as output_file:
                        pdf_writer = PyPDF2.PdfFileWriter()
                        pdf_writer.addPage(page)
                        pdf_writer.write(output_file)

                return send_file(filepath, as_attachment=True)
            except Exception as e:
                return jsonify({'error': f'Error saving file: {e}'})
    else:
        return jsonify({'error': 'Invalid file format'})


if __name__ == '__main__':
    app.run(debug=True)
