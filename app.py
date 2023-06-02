from flask import Flask, render_template,jsonify,request
import schedule
import time
from scripts.linear_reg_pred import *
from scripts.scraper import *
from database import engine
from sqlalchemy.sql import text
import sass
import tokpedscrape
import lazadascrape

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
    return render_template('register.html',page_name=page_name, verifp = 0)

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

@app.route('/send_data', methods = ['POST'])
def send_data():
    recompile_sass()
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

def searchTokopedia(query):
    newscrape = tokpedscrape.scrapeTokopedia(query)
    return newscrape

def searchLazada(query):
    newscrape1 = lazadascrape.scrapeLazada(query)
    return newscrape1

@app.route('/search',methods=['GET', 'POST'])
def search():
    recompile_sass()
    page_name = "search"
    abc = request.values.get('query')
    hasil = searchTokopedia(abc)
    if(abc):
        links = []
        images = []
        names = []
        prices = []
        for items in hasil:
            links.append(items['link'])
            images.append(items['img_src'])
            names.append(items['name'])
            prices.append(items['price'])
    #print(len(links))
    hasil1 = searchLazada(abc)
    links1 = []
    images1 = []
    names1 = []
    prices1 = []
    for items in hasil1:
        links1.append(items['linke'])
        images1.append(items['img_srce'])
        names1.append(items['namee'])
        prices1.append(items['pricee'])
    if not abc:
        return render_template("search.html", page_name=page_name, notcheck = "yes")
    else:
        print(abc)
        return render_template("search.html", page_name=page_name, checked = "yes",query = abc,
                               name1 = names[0], name2 = names[1], name3 = names[2], name4 = names[3], name5 = names[4],
                               price1 = prices[0], price2 = prices[1], price3 = prices[2], price4 = prices[3], price5 = prices[4],
                               imglink1 = images[0], imglink2 = images[1], imglink3 = images[2], imglink4 = images[3], imglink5 = images[4],
                               link1 = links[0], link2 = links[1], link3 = links[2], link4 = links[3], link5 = links[4],
                               namee1 = names1[0], namee2 = names1[1], namee3 = names1[2], namee4 = names1[3], namee5 = names1[4],
                               pricee1 = prices1[0], pricee2 = prices1[1], pricee3 = prices1[2], pricee4 = prices1[3], pricee5 = prices1[4],
                               imglinke1 = images1[0], imglinke2 = images1[1], imglinke3 = images1[2], imglinke4 = images1[3], imglinke5 = images1[4],
                               linke1 = links1[0], linke2 = links1[1], linke3 = links1[2], linke4 = links1[3], linke5 = links1[4]
                               )
    
# hasil = searchLazada("ayam")
# print(hasil)

    






@app.route('/search_empty', methods = ['GET', 'POST'])
def search_empty():
    recompile_sass()
    page_name = "search_empty"
    return render_template("search_empty.html", page_name=page_name)

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









