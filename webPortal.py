from functools import wraps
import mysql.connector
import requests
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, RadioField, EmailField, IntegerField
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret123'

# Config MYSQL
# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Password123!'
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
    accountType = IntegerField('AccountType', [validators.number_range(min=0, max=1, message="Only 1 or 0 is allowed")])
    accountStatus = IntegerField('AccountStatus', [validators.number_range(min=0, max=1, message="Only 1 is allowed")])


# Admin register  form class
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))
        accountType = form.accountType.data
        accountStatus = form.accountStatus.data
        quizScore =0
        quizProgress = 0
        tutorialProgress = 0


        # Create Cursor
        cur = mysql.connection.cursor()

        if accountType==1: #admin
            email_value = cur.execute("SELECT email FROM admin WHERE email=%s", [email])

            if email_value > 0:
                flash("User is already registered", 'success')
                redirect(url_for('index'))
                return render_template('register.html', form=form)


            else:
                cur.execute("INSERT INTO admin(email, password, accountType, accountStatus) VALUES(%s, %s,%s,%s)",
                            (email, password, accountType, accountStatus))
        else:
            email_value = cur.execute("SELECT email FROM Student WHERE email=%s", [email])

            if email_value > 0:
                flash("User is already registered", 'success')
                redirect(url_for('index'))
                return render_template('register.html', form=form)


            else:
                cur.execute("INSERT INTO Student(email, password, accountType, accountStatus, quizScore, quizProgress,tutorialProgress) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                            (email, password, accountType, accountStatus, quizScore, quizProgress, tutorialProgress))

        # Commit to DB
        mysql.connection.commit()

        # Close Connection
        cur.close()

        flash("User is Registered", 'success')

        redirect(url_for('login'))
    return render_template('register.html', form=form)


# user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        email = request.form['email']
        password_candidate = request.form['password']
        # Create Cursor
        cur1 = mysql.connection.cursor()
        cur = mysql.connection.cursor()

        # Get email
        result = cur1.execute("SELECT * FROM admin WHERE email = %s", [email] )
        print("result:", result)
        result_student = cur.execute("SELECT * FROM Student WHERE email = %s", [email] )
        print("result_student:", result_student)
        
        if result > 0:
            # Get stored hash
            data = cur1.fetchone()
            print("data:",data)
            print(data['password'])
            password = data['password']

            # Compare Password
            if sha256_crypt.verify(password_candidate, password):
                app.logger.info('PASSWORD MATCHED')
                # Pass
                session['logged_in'] = True
                session['email'] = email
                flash('You are now logged in', 'success')
                return redirect((url_for('dashboard')))
            else:
                error = 'Invalid Login'
                return render_template('login.html', error=error)
            # Close Connection
            cur.close()
        elif result_student > 0:
            # Get stored hash
            data = cur.fetchone()
            print("data:",data)
            password = data['password']

            # Compare Password
            if sha256_crypt.verify(password_candidate, password):
                app.logger.info('PASSWORD MATCHED')
                # Pass
                session['logged_in'] = True
                session['email'] = email
                flash('You are now logged in', 'success')
                return redirect((url_for('student_dashboard')))
            else:
                error = 'Invalid Login'
                return render_template('login.html', error=error)

        else:
            error = 'Invalid email'
            return render_template('login.html', error=error)

    return render_template('login.html')


# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))

    return wrap


# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out ', 'success')
    return redirect(url_for('login'))


# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    # Create cursor
    cur = mysql.connection.cursor()

    # Show articles only from the user logged in
    result = cur.execute("SELECT * FROM admin")

    adminDetails = cur.fetchall()

    if result > 0:
        return render_template('dashboard.html', data=adminDetails)
    else:
        msg = 'No Articles Found'
        return render_template('dashboard.html', msg=msg)
    # Close connection
    cur.close()


# Edit Admin Form Class
class EditAdminForm(Form):
    email = StringField('Email', [validators.Email()])
    password = PasswordField('Password',
                             [validators.DataRequired(),
                              validators.EqualTo('confirm', message='Passwords do not match')
                              ])
    confirm = PasswordField('Confirm Password')
    accountType = IntegerField('AccountType', [validators.number_range(min=1, max=1, message="Only 1 is allowed")])
    accountStatus = IntegerField('AccountStatus', [validators.number_range(min=0, max=1, message="Only 1 is allowed")])


# Edit Article
@app.route('/edit_admin/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_admin(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Get article by id
    result = cur.execute("SELECT * FROM admin WHERE adminID = %s", [id])
    admin = cur.fetchone()
    cur.close()
    # Get form
    form = EditAdminForm(request.form)

    # Populate article form fields
    form.email.data = admin['email']
    form.accountStatus.data = admin['accountStatus']
    form.accountType.data = admin['accountType']

    if request.method == 'POST' and form.validate():
        email = request.form['email']
        password = request.form['password']
        accountStatus = request.form['accountStatus']
        accountType = request.form['accountType']

        # Create Cursor
        cur = mysql.connection.cursor()
        app.logger.info(email)
        # Execute
        cur.execute("UPDATE admin SET email=%s,password=%s, accountStatus= %s , accountType WHERE id=%s", (email,password,accountType,accountStatus))
        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()


        flash('Profile Updated', 'success')

        return redirect(url_for('dashboard'))
    return render_template('edit_admin.html', form=form)


###Student dashboard
@app.route("/student_dashboard")
@is_logged_in
def student_dashboard():
    # Create cursor
    cur = mysql.connection.cursor()

    # Show articles only from the user logged in
    result = cur.execute("SELECT * FROM Student where email='rainyy@gmail.com'")

    studentDetails = cur.fetchall()

    if result > 0:
        return render_template('student_dashboard.html', data=studentDetails)
    else:
        msg = 'No Articles Found'
        return render_template('student_dashboard.html', msg=msg)
    # Close connection
    cur.close()

@app.route('/learningPage')
def learningPage():
    return render_template('learningPage.html')

@app.route('/quizPage')
def quizPage():
    return render_template('quizPage.html')

@app.route('/freestylePage')
def freestylePage():
    return render_template('freestylePage.html')


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)
