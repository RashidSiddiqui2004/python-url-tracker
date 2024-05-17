from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/choose_directory', methods=['POST'])
def choose_directory():
    if 'directory' in request.files:
        directory = request.files.getlist('directory')[0]
        dir_path = os.path.dirname(directory.filename)
        files = os.listdir(dir_path)
        files = [f for f in files if os.path.isfile(os.path.join(dir_path, f))]
        return render_template('index.html', files=files, directory=dir_path)
    
    return redirect(url_for('index'))

@app.route('/submit_url', methods=['POST'])
def submit_url():
    selected_file = request.form.get('file')
    url = request.form.get('url')
    directory = request.form.get('directory')

    if selected_file and url and directory:
        file_path = os.path.join(directory, selected_file)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with open(file_path, 'a') as file:
            file.write(f"\n{timestamp}: {url}\n")
        
        return render_template('success.html')
    return "Missing data in form submission", 400

if __name__ == '__main__':
    app.run(debug=True)
