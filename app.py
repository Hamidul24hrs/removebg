from flask import Flask, render_template, request, send_file
import os
from rembg import remove  # `rembg` লাইব্রেরি ব্যবহার করা হচ্ছে

app = Flask(__name__)

# ফোল্ডার যেখানে ছবিগুলি আপলোড হবে
UPLOAD_FOLDER = 'uploads/'
OUTPUT_FOLDER = 'outputs/'

# ফোল্ডার তৈরি করা
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return "No file part"
    file = request.files['image']
    
    if file.filename == '':
        return "No selected file"
    
    # ফাইল সেভ করা
    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(input_path)

    # ব্যাকগ্রাউন্ড রিমুভ করা
    output_path = os.path.join(OUTPUT_FOLDER, 'output_' + file.filename)
    with open(input_path, 'rb') as input_file:
        input_data = input_file.read()
        output_data = remove(input_data)  # `rembg` লাইব্রেরি ব্যাকগ্রাউন্ড সরানোর জন্য

        with open(output_path, 'wb') as output_file:
            output_file.write(output_data)

    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
