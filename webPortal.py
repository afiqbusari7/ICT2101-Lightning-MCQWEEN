from functools import wraps
import os
from werkzeug.utils import secure_filename
import mysql.connector
import requests
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, RadioField, EmailField, IntegerField
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret123'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Config MYSQL
# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'mydb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(app)


#Register forms
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
        quizScore = 0
        quizProgress = 0
        tutorialProgress = 0

        # Create Cursor
        cur = mysql.connection.cursor()

        if accountType == 1:  # admin
            email_value = cur.execute("SELECT email FROM admin WHERE email=%s", [email])

            if email_value > 0:
                flash("User is already registered", 'danger')
                redirect(url_for('index'))
                return render_template('register.html', form=form)


            else:
                cur.execute("INSERT INTO admin(email, password, accountType, accountStatus) VALUES(%s, %s,%s,%s)",
                            (email, password, accountType, accountStatus))
        else:

            email_value = cur.execute("SELECT email FROM student WHERE email=%s", [email])


            if email_value > 0:
                flash("User is already registered", 'danger')
                redirect(url_for('index'))
                return render_template('register.html', form=form)


            else:
                cur.execute(
                    "INSERT INTO Student(email, password, accountType, accountStatus, quizScore, quizProgress,tutorialProgress) VALUES (%s,%s,%s,%s,%s,%s,%s)",
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
        result = cur1.execute("SELECT * FROM admin WHERE email = %s", [email])
        print("result:", result)
        result_student = cur.execute("SELECT * FROM Student WHERE email = %s", [email])
        print("result_student:", result_student)

        if result > 0:
            # Get stored hash
            data = cur1.fetchone()
            # print("data:", data)
            # print(data['password'])
            password = data['password']
            accType = data['accountType']
            accStatus = data['accountStatus']
            if accStatus == 0:
                error = 'Invalid Login'
                return render_template('login.html', error=error)

            # Compare Password
            if sha256_crypt.verify(password_candidate, password):
                app.logger.info('PASSWORD MATCHED')
                # Pass
                session['logged_in'] = True
                session['email'] = email
                session['accType'] = accType
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
            # print("data:", data)
            password = data['password']
            accType = data['accountType']
            accStatus = data['accountStatus']
            if accStatus == 0:
                error = 'Invalid Login'
                return render_template('login.html', error=error)

            # Compare Password
            if sha256_crypt.verify(password_candidate, password):
                app.logger.info('PASSWORD MATCHED')
                # Pass
                session['logged_in'] = True
                session['email'] = email
                session['accType'] = accType
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

#checks user if is admin
def is_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        # print(session)
        if session['accType'] == 1:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('student_dashboard'))

    return wrap

#checks if user is logged in as amdin
def is_loggedAdmin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        # print(session)
        if session['accType'] == 1:
            return redirect(url_for('dashboard'))
        else:
            return f(*args, **kwargs)


    return wrap

#check is user is student
def is_student(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        # print(session)
        if session['accType'] == 1:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('student_dashboard'))

    return wrap


# direct the home page accessibility
@app.route('/')
@is_loggedAdmin
@is_student
def index():
    return render_template('home.html')






# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out ', 'success')
    return redirect(url_for('login'))

#studeent form
class createStudentForm(Form):
    email = StringField('Email', [validators.Email()])
    password = PasswordField('Password',
                             [validators.DataRequired(),
                              validators.EqualTo('confirm', message='Passwords do not match')
                              ])
    confirm = PasswordField('Confirm Password')
    accountType = IntegerField('AccountType', [validators.number_range(min=0, max=1, message="Only 1 or 0 is allowed")])


# AdminDashboard
@app.route('/dashboard', methods=['GET', 'POST'])
@is_logged_in
@is_admin
def dashboard():
    # Create cursor
    cur = mysql.connection.cursor()

    # Show articles only from the user logged in
    result = cur.execute("SELECT * FROM student")

    studentDetails = cur.fetchall()

    if result > 0:
        form = createStudentForm(request.form)
        if request.method == 'POST' and form.validate():
            email = form.email.data
            password = sha256_crypt.encrypt(str(form.password.data))
            accountType = form.accountType.data
            accountStatus = 1
            quizScore = 0
            quizProgress = 0
            tutorialProgress = 0
            # Create Cursor
            cur = mysql.connection.cursor()

            if accountType == 0:
                email_value = cur.execute("SELECT email FROM student WHERE email=%s", [email])
                if email_value > 0:
                    flash("User is already registered", 'danger')
                    redirect(url_for('index'))
                    return render_template('register.html', form=form)
                else:
                    cur.execute(
                        "INSERT INTO Student(email, password, accountType, accountStatus, quizScore, quizProgress,tutorialProgress) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                        (email, password, accountType, accountStatus, quizScore, quizProgress, tutorialProgress))
            else:
                email_value = cur.execute("SELECT email FROM admin WHERE email=%s", [email])
                if email_value > 0:
                    flash("User is already registered", 'danger')
                    redirect(url_for('index'))
                    return render_template('register.html', form=form)
                else:
                    cur.execute(
                        "INSERT INTO admin(email, password, accountType, accountStatus) VALUES (%s,%s,%s,%s)",
                        (email, password, accountType, accountStatus))
            # Commit to DB
            mysql.connection.commit()

            # Close Connection
            cur.close()

            flash("User Created", 'success')

            redirect(url_for('dashboard'))
        return render_template('dashboard.html', data=studentDetails, form=form)
    else:
        msg = 'No Students Found'
        return render_template('dashboard.html', msg=msg)


# Edit Student Form Class
class EditAccountForm(Form):
    # email = StringField('Email', [validators.Email()])
    password = PasswordField('Password',
                             [validators.DataRequired(),
                              validators.EqualTo('confirm', message='Passwords do not match')
                              ])
    confirm = PasswordField('Confirm Password')
    # accountType = IntegerField('AccountType', [validators.number_range(min=0, max=0, message="Only 0 is allowed")])
    # accountStatus = IntegerField('AccountStatus', [validators.number_range(min=0, max=1, message="Only 1 is allowed")])


# Edit Accounts
@app.route('/edit_accounts/<string:id>', methods=['GET', 'POST'])
@is_logged_in
@is_admin
def edit_accounts(id):
    # Create cursor
    form = EditAccountForm(request.form)
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM student WHERE studentID = %s", [id])
    admin = cur.fetchone()
    if request.method == 'POST' and form.validate():
        password = sha256_crypt.encrypt(str(form.password.data))
        cur.execute("UPDATE student SET password=%s WHERE studentID=%s", (password, [id]))
        # Commit to DB
        mysql.connection.commit()

        # Close Connection
        cur.close()
        flash('Password Updated', 'success')
        return redirect(url_for('dashboard'))
    return render_template('edit_accounts.html', form=form)

#Update User account
@app.route("/update_accounts/<string:id>", methods=['GET'])
@is_logged_in
@is_admin
def update_account(id):
    # Create cursor
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM student WHERE studentID = %s", [id])
    record = cur.fetchone()
    if (record['accountStatus']) == 0:
        result = cur.execute("UPDATE student SET accountStatus = 1 WHERE studentID=%s", [id])
    else:
        result = cur.execute("UPDATE student SET accountStatus = 0 WHERE studentID=%s", [id])

    # Commit to DB
    mysql.connection.commit()
    # Close connection
    cur.close()
    flash('Profile Updated', 'success')
    return redirect(url_for('dashboard'))


###Student dashboard
@app.route("/student_dashboard")
@is_logged_in
def student_dashboard():
    # Create cursor
    cur = mysql.connection.cursor()

    # Show articles only from the user logged in
    result = cur.execute("SELECT * FROM student where email= %s", [session['email']])



    studentDetails = cur.fetchall()

    if result > 0:
        return render_template('student_dashboard.html', data=studentDetails)
    else:
        msg = 'No Student Found'
        return render_template('student_dashboard.html', msg=msg)
    # Close connection
    cur.close()


# Map Dashboard for admin
@app.route('/mapDashboard')
@is_logged_in
@is_admin
def mapDashboard():
    # Lists the images in the static image folder for html
    maps = os.listdir('static/map')
    mapsList = ['map/' + file for file in maps]
    return render_template('mapDashboard.html', maps=mapsList)


# Function to check against allowed extensions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Generates BLOB Data from image
def mapToBinary(map):
    with open(map, 'rb') as file:
        binaryData = file.read()
    return binaryData


# Uses BLOB Data to create map picture
def write_file(data, filename):
    with open(filename, 'wb') as file:
        file.write(data)


# Upload Map Function
@app.route('/uploadMap', methods=['GET', 'POST'])
@is_logged_in
@is_admin
def uploadMap():
    if request.method == 'POST':
        # Checks if there is a file being uploaded
        if 'file' not in request.files:
            flash('No file', 'danger')
            return redirect(url_for('mapDashboard'))

        f = request.files['file']
        if f.filename == '':
            flash('No Selected File', 'danger')
            return redirect(url_for('mapDashboard'))
        # Checks if extension is valid
        if f and allowed_file(f.filename):
            # Saves file into static/image folder and creates new map entry in db
            f.save(os.path.join('static/map', secure_filename(f.filename)))
            mapData = mapToBinary('static/map/' + f.filename)
            # write_file(mapBLOB, 'static/image/'+f.filename)
            mapName = f.filename
            # Create Cursor
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO maps(mapData,mapName) VALUES(%s,%s)",
                        (mapData, mapName))
            # Commit to DB
            mysql.connection.commit()
            # Close Connection
            cur.close()

            flash("Map Uploaded", 'success')
            return redirect(url_for('mapDashboard'))
        else:
            flash("Error Uploading Map", 'danger')
            return redirect(url_for('mapDashboard'))
    return redirect(url_for('mapDashboard'))

#learning page
@app.route('/learningPage')
@is_logged_in
def learningPage():
    return render_template('learningPage.html')

#quiz page
@app.route('/quizPage')
@is_logged_in
def quizPage():
    return render_template('quizPage.html')

#free style
@app.route('/freestylePage')
@is_logged_in
def freestylePage():
    return render_template('freestylePage.html')


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)
