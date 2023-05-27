from flask import Flask, render_template,jsonify,request
import schedule
import time
from scripts.linear_reg_pred import *
from scripts.scraper import *
from database import engine
from sqlalchemy.sql import text
import sass

app = Flask(__name__)

def recompile_sass():
    sass.compile(dirname=('static/scss', 'static/css'))

@app.route('/', methods=['GET', 'POST'])
def home():
    recompile_sass()
    page_name="home"
    return render_template('home.html',page_name=page_name)

@app.route('/login', methods=['GET','POST'])
def login():
    recompile_sass()
    page_name="login"
    return render_template('login.html',page_name=page_name)

@app.route('/register', methods=['GET','POST'])
def register():
    recompile_sass()
    page_name="register"
    return render_template('register.html',page_name=page_name)

def user_to_db(email,password,username):
    with engine.connect() as conn:
        sql = conn.execute(text(f"insert into User (email, username, password) VALUES('{email}', '{username}', md5('{password}'));"))

@app.route('/send_data', methods = ['POST'])
def send_data():
    recompile_sass()
    email = request.form['register-email']
    password = request.form['register-password']
    username = request.form['register-username']
    user_to_db(email,password,username)
    page = "send_data"
    return render_template('send_data.html',page_name = page)

#Note, Will also need a /logout route for logging out, i think a html page still needed? idk need further research.

#Will need integration with user, for example, the link should be like /history/<username> or something like that
#for this route will be a temporary link route
#also, needed to have if user authenticated, means if the user logged in or not. if no or not the user, then cant get into the page.
@app.route('/history',methods=['GET'])
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


@app.route('/search',methods=['GET'])
def search():
    recompile_sass()
    page_name = "search"
    return render_template("search.html", page_name=page_name)


@app.route('/inventory',methods=['GET'])
def inventory():
    recompile_sass()
    page_name = "inventory"
    return render_template("inventory.html", page_name=page_name)

@app.route('/detail', methods = ['GET'])
def detail():
    recompile_sass()
    return render_template('detail.html',page_name = "detail")


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
