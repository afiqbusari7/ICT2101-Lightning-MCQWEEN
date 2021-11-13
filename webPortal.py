import requests
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, RadioField, EmailField
from passlib.hash import sha256_crypt

app = Flask(__name__)

# Config MYSQL
# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'mydb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(app)

Articles = Articles()


# direct the pages
@app.route('/')
def index():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/articles')
def articles():
    return render_template('articles.html', articles=Articles)


@app.route('/article/<string:id>')
def article(id):
    return render_template('article.html', id=id)


class RegisterForm(Form):
    email = StringField('Email', [validators.Email()])
    password = PasswordField('Password',
                             [validators.DataRequired(),
                              validators.EqualTo('confirm', message='Passwords do not match')
                              ])
    confirm = PasswordField('Confirm Password')
    accountType = StringField('accountType', [validators.Length(min=1, max=1)])
    accountStatus = StringField('accountStatus', [validators.Length(min=1, max=1)])


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))
        accountType = form.accountType.data
        accountStatus = form.accountStatus.data

        # Create Cursor
        cur = mysql.connection.cursor()
        email_value = cur.execute("SELECT email FROM admin WHERE email=%s", [email])
        if email_value > 0:
            flash("User is already registered", 'success')
            redirect(url_for('index'))
            return render_template('register.html', form=form)


        else:
            cur.execute("INSERT INTO admin(email,password,accountType,accountStatus) VALUES(%s, %s,%s,%s)",
                        (email, password, accountType, accountStatus))

        # Commit to DB
        mysql.connection.commit()

        # Close Connection
        cur.close()

        flash("User is Registered", 'success')

        redirect(url_for('index'))
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)
