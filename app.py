from fpdf import FPDF, HTMLMixin
from flask import Flask, jsonify, request, redirect, render_template,session,url_for,send_file
from flask_pymongo import PyMongo
import random
import string
import datetime
from bson.objectid import ObjectId
import os


class HTML2PDF(FPDF, HTMLMixin):
    pass

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://sameena:testpass@cluster0.pdqrp.mongodb.net/form_automation?retryWrites=true&w=majority"
mongo = PyMongo(app)

secret_admirer = mongo.db.secret_admirer
secret_admirer_forms = mongo.db.secret_admirer_forms
intern_of_the_week = mongo.db.intern_of_the_week
intern_of_the_week_forms = mongo.db.intern_of_the_week_forms

@app.route("/secret-admirer/<form_id>",methods=['POST','GET'])
def secret_admirer_form(form_id):
    form = secret_admirer_forms.find_one({'form_id':form_id})
    if(form == None):
        return "404 Not Found"
    form_data = {
        'email' : '',
        'name' : '', 
        'secret_admirer' : '',
        'reason': '',
        'hint' : '',
        'form_id' : form_id
        }
    return render_template("form.html", form = form, error_msg = '', form_data = form_data)

@app.route("/intern-of-the-week/<form_id>",methods=['POST','GET'])
def intern_of_the_form(form_id):
    form = intern_of_the_week_forms.find_one({'form_id':form_id})
    if(form == None):
        return "404 Not Found"
    form_data = {
        'email' : '',
        'name' : '', 
        'intern_of_the_week' : '',
        'reason': '',
        'star': '',
        'questions' : '',
        'form_id' : form_id
        }
    return render_template("form-2.html", form = form, form_data = form_data)

@app.route("/secret-admirer/<form_id>/submit",methods = ['POST'])
def secret_admirer_insert_data(form_id):
    form_data = {
        'email' : request.form['email'],
        'name' : request.form['name'], 
        'secret_admirer' : request.form['secret_admirer'],
        'reason': request.form['reason'],
        'hint' : request.form['hint'],
        'form_id' : form_id
        }
    if(request.form['email'] == ''):
        error_msg = "Please Give Your Email Address"
        form = secret_admirer_forms.find_one({'form_id':form_id})
        return render_template("form.html", form = form, error_msg = error_msg, form_data = form_data)
    if(request.form['name'] == ''):
        error_msg = "Please Give Your Name"
        form = secret_admirer_forms.find_one({'form_id':form_id})
        return render_template("form.html", form = form, error_msg = error_msg, form_data = form_data)
    if(request.form['secret_admirer'] == ''):
        error_msg = "Please Give Your Secret Admirer Name"
        form = secret_admirer_forms.find_one({'form_id':form_id})
        return render_template("form.html", form = form, error_msg = error_msg, form_data = form_data)
    if(request.form['reason'] == ''):
        error_msg = "Please Give The Reason"
        form = secret_admirer_forms.find_one({'form_id':form_id})
        return render_template("form.html", form = form, error_msg = error_msg, form_data = form_data)
    if(request.form['hint'] == ''):
        error_msg = "Please Give Any Hint"
        form = secret_admirer_forms.find_one({'form_id':form_id})
        return render_template("form.html", form = form, error_msg = error_msg, form_data = form_data)
    #print(form_data)
    secret_admirer.insert_one(form_data)
    return render_template("form-submitted.html")

@app.route("/intern-of-the-week/<form_id>/submit",methods = ['POST'])
def intern_of_the_week_insert_data(form_id):
    form_data = {
        'email' : request.form['email'],
        'name' : request.form['name'], 
        'intern_of_the_week' : request.form['intern_of_the_week'],
        'reason': request.form['reason'],
        'star' : request.values.get('star'),
        'questions' : request.form['questions'],
        'form_id' : form_id
        }
    if(request.form['email'] == ''):
        error_msg = "Please Give Your Email Address"
        form = intern_of_the_week_forms.find_one({'form_id':form_id})
        return render_template("form-2.html", form = form, error_msg = error_msg, form_data = form_data)
    if(request.form['name'] == ''):
        error_msg = "Please Give Your Name"
        form = intern_of_the_week_forms.find_one({'form_id':form_id})
        return render_template("form-2.html", form = form, error_msg = error_msg, form_data = form_data)
    if(request.form['intern_of_the_week'] == ''):
        error_msg = "Please Give Your Nominee Name"
        form = intern_of_the_week_forms.find_one({'form_id':form_id})
        return render_template("form-2.html", form = form, error_msg = error_msg, form_data = form_data)
    if(request.form['reason'] == ''):
        error_msg = "Please Give The Reason"
        form = intern_of_the_week_forms.find_one({'form_id':form_id})
        return render_template("form-2.html", form = form, error_msg = error_msg, form_data = form_data)
    if(request.values.get('star') == None):
        error_msg = "Please Give The Star Rating"
        form = intern_of_the_week_forms.find_one({'form_id':form_id})
        return render_template("form-2.html", form = form, error_msg = error_msg, form_data = form_data)
    #print(form_data)
    intern_of_the_week.insert_one(form_data)
    return render_template("form-2-submitted.html")

@app.route("/download-pdf",methods = ['GET'])
def download_pdf():
    return render_template('download.html',value = "secret_admirer.pdf")


@app.route('/secret-admirer/<return_file_type>/<form_id>')
def return_file(return_file_type,form_id):
    print(return_file_type)
    pdf = HTML2PDF()
    rows = secret_admirer.find({'form_id':form_id})
    results = []
    html = ''''''
    if(return_file_type == "admin-return-file"):
        for row in rows:
            Email = row['email']
            Name = row['name']
            Secret_Admirer = row['secret_admirer']
            Reason = row['reason']
            Hint = row['hint']
            # print("printing",Secret_Admirer,Reason,Hint)
            html += '''<h1>Email</h1>
                <p>'''+Email+'''</p>
                <h1>Name</h1>
                <p>'''+Name+'''</p>
                <h1>Who is your secret admirer in our Intern team?</h1>
                <p>'''+Secret_Admirer+'''</p>
                <h1>Tell us why?</h1>
                <p>'''+Reason+'''</p>
                <h1>Give them a hint about you so they can guess a bit</h1>
                <p>'''+Hint+'''</p><br><br><hr><br>'''
    else:
        for row in rows:
            Secret_Admirer = row['secret_admirer']
            Reason = row['reason']
            Hint = row['hint']
            print(Secret_Admirer,Reason,Hint)
            html += '''<h1>Who is your secret admirer in our Intern team?</h1>
                <p>'''+Secret_Admirer+'''</p>
                <h1>Tell us why?</h1>
                <p>'''+Reason+'''</p>
                <h1>Give them a hint about you so they can guess a bit</h1>
                <p>'''+Hint+'''</p><br><br><hr><br>'''
        
    pdf.add_page()
    pdf.write_html(html)
    pdf.output('img/secret_admirer.pdf')
    file_path = "img/secret_admirer.pdf"
    return send_file(file_path, attachment_filename='secret-admirer.pdf', as_attachment=True, cache_timeout=0)

@app.route('/intern-of-the-week/<return_file_type>/<form_id>')
def return_file_2(return_file_type,form_id):
    pdf = HTML2PDF()
    rows = intern_of_the_week.find({'form_id':form_id})
    results = []
    html = ''''''
    if(return_file_type == "admin-return-file"):
        for row in rows:
            Email = row['email']
            Name = row['name']
            Intern_of_the_week = row['intern_of_the_week']
            Reason = row['reason']
            star = row['star']
            questions = row['questions']
            print(Email,Name,Intern_of_the_week,Reason,star)
            html += '''<h1>Email</h1>
                <p>'''+Email+'''</p>
                <h1>Name</h1>
                <p>'''+Name+'''</p>
                <h1>Who would you nominate as Intern of the Week?</h1>
                <p>'''+Intern_of_the_week+'''</p>
                <h1>Why would you nominate them?</h1>
                <p>'''+Reason+'''</p>
                <h1>Rate them (1-10)</h1>
                <p>'''+star+'''</p>
                <h1>Comments/Questions</h1>
                </p>'''+questions+'''</p><br><br><hr><br>'''      
    else:
        for row in rows:
            Intern_of_the_week = row['intern_of_the_week']
            Reason = row['reason']
            star = row['star']
            questions = row['questions']
            print("printing",Intern_of_the_week,Reason,star)
            html += '''<h1>Who would you nominate as Intern of the Week?</h1>
                <p>'''+Intern_of_the_week+'''</p>
                <h1>Why would you nominate them?</h1>
                <p>'''+Reason+'''</p>
                <h1>Rate them (1-10)</h1>
                <p>'''+star+'''</p>
                <h1>Comments/Questions</h1>
                </p>'''+questions+'''</p><br><br><hr><br>'''

    pdf.add_page()
    pdf.write_html(html)
    pdf.output('img/intern_of_the_week.pdf')
    file_path = "img/intern_of_the_week.pdf"
    return send_file(file_path, attachment_filename='intern-of-the-week.pdf', as_attachment=True, cache_timeout=0)

@app.route('/')
def index():
    secret_admirer_forms_list = secret_admirer_forms.find()
    intern_of_the_week_forms_list = intern_of_the_week_forms.find()
    return render_template("index.html", secret_admirer_forms_list = secret_admirer_forms_list, intern_of_the_week_forms_list = intern_of_the_week_forms_list)


@app.route('/new-secret-admirer-form')
def new_form():
    return render_template("new_form.html")

@app.route('/create-secret-admirer-form', methods=['POST'])
def create_form():
    form_name = request.form['form-name']
    if(form_name==''):
        return render_template("new_form.html", error_msg = "Please enter form name")
    letters_and_digits = string.ascii_letters + string.digits
    form_id = ''.join((random.choice(letters_and_digits) for i in range(16)))
    current_date = datetime.date.today()
    date = current_date.strftime("%d-%m-%Y")
    secret_admirer_forms.insert_one({'form_name':form_name, 'form_id':form_id, 'date':date})
    return redirect(url_for('form_details', form_id = form_id))

@app.route('/secret-admirer-form-details/<form_id>')
def form_details(form_id):
    form = secret_admirer_forms.find_one({'form_id':form_id})
    responses = secret_admirer.find({'form_id':form['form_id']})
    return render_template("form-details.html",form = form, responses = responses)

@app.route('/new-intern-of-the-week-form')
def new_form_2():
    return render_template("new_form_2.html")

@app.route('/create-intern-of-the-week-form', methods=['POST'])
def create_form_2():
    form_name = request.form['form-name']
    if(form_name==''):
        return render_template("new_form_2.html", error_msg = "Please enter form name")
    letters_and_digits = string.ascii_letters + string.digits
    form_id = ''.join((random.choice(letters_and_digits) for i in range(16)))
    current_date = datetime.date.today()
    date = current_date.strftime("%d-%m-%Y")
    intern_of_the_week_forms.insert_one({'form_name':form_name, 'form_id':form_id, 'date':date})
    return redirect(url_for('form_details_2', form_id = form_id))

@app.route('/intern-of-the-week-form-details/<form_id>')
def form_details_2(form_id):
    form = intern_of_the_week_forms.find_one({'form_id':form_id})
    responses = intern_of_the_week.find({'form_id':form['form_id']})
    return render_template("form-2-details.html",form = form, responses = responses)


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