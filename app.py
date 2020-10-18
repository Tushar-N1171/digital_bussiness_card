from flask import Flask,render_template, request, flash,make_response
from flask_pymongo import PyMongo
import pdfkit
import os
from flask_weasyprint import HTML, render_pdf

basedir = os.path.abspath(os.path.dirname(__file__))
config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')


app = Flask(__name__)


app.config["MONGO_URI"] = "mongodb://localhost:27017/trail"


mongo = PyMongo(app)


@app.route('/')
def inded():
    return render_template("index.html")

@app.route('/create_card', methods=['GET', 'POST'])
def create_card():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        phone = request.form['phone']

        data = {
            'fname':fname,
            'lname':lname,
            'email':email,
            'phone':phone
        }
        print(data)

        done = mongo.db.cards.insert_one(
            {
            'fname':fname,
            'lname':lname,
            'email':email,
            'phone':phone
            }
        )

        if done:
            flash("Data added successfully","success")
        else:
            flash("something went wrong with database","danger")


    cards = mongo.db.cards.find()



    return render_template("create_card.html",cards=cards)



@app.route('/view_card/<fname>', methods=['GET', 'POST'])
def view_card(fname):
    card = mongo.db.cards.find_one({'fname':fname})

    
    return render_template("view_card.html",card = card)

@app.route('/pdf_card/<fname>', methods=['GET', 'POST'])
def pdf_card(fname):

    card = mongo.db.cards.find_one({'fname':fname})

    css = [
        basedir+"/static/css/bootstrap.css",
    
        basedir+"/static/css/style.css",
        basedir+"/static/css/responsive.css",
        ]

    rendered = render_template("pdf_card.html",card = card)
    pdf = pdfkit.from_string(rendered, False, css=css, configuration=config)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = (
        "attachment; filename=" + fname +".pdf"
    )

    return response


@app.route('/pdf_card1/<fname>')
def pdf_card1(fname):
    # Make a PDF straight from HTML in a string.
    card = mongo.db.cards.find_one({'fname':fname})

    html = render_template("view_card.html",card = card)
    return render_pdf(HTML(string=html),stylesheets=css)


@app.route('/pdf_approach2/<fname>', methods=['GET', 'POST'])
def pdf_approach2(fname):
    card = mongo.db.cards.find_one({'fname':fname})

    html = render_template("pdf_approach2.html",card = card)
    return render_pdf(HTML(string=html))
    #return render_pdf(HTML(string=html),download_filename=fname+".pdf")


    #use below line if you want html page
    #return render_template("pdf_approach2.html",card = card)


if __name__ == '__main__':
    app.secret_key = "sdfhneksj"
    app.run(debug=True)