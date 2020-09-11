from fpdf import FPDF, HTMLMixin
from flask import Flask, jsonify, request, redirect, render_template,session,url_for,send_file
from flask_pymongo import PyMongo
import string
from bson.objectid import ObjectId
import secrets


class HTML2PDF(FPDF, HTMLMixin):
    pass

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://sameena:testpass@cluster0.pdqrp.mongodb.net/form_automation?retryWrites=true&w=majority"
mongo = PyMongo(app)

secret_admirer = mongo.db.secret_admirer

@app.route("/secret-admirer/<form_name>/<referral_number>",methods=['POST','GET'])
def secret_admirer_form(form_name,referral_number):
    return render_template("form.html")

@app.route("/secret-admirer/submit",methods = ['POST'])
def insert_data():
    form_data = {'email' : request.form['email'],
    'name' : request.form['name'], 
    'secret_admirer' : request.form['secret_admirer'],
    'reason': request.form['reason'],
    'hint' : request.form['hint']}
    secret_admirer.insert_one(form_data)
    return "submitted successfully"

@app.route("/download-pdf",methods = ['GET'])
def download_pdf():
    return render_template('download.html',value = "secret_admirer.pdf")

pdf = HTML2PDF()
@app.route('/return-file/<filename>')
def return_files_tut(filename):
    rows = secret_admirer.find()
    results = []
    for row in rows:
        Secret_Admirer = row['secret_admirer']
        Reason = row['reason']
        Hint = row['hint']
        print("printing",Secret_Admirer,Reason,Hint)
        html = '''<h1>WHO is your secret admirer?</h1>
            <p>'''+Secret_Admirer+'''</p>
            <h1>Why?</h1>
            <p>'''+Reason+'''</p>
            <h1>Hint</h1>
            <p>'''+Hint+'''</p>'''
        print(html)
        pdf.add_page()
        pdf.write_html(html)
    pdf.output('img/secret_admirer.pdf')
    file_path = "img/secret_admirer.pdf"
    return send_file(file_path, as_attachment=True, attachment_filename='')

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/new-form')
def new_form():
    secretsGenerator = secrets.SystemRandom()
    randomNumber = secretsGenerator.randint(9999,1000000)
    print(randomNumber)
    return render_template("new_form.html",rand_num = randomNumber)
# @app.route("/htmltopdf",methods = ['GET','POST'])
# def html2pdf():
#     # with open('index.html', 'r') as f:
#     #     html_string = f.read() 
#     rows = secret_admirer.find()
#     results = []
#     for row in rows:
#         Secret_Admirer = row['secret_admirer']
#         Reason = row['reason']
#         Hint = row['hint']
#         print("printing",Secret_Admirer,Reason,Hint)
#         html = '''<h1>WHO is your secret admirer?</h1>
#             <p>'''+Secret_Admirer+'''</p>
#             <h1>Why?</h1>
#             <p>'''+Reason+'''</p>
#             <h1>Hint</h1>
#             <p>'''+Hint+'''</p>'''
#         print(html)
#         pdf.add_page()
#         pdf.write_html(html)
#     pdf.output('img/secret_admirer.pdf')
#     file_path = "img/secret_admirer.pdf"
#     return send_file(file_path, as_attachment=True, attachment_filename='')
    
if __name__ == '__main__':
    app.run(debug=True)