from flask import Flask, render_template,jsonify,request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

#for /search route, might want to have data = request.form.get('home-search'), 
# so that user can directly start search on home and redirect to /search

if __name__ == "__main__":
    app.run(debug=True)