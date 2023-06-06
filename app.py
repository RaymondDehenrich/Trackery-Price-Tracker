from flask import Flask, render_template, jsonify, request, session, flash, redirect, url_for
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

@app.route('/login')
def login():
    recompile_sass()
    page_name = "login"
    return render_template('login.html')

def pass_check(em):
    with engine.connect() as conn:
        sql = conn.execute(text(f"select password from User WHERE email= '{em}'"))
        passvalid = []
        for row in sql.all():
            passvalid.append(row._mapping['password'])
        return passvalid

@app.route('/login/form', methods=['POST'])
def loginform():
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

@app.route('/register')
def register():
    recompile_sass()
    return render_template('register.html', verifp = 0)

@app.route('/register/form', methods=['POST'])
def registerform():
    page = "send_data"
    email = request.form['register-email']
    password = request.form['register-password']
    username = request.form['register-username']
    bb = email_check(email)
    if not bb:
        user_to_db(email,password,username)
        return render_template('send_data.html',page_name = page)
    else:
        return render_template('register.html',page_name = "register", verifp = 1)

@app.route('/search')
def search():
    recompile_sass()
    page_name = "search"
    abc = request.values.get('query')
    tokopedia = searchTokopedia(abc) if abc else dict()
    lazada = dict()#searchLazada(abc) if abc else dict()
    return render_template("search.html", tokopedia=tokopedia, lazada=lazada)

@app.route('/inventory')
def inventory():
    recompile_sass()
    return render_template("inventory.html")

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









