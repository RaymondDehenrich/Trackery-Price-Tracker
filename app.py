from flask import Flask, render_template, jsonify, request, session, flash, redirect, url_for, make_response
import schedule
import time
from scripts.linear_reg_pred import *
from scripts.scraper import *
from database import engine
from sqlalchemy.sql import text
import sass
import tokpedscrape
import lazadascrape
import hashlib

app = Flask(__name__)
app.config['SECRET_KEY'] = 'djasdasjdabakbfabhfibaif    '

@app.route('/')
def home():
    recompile_sass()
    return render_template('home.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route('/login/')
@app.route('/login/<success>')
def login(success=None):
    if "email" in session: # auth
        return redirect(url_for("home"))
    recompile_sass()
    return render_template('login.html', success = success=="success")

@app.route('/login/form', methods=['POST'])
def loginform():
    if "email" in session: # auth
        return redirect(url_for("home"))
    email = request.form.get('login-email')
    password = request.form.get('login-password')
    #encode password
    pass_encode =hashlib.md5(password.encode())
    pass_final = pass_encode.hexdigest()
    # print(pass_final)
    # print(pass_check(email)[0])
    # cek email sm password di database
    if email_check(email) and (pass_final == pass_check(email)[0]):
        #cek password
        # di redirect ke login
        session['email'] = email
        return redirect(url_for("home"))
    else:
        # fail, login ulang
        flash('Invalid email or password. Please try again.', 'error')
        return redirect(url_for("login"))

@app.route('/register/')
@app.route('/register/<code>')
def register(code=None):
    if "email" in session: # auth
        return redirect(url_for("home"))
    recompile_sass()
    return render_template('register.html', code=code)

@app.route('/register/form', methods=['POST'])
def registerform():
    if "email" in session: # auth
        return redirect(url_for("home"))

    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    confirmpassword = request.form['confirmpassword']
    terms = "terms" in request.form and request.form["terms"] == "on"
    privacy = "privacy" in request.form and request.form["privacy"] == "on"

    validation_result = validation(email, username, password, confirmpassword, terms, privacy)
    if validation_result != "ok":
        return redirect(url_for("register", code=validation_result))
    else:
        user_to_db(email,password,username)
        return redirect(url_for("login", success = "success"))

# Buat JS
@app.route('/register/form/validation', methods=['POST'])
def registerformvalidation():
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    confirmpassword = request.form['confirmpassword']
    terms = "terms" in request.form and request.form["terms"] == "on"
    privacy = "privacy" in request.form and request.form["privacy"] == "on"

    response = make_response(
        validation(email, username, password, confirmpassword, terms, privacy),
        200
    )
    response.mimetype = "text/plain"
    return response

def validation(email, username, password, confirmpassword, terms, privacy):
    if not len(email) or not len(username) or not len(password) or not len(confirmpassword):
        return "blank"
    if not terms or not privacy:
        return "accept"
    if not email.endswith("@gmail.com"):
        return "email"
    if len(password) < 5:
        return "pwlen"
    if password != confirmpassword:
        return "pwmismatch"
    if len(email_check(email)):
        return "dupeemail"
    return "ok"

def add_item_temp(name, image, link, price, id):
    with engine.connect() as conn:
        sql = conn.execute(text(f"insert INTO item_temp(itemname, image, link, Latest_price, UserId) VALUES('{name}' ,'{image}', '{link}','{price}','{id}');"))

def add_item_real(name, image, link, price, id):
    with engine.connect() as conn:
        sql = conn.execute(text(f"insert INTO item(itemname, image, link, Latest_price, UserId) VALUES('{name}' ,'{image}', '{link}','{price}','{id}');"))

def check_email_userid(email):
    with engine.connect() as conn:
        sql = conn.execute(text(f"select userid from User where email = '{email}';"))
        id = []
        for row in sql.all():
            id.append(row._mapping['userid'])
        return id
    
client_dict = []
client_dict_lazada = []
def add_to_client(item):
    global client_dict
    client_dict = item

def add_to_client_lazada(item):
    global client_dict_lazada
    client_dict_lazada = item

def add_to_db(index):
    item = client_dict[index]
    price = item['price']
    price = price[2:]
    int_price = int(price.replace('.',''))
    add_item_real(item['name'], item['img_src'], item['link'], int_price, check_email_userid(session['email'])[0])

def add_to_db_fromlazada(index):
    item = client_dict_lazada[index]
    price = item['price']
    price = price[2:]
    int_price = int(price.replace('.',''))
    add_item_real(item['name'], item['img_src'], item['link'], int_price, check_email_userid(session['email'])[0])

@app.route('/search')
def search():
    client_dict.clear()
    client_dict_lazada.clear()
    recompile_sass()
    page_name = "search"
    abc = request.values.get('query')
    tokopedia = searchTokopedia(abc) if abc else dict()
    add_to_client(tokopedia)
    lazada = searchLazada(abc) if abc else dict()
    add_to_client_lazada(lazada)
    return render_template("search.html", tokopedia=tokopedia, query = abc, lazada=lazada)

@app.route('/search?query=<query>/<int:index>')
def searchindex(query, index):
    recompile_sass()
    print("ini tokped: ")
    if 'email' in session:
        add_to_db(index)
    else:
        flash("Please log in to add item",'warning')
    client_dict.clear()
    client_dict_lazada.clear()
    recompile_sass()
    page_name = "search"
    tokopedia = searchTokopedia(query) if query else dict()
    add_to_client(tokopedia)
    lazada = searchLazada(query) if query else dict()
    add_to_client_lazada(lazada)
    return render_template("search.html", page_name=page_name, query = query, tokopedia=tokopedia, lazada=lazada)

@app.route('/search?query=<query>/<int:index>/laz')
def searchindexlaz(query, index):
    recompile_sass()
    print("ini lazada")
    add_to_db_fromlazada(index)
    client_dict.clear()
    client_dict_lazada.clear()
    recompile_sass()
    page_name = "search"
    tokopedia = searchTokopedia(query) if query else dict()
    add_to_client(tokopedia)
    lazada = searchLazada(query) if query else dict()
    add_to_client_lazada(lazada)
    return render_template("search.html", page_name=page_name, query = query, tokopedia=tokopedia, lazada=lazada)

def inventory_check(email):
    id = check_email_userid(email)
    with engine.connect() as conn:
        sql = conn.execute(text(f"select  itemname, image, link, latest_price  from item i JOIN User u ON i.UserID = u.UserID where u.UserID = {id[0]}"))
        item = []
        for row in sql.all():
            item.append(row)
        return item


@app.route('/inventory')
def inventory():
    recompile_sass()
    if 'email' in session:
        items = inventory_check((session['email']))
    else:
        items = None
    return render_template("inventory.html", item = items)

@app.route('/detail')
def detail():
    recompile_sass()
    return render_template('detail.html')


#Note, Will also need a /logout route for logging out, i think a html page still needed? idk need further research.

#Will need integration with user, for example, the link should be like /history/<username> or something like that
#for this route will be a temporary link route
#also, needed to have if user authenticated, means if the user logged in or not. if no or not the user, then cant get into the page.
@app.route('/history')
def history():
    recompile_sass()

    #added temporary list for history, should be integrated with database

    #ASSUMPTION
    #1. only have 5 variable each and every variable is filled.
    #2. has already been sorted according to time.
    #3. everything other than history-id is string.
    history_list = [
        {
        'history-id':1,
        'history-search':'bakso',
        'average-price':'Rp.40.000',
        'time': '13:20',
        'date': '20/04/2023'
        },
        {
        'history-id':2,
        'history-search':'pangsit',
        'average-price':'Rp.30.000',
        'time': '13:40',
        'date': '20/04/2025'
        },
        {
        'history-id':3,
        'history-search':'keyboard',
        'average-price':'Rp.400.000',
        'time': '6:50',
        'date': '20/04/2026'
        }
    ]
    return render_template('history.html',history_list=history_list)


def pass_check(em):
    with engine.connect() as conn:
        sql = conn.execute(text(f"select password from User WHERE email= '{em}'"))
        passvalid = []
        for row in sql.all():
            passvalid.append(row._mapping['password'])
        return passvalid

def searchTokopedia(query):
    newscrape = tokpedscrape.scrapeTokopedia(query)
    return newscrape

def searchLazada(query):
    newscrape1 = lazadascrape.scrapeLazada(query)
    return newscrape1

def recompile_sass():
    sass.compile(dirname=('static/scss', 'static/css'))

def user_to_db(email,password,username):
    with engine.connect() as conn:
        sql = conn.execute(text(f"insert into User (email, username, password) VALUES('{email}', '{username}', md5('{password}'));"))

def email_check(em):
    with engine.connect() as conn:
        sql = conn.execute(text(f"select email from User WHERE email = '{em}'"))
        emailvalid = []
        for row in sql.all():
            emailvalid.append(row._mapping['email'])
        return emailvalid

#for /search route, might want to have data = request.form.get('home-search'),
# so that user can directly start search on home and redirect to /search
'''
schedule.every().day.at("12:00").do(dailyScrape)

def start_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)
'''
if __name__ == "__main__":
    '''
    import threading
    scheduler_thread = threading.Thread(target=start_scheduler)
    scheduler_thread.start()
    '''
    recompile_sass()
    '''BUAT RUN KE WEB'''
    app.run(host='0.0.0.0',debug=True)












