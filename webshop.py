# all the imports
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import psycopg2
from psycopg2.extras import NamedTupleConnection, NamedTupleCursor

app = Flask(__name__)

app.config.from_pyfile('config.cfg')


def dbconnect(func):
    def newfunc(*args, **kwargs):
        conn = app.config['DBENGINE'].connect(app.config['DBPARAMS'], cursor_factory=NamedTupleCursor)
        cursor = conn.cursor()
        returnvalue = func(*args, cursor=cursor, **kwargs)
        conn.commit()
        conn.close()
        return returnvalue
    newfunc.__name__ = func.__name__
    return newfunc



@app.route('/')
def home():
         return render_template('home.html',loginState = loginState(),myAcount = myAcount())

@app.route('/equipment')
def equipment():
         return render_template('equipment.html',loginState = loginState(),myAcount = myAcount())

@app.route('/games')
def games():
         return render_template('games.html',loginState = loginState(),myAcount = myAcount())

@app.route('/merchandise')
def merchandise():
         return render_template('merchandise.html',loginState = loginState(),myAcount = myAcount())

@app.route('/about')
def about():
         return render_template('about.html',loginState = loginState(),myAcount = myAcount())

@app.route('/contact')
def contact():
         return render_template('contact.html',loginState = loginState(),myAcount = myAcount())

@app.route('/Login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            return redirect(url_for('welcome'))
    return render_template('Login.html',error = error,loginState = loginState(),myAcount = myAcount())


@app.route('/layout')
def layout():
         return render_template('layout.html',loginState = loginState(),myAcount = myAcount())

@app.route('/Logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))

@app.route('/welcome')
def welcome():
        return render_template('welcome.html',loginState = loginState(),myAcount = myAcount())

@app.route('/myAcount')
def myAcount():
        return render_template('myAcount.html',loginState = loginState(),myAcount = myAcount())

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html',loginState = loginState(),myAcount = myAcount())




def loginState():
    string = ""
    if not session.get('logged_in'):
        string = 'Login'
    else:
        string = "Logout"
    return string

def myAcount():
    string = ''
    if not session.get('logged_in'):
        string = ''
    else:
        string = '<a href="/myAcount"><span>My Acount</span></a>'
    return string



if __name__ == '__main__':
    app.run(debug=True)