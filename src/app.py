from flask import Flask, request, jsonify

from src.classifier import classify_file
from src.text_extraction import get_text_from_image, get_text_from_docx, get_text_from_pdf
app = Flask(__name__)

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', "docx"}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/classify_file', methods=['POST'])
def classify_file_route():

    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": f"File type not allowed"}), 400

    filename = file.filename.lower()

     # Attempt to classify based on file name
    file_class = classify_file(file, "")
    if file_class != "unknown file":
        return jsonify({"file_class": file_class}), 200

    if filename.endswith("pdf"): 
        text = get_text_from_pdf(file)
    
    elif filename.endswith(("png", "jpg")): 
        text = get_text_from_image(file)
    
    else: 
        text = get_text_from_docx(file)
    
    file_class = classify_file(file, text)
    return jsonify({"file_class": file_class}), 200


if __name__ == '__main__':
    app.run(debug=True)
