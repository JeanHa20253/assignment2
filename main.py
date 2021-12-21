import smtplib
from flask_bootstrap import Bootstrap
from flask import *
from flask_sqlalchemy import SQLAlchemy
from wtf_form import *
from flask_ckeditor import CKEditor
import os

GMAIL_ACC='testing.minhanh@gmail.com'
GMAIL_PASS='151002python()'

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

Bootstrap(app)
ckeditor= CKEditor(app)

##CREATE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///products_collection.db"

# Optional: But it will silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##CREATE TABLE
class Products(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), primary_key=False)
    intro= db.Column(db.String(250), primary_key=False)
    describe = db.Column(db.String(250), primary_key=False)
    link = db.Column(db.String(250), primary_key=False)
    link_img=db.Column(db.String(250), primary_key=False)

    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Product {self.title}>'


# CREATE RECORD

db.create_all()





@app.route('/')
def home():
    works = Products.query.all()
    return render_template('index.html', posts=works)


@app.route('/contact', methods=['POST','GET'])
def contact():
    if request.method== 'POST':
        send_mail(
            username= request.form['name'],
            message=request.form['message'],
            email=request.form['email'],
            phonenumber=request.form['number'],
            subject=request.form['subject'],

        )
        return render_template ('contact.html', subtitle_contact="I will reply as soon as possible!")
    else:
        return render_template('contact.html',subtitle_contact= "Let's get in touch!")


def send_mail(username,message,email,phonenumber,subject):
    with smtplib.SMTP('smtp.gmail.com') as con:
        con.starttls()
        con.login(user=GMAIL_ACC,
                  password=GMAIL_PASS)
        con.sendmail(
            from_addr=GMAIL_ACC,
            to_addrs='haphamminhanh2014@gmail.com',
            msg=f'Subject:!!! Mail from user: {username} about: {subject}\n\nContact information:\n'
                f'Username: {username}\nEmail: {email}\nPhone number: {phonenumber}\n'
                f'{message}'
        )


# for each portfolio:
@app.route('/portfolio/<id>')
def portfolio(id):
    return render_template('no-sidebar.html', portfolio=id)

@app.route('/boomchakalaka',methods=['POST','GET'])
def hello():
    form= ProductInfo()
    if form.validate_on_submit():
        print('success')
        new_product = Products(
            title=form.name.data,
            intro= form.intro.data,
            describe = form.describe.data,
            link =form.url.data,
            link_img =form.img_url.data
        )
        db.session.add(new_product)
        db.session.commit()
        return redirect('/')

    return render_template('post.html', subtitle_contact='Well done', form= form)


@app.route('/allworks')
def all():
    return render_template('no-sidebar.html')


if __name__ == '__main__':
    app.run(debug=True)
