
 

import os
from flask import Flask, request, redirect, jsonify,url_for
from werkzeug.utils import secure_filename
import tabula

app = Flask(__name__)

allowed_files = ['pdf']

def checkPdf(filename):
    """
    
    Checks if the given filename is a PDF file by verifying its extension. Returns True if the file is a PDF, False otherwise.
    
    Args:
        filename (str): The name of the file to be checked.
    
    Returns:
        bool: True if the file is a PDF, False otherwise.
    
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_files


@app.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    """
    Uploads a PDF file to the server and redirects to a route to extract data from the uploaded file. Returns an error message if the file is not a PDF or if no file is selected for uploading.
    
    Returns:
        Response: A response object with a JSON message and a status code.
    """
    # check if the post request has the file part
    if 'file' not in request.files:
		resp = jsonify({'message' : 'No file part in the request'})
		resp.status_code = 400
		return resp
	file = request.files['file']
    if file.filename == '':
		resp = jsonify({'message' : 'No file selected for uploading'})
		resp.status_code = 400
		return resp
	if file and checkPdf(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(os.getcwd(), filename))
		return redirect(url_for('get_data',filename = filename))
	else:
		resp = jsonify({'message' : 'Allowed file type is pdf only'})
		resp.status_code = 400
		return resp


@app.route('/scan/<filename>',methods=['GET'])
def get_data(filename):
    """
    Extracts data from a PDF file using the tabula library and returns the data in JSON format. The function reads all pages of the PDF file and extracts the grades data for each semester. The extracted data includes the subject code, subject name, credit, and grade for each subject. The function also extracts the name, roll number, course, and branch of the student from the PDF file.
    
    Args:
        filename (str): The name of the PDF file to be scanned.
    
    Returns:
        Response: A response object with a JSON message containing the extracted data and a status code.
    """

    path = os.path.abspath(os.path.join(os.getcwd(), filename))
    print(path)
    df = tabula.read_pdf(path,pages='all')

    os.remove(os.path.join(os.getcwd(), filename))

    grades = []
    pre_data = []

    for i in range(len(df)):
        if i%2!=0:
            grades.append(df[i])
        else:
            pre_data.append(df[i])

    grades_data = {}
    grade_headings = ['Sub.Code','Subject Name','Credit(s)','Grade']
    maxSem = 0

    for i in range(len(grades)):
        headings = pre_data[i].columns
        sem = pre_data[i][headings[3]][0]
        if int(sem) > maxSem :
            grades_data['name'] = pre_data[i][headings[1]][1]
            grades_data['roll_no'] = pre_data[i][headings[1]][0]
            grades_data['course'] = headings[1]
            grades_data['branch'] = headings[3]

        maxSem = max(maxSem,int(sem))
        grades_data[sem] = {}
        grades_data[sem]['session'] = pre_data[i][headings[3]][1]

        for head in grade_headings:
            grades_data[sem][head] = list(grades[i][head])

    return jsonify(grades_data)


if __name__=='__main__':
    app.run(debug=True)
