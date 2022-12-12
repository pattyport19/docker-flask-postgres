import time
from flask import Flask, render_template, flash, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy


DBUSER = 'marco'
DBPASS = 'foobarbaz'
DBHOST = 'db'
DBPORT = '5432'
DBNAME = 'testdb'


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'.format(
        user=DBUSER,
        passwd=DBPASS,
        host=DBHOST,
        port=DBPORT,
        db=DBNAME)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'foobarbaz'


db = SQLAlchemy(app)

class userr(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    userName = db.Column(db.String(100))
    password = db.Column(db.String(50))
    email = db.Column(db.String(200))

    def __init__(self, userName, password, email):
        self.userName = userName 
        self.password = password
        self.email = email

class Box(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('userr.id'))
    ip = db.Column(db.String(50))
    threadHum = db.Column(db.Integer,nullable=False)

    def __init__(self,id, userId, ip, threadHum):
        self.id = id
        self.userId = userId 
        self.ip=ip
        self.threadHum  = threadHum 

class students(db.Model):
    id = db.Column('student_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    addr = db.Column(db.String(200))

    def __init__(self, name, city, addr):
        self.name = name
        self.city = city
        self.addr = addr


def database_initialization_sequence():
    db.create_all()
    test_rec = students(
            'John Doe',
            'Los Angeles',
            '123 Foobar Ave')

    test_user = userr('user1', '', 'user@user.com')
    test_box = Box(101,1,'192.168.1.131', 55.5)

    db.session.add(test_user)
    db.session.add(test_box)

    db.session.add(test_rec)
    db.session.rollback()
    db.session.commit()


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['city'] or not request.form['addr']:
            flash('Please enter all the fields', 'error')
        else:
            student = students(
                    request.form['name'],
                    request.form['city'],
                    request.form['addr'])

            db.session.add(student)
            db.session.commit()
            flash('Record was succesfully added')
            return redirect(url_for('home'))
    return render_template('show_all.html', students=students.query.all())

@app.route('/data', methods = ['GET'])
def view_data_from_boxes():
    return render_template('ttt.html')


@app.route('/hum/<box_id>/<hum>', methods = ['GET','POST'])
def  set_hum(box_id, hum):
    if request.method == 'POST':
        box = Box.query.filter_by(id=box_id).first()
        box.threadHum = hum
        db.session.commit()

    #enviar valor novo para o pi
    
        print("funcioneiiiiiii")
        return 'OKK'


if __name__ == '__main__':
    dbstatus = False
    while dbstatus == False:
        try:
            db.create_all()
        except:
            time.sleep(2)
        else:
            dbstatus = True
    database_initialization_sequence()
    app.run(debug=True, host='0.0.0.0')