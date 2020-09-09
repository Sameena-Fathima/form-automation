from fpdf import FPDF, HTMLMixin
from flask import Flask, jsonify, request, redirect, render_template,session,url_for
from flask_pymongo import PyMongo
import string
from bson.objectid import ObjectId

# class HTML2PDF(FPDF, HTMLMixin):
#     pass

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://sameena:testpass@cluster0.pdqrp.mongodb.net/form_automation?retryWrites=true&w=majority"
#app.config["MONGO_URI"] = "mongodb+srv://teat_user:test123@cluster0.pdqrp.mongodb.net/hospital_pricing?retryWrites=true&w=majority"
mongo = PyMongo(app)

secret_admirer = mongo.db.secret_admirer

@app.route("/secret-admirer")
def secret_admirer():
    return render_template("form.html")

@app.route("/secret-admirer/submit",methods = ['POST'])
def insert_data():
    form_data = {'email' : request.form['email'],
    'name' : request.form['name'], 
    'secret_admirer' : request.form['secret_admirer'],
    'reason': request.form['reason'],
    'hint' : request.form['hint']}
    secret_admirer.insert_one(form_data)

# def html2pdf():
#     # with open('index.html', 'r') as f:
#     #     html_string = f.read() 
#     html = ''' <h1>WHO is your secret admirer?</h1>
#         <p>Gokul</p>
#         <h1>Why?</h1>
#         <p>Hardworking and dedicated</p>
#         <h1>Hint</h1>
#         <p>Deja vu</p>'''
    
#     pdf = HTML2PDF()
#     pdf.add_page()
#     pdf.write_html(html)
#     pdf.add_page()
#     pdf.write_html(html)
#     pdf.output('html2pdf.pdf')
    
if __name__ == '__main__':
    app.run(debug=True)