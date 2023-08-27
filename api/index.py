from flask import Flask, request, send_file, jsonify
import os
import pdfplumber
from PyPDF2 import PdfReader, PdfWriter

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
PDF_FILE = ""

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
        print(ecommerce_value, setting_two_value)

        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No selected file'})

        if file and allowed_file(file.filename):
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            else:
                print("Path Exists")

            filepath = os.path.join(upload_dir, file.filename)

            try:
                file.save(filepath)
                
                crop_pdf_page(filepath,'test.pdf')
                
                return send_file('test.pdf', as_attachment=True)
            except Exception as e:
                return jsonify({'error': f'Error saving file: {e}'})
    else:
        return jsonify({'error': 'Invalid file format'})


def crop_pdf_page(input_file, output_file):
  
    reader=PdfReader(input_file,'r')
    writer=PdfWriter()

    print("Total PDF Pages",len(reader.pages))
    page=reader.pages[4]
    # The `print(page)` statement is printing the information about the `page` object.
    # print(page)

    print(page.mediabox.left)
    print(page.mediabox.right)
    print(page.mediabox.top)
    print(page.mediabox.bottom)

    lower_left_cordinate=(170,467)
    upper_right_cordinate=(255,353)

    print(lower_left_cordinate[0])
    for i in range(len(reader.pages)):
        page=reader.pages[i]
        page.cropbox.lower_left=lower_left_cordinate
        page.cropbox.upper_right=upper_right_cordinate
        writer.add_page(page)

    outstream= open(output_file,'wb')
    writer.write(outstream)
    outstream.close()


if __name__ == '__main__':
    app.run(debug=True)
