# all the imports
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import psycopg2
from psycopg2.extras import NamedTupleConnection, NamedTupleCursor

app = Flask(__name__)

app.config.from_pyfile('config.cfg')
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

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
@dbconnect
def home(cursor=None):
         return render_template('home.html',loginState = loginState(),myAcount = myAcount(),adminPanel = adminPanel())

@app.route('/equipment', methods=['GET', 'POST'])
@dbconnect
def equipment(cursor=None):
    error = None
    product = "equipment"
    divider = 0
    cursor.execute("SELECT id,name,price,producttype FROM products WHERE producttype = %s",(product,))
    result = cursor.fetchall()
    for res in result:
        divider +=1
    if divider > 3:
        divider = 0
    if request.method == "GET":
        if request.query_string == '':
            return render_template('equipment.html',error = error,loginState = loginState(),myAcount = myAcount(),adminPanel = adminPanel(),show = result,divider = divider)
        else:
            if session.get('logged_in'):
                productID = request.query_string
                cursor.execute("SELECT * FROM shoppingcart WHERE product_id = %s AND idshoppingcart = %s AND customer_id = %s;",(productID,session.get('cart_id'),session.get('user_id')))
                result1 = cursor.fetchone()
                if(result1 > 0):
                    error = "ERROR:you allready have this in your cart"
                    return render_template('equipment.html',error = error,loginState = loginState(),myAcount = myAcount(),adminPanel = adminPanel(),show = result,divider = divider)
                else:
                    cursor.execute("INSERT INTO shoppingcart(idshoppingcart, customer_id, product_id, quantity) VALUES (%s, %s, %s, 1);",(session.get('cart_id'),session.get('user_id'),productID))
                    error = "SUCCES:item added to your cart"
                    return render_template('equipment.html',error = error,loginState = loginState(),myAcount = myAcount(),adminPanel = adminPanel(),show = result,divider = divider)
            else:
                return redirect(url_for('login'))
    return render_template('equipment.html',error=error,loginState = loginState(),myAcount = myAcount(),adminPanel = adminPanel(),show = result,divider = divider)


@app.route('/adminPanel')
@dbconnect
def adminPanel(cursor=None):
         return render_template('adminPanel.html',error=error,loginState = loginState(),myAcount = myAcount(),adminPanel = adminPanel())

@app.route('/games', methods=['GET', 'POST'])
@dbconnect
def games(cursor=None):
    error = None
    product = "games"
    divider = 0
    cursor.execute("SELECT id,name,price,producttype FROM products WHERE producttype = %s",(product,))
    result = cursor.fetchall()
    if request.method == "GET":
        if request.query_string == '':
            return render_template('games.html',error = error,loginState = loginState(),myAcount = myAcount(),adminPanel = adminPanel(),show = result,divider = divider)
        else:
            if session.get('logged_in'):
                productID = request.query_string
                cursor.execute("SELECT * FROM shoppingcart WHERE product_id = %s AND idshoppingcart = %s AND customer_id = %s;",(productID,session.get('cart_id'),session.get('user_id')))
                result1 = cursor.fetchone()
                if(result1 > 0):
                    error = "ERROR:you allready have this in your cart"
                    return render_template('games.html',error = error,loginState = loginState(),myAcount = myAcount(),adminPanel = adminPanel(),show = result,divider = divider)
                else:
                    cursor.execute("INSERT INTO shoppingcart(idshoppingcart, customer_id, product_id, quantity) VALUES (%s, %s, %s, 1);",(session.get('cart_id'),session.get('user_id'),productID))
                    error = "SUCCES:item added to your cart"
                    return render_template('games.html',error = error,loginState = loginState(),myAcount = myAcount(),adminPanel = adminPanel(),show = result,divider = divider)
            else:        
                return redirect(url_for('login'))
        return render_template('games.html',error=error,loginState = loginState(),myAcount = myAcount(),adminPanel = adminPanel(),show = result,divider = divider)

@app.route('/merchandise', methods=['GET', 'POST'])
@dbconnect
def merchandise(cursor=None):
    error = None
    product = "merchandise"
    divider = 0
    cursor.execute("SELECT id,name,price,producttype FROM products WHERE producttype = %s",(product,))
    result = cursor.fetchall()
    for res in result:
        divider +=1
    if divider > 3:
        divider = 0
    if request.method == "GET":
            if request.query_string == '':
                return render_template('merchandise.html',error = error,loginState = loginState(),myAcount = myAcount(),adminPanel = adminPanel(),show = result,divider = divider)
            else:
                if session.get('logged_in'):
                    productID = request.query_string    
                    cursor.execute("SELECT * FROM shoppingcart WHERE product_id = %s AND idshoppingcart = %s AND customer_id = %s;",(productID,session.get('cart_id'),session.get('user_id')))
                    result1 = cursor.fetchone()
                    if(result1 > 0):
                        error = "ERROR:you allready have this in your cart"
                        return render_template('merchandise.html',error = error,loginState = loginState(),myAcount = myAcount(),adminPanel = adminPanel(),show = result,divider = divider)
                    else:
                        cursor.execute("INSERT INTO shoppingcart(idshoppingcart, customer_id, product_id, quantity) VALUES (%s, %s, %s, 1);",(session.get('cart_id'),session.get('user_id'),productID))
                        error = "SUCCES:item added to your cart"
                        return render_template('merchandise.html',error = error,loginState = loginState(),myAcount = myAcount(),adminPanel = adminPanel(),show = result,divider = divider)
                else:        
                    return redirect(url_for('login'))
               
    return render_template('merchandise.html',error=error,loginState = loginState(),myAcount = myAcount(),adminPanel = adminPanel(),show = result,divider = divider)


@app.route('/about')
@dbconnect
def about(cursor=None):
         return render_template('about.html',loginState = loginState(),myAcount = myAcount(),adminPanel = adminPanel())

@app.route('/contact')
@dbconnect
def contact(cursor=None):
         return render_template('contact.html',loginState = loginState(),myAcount = myAcount(),adminPanel = adminPanel())





@app.route('/shoppingcart', methods=['GET', 'POST'])
@dbconnect
def cart(cursor=None):
    error = None
    listqty = 0
    result = ''
    if session.get('logged_in') == None:
        error = "je bent niet ingelogt"
        return render_template('shoppingcart.html',error = error,loginState = loginState(),myAcount = myAcount(),adminPanel = adminPanel(),showCart = result,list = listqty)
    cursor.execute("SELECT p.*,s.quantity,s.product_id FROM products AS p,shoppingcart AS s WHERE s.idshoppingcart = %s AND s.customer_id = %s AND s.product_id = p.id;",(str(session.get('cart_id')),str(session.get('user_id'))))
    result = cursor.fetchall()
    if request.method == "GET":
        if request.query_string == '':
            return render_template('shoppingcart.html',error = error,loginState = loginState(),myAcount = myAcount(),adminPanel = adminPanel(),showCart = result,list = listqty)
        else:
            productID = request.query_string
            cursor.execute("""
                    DELETE FROM shoppingcart
                    WHERE idshoppingcart = %s AND customer_id = %s AND product_id = %s;""",(session.get('cart_id'),session.get('user_id'),productID))
            error = "item is successfully removed"
            return redirect(url_for('cart'))
        #cursor.execute("""
         #           UPDATE shoppingcart
          #          SET quantity=%s
           #         WHERE idshoppingcart = %s AND customer_id = %s AND product_id = %s;""",(request.form['quantity'],session.get('cart_id'),session.get('user_id'),request.form['id']))

    return render_template('shoppingcart.html',error = error,loginState = loginState(),myAcount = myAcount(),adminPanel = adminPanel(),showCart = result,list = listqty)

@app.route('/Login', methods=['GET', 'POST'])
@dbconnect
def login(cursor=None):
    error = None
    if request.method == 'POST':
        for input in request.form:
            if request.form[input] == '':
                error = "Please fill in the complete form!"
                return render_template('login.html',error = error,loginState = loginState(),myAcount = myAcount(),adminPanel = adminPanel())

        cursor.execute("SELECT id,email,password,role FROM login WHERE email = %s AND password = %s",(request.form['email'],request.form['password']))
        result = cursor.fetchone()
        if result:
            session['cart_id'] = result.id
            session['user_id'] = result.id
            session['logged_in'] = True
            session['role'] = str(result.role)                                                                                                    
            return render_template('home.html',error = error,loginState = loginState(),myAcount = myAcount(),adminPanel = adminPanel())
        else:
            error = "invalid credentials"
            return render_template('login.html',error = error,loginState = loginState(),myAcount = myAcount(),adminPanel = adminPanel())
    return render_template('Login.html',error = error,loginState = loginState(),myAcount = myAcount(),adminPanel = adminPanel())


@app.route('/layout')
@dbconnect
def layout(cursor=None):
         return render_template('layout.html',loginState = loginState(),myAcount = myAcount(),adminPanel = adminPanel())

@app.route('/Logout')
@dbconnect
def logout(cursor=None):
    session.pop('logged_in', None)
    session.pop('role', None)
    session.pop('cart_id',None)
    session.pop('user_id',None)
    return redirect(url_for('home'))

@app.route('/welcome')
@dbconnect
def welcome(cursor=None):
        return render_template('welcome.html',loginState = loginState(),myAcount = myAcount(),adminPanel = adminPanel())

@app.route('/myAcount')
@dbconnect
def myAcount(cursor=None):
        return render_template('myAcount.html',loginState = loginState(),myAcount = myAcount(),adminPanel = adminPanel())

@app.route('/register', methods=['GET', 'POST'])
@dbconnect
def register(cursor=None):
    error = None
    if request.method == 'POST':
        for input in request.form:
            if request.form[input] == '':
                error = "Please fill in the complete form!"
                return render_template('register.html',error=error,loginState = loginState(),myAcount = myAcount(),adminPanel = adminPanel())

        cursor.execute("SELECT email FROM login WHERE email = %s",(request.form['email'],))
        result = cursor.fetchone()

        if result:
            error = "This e-mail address already exists"                                                                                                       

            return render_template('register.html',error=error,loginState = loginState(),myAcount = myAcount(),adminPanel = adminPanel())

        cursor.execute("INSERT INTO login (email,password,role) VALUES(%s,%s,'user')",(request.form['email'],request.form['password']))
        cursor.execute("""
        INSERT INTO user_info(  
                gender, firstname, infix, surname, address, addressnumber, city,
             zipcode, country, telephonenumber, mobilenumber)
    VALUES (%s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s);
        """,(
            request.form['gender'],request.form['firstname'],
            request.form['infix'],request.form['surname'],
            request.form['address'],request.form['addressnumber'],
            request.form['city'],request.form['zipcode'],
            request.form['country'],request.form['telephonenumber'],
            request.form['mobilenumber']
            )
        )
        return render_template('home.html',loginState = loginState(),myAcount = myAcount(),adminPanel = adminPanel())
    return render_template('register.html',loginState = loginState(),myAcount = myAcount(),adminPanel = adminPanel())

@app.route('/adminProductManagement')
@dbconnect
def adminProductManagement(cursor=None):
        return render_template('adminProductManagement.html',loginState = loginState(),myAcount = myAcount(),adminPanel = adminPanel())

@app.route('/adminAdManagement')
@dbconnect
def adminAdManagement(cursor=None):
        return render_template('adminAdManagement.html',loginState = loginState(),myAcount = myAcount(),adminPanel = adminPanel())

@app.route('/adminUserManagement')
@dbconnect
def adminUserManagement(cursor=None):
        return render_template('adminUserManagement.html',loginState = loginState(),myAcount = myAcount(),adminPanel = adminPanel())



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



def adminPanel():
    string = ''
    test = ''
    if session.get('role') == 'admin':
        test = 'style="padding-left:10em"'
        string ="""<li class='has-sub'><a href='/adminPanel'><span>AdminPanel</span></a>
      <ul>
         <li><a href='/adminUserManagement'><span>User Control</span></a></li>
         <li><a href='/adminProductManagement'><span>Product management</span></a></li>
         <li class='last'><a href='/adminAdManagement'><span>bargain control</span></a></li>
      </ul>
   </li>"""
    else:
        string = ''
    return str(string)






if __name__ == '__main__':
    app.run(debug=True)
