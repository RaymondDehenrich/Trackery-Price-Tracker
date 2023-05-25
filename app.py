from flask import Flask, render_template,jsonify,request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    page_name="home"
    return render_template('home.html',page_name=page_name)

@app.route('/login', methods=['GET','POST'])
def login():
    page_name="login"
    return render_template('login.html',page_name=page_name)

@app.route('/register', methods=['GET','POST'])
def register():
    page_name="register"
    return render_template('register.html',page_name=page_name)

#Note, Will also need a /logout route for logging out, i think a html page still needed? idk need further research.

#Will need integration with user, for example, the link should be like /history/<username> or something like that
#for this route will be a temporary link route
#also, needed to have if user authenticated, means if the user logged in or not. if no or not the user, then cant get into the page.
@app.route('/history',methods=['GET'])
def history():
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


#for /search route, might want to have data = request.form.get('home-search'), 
# so that user can directly start search on home and redirect to /search

if __name__ == "__main__":
    app.run(debug=True)