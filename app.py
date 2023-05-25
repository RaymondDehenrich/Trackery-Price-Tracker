from flask import Flask, render_template,jsonify
import schedule
import time
from scripts.linear_reg_pred import *
from scripts.scraper import *

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

schedule.every().day.at("12:00").do(dailyScrape)

def start_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    import threading
    scheduler_thread = threading.Thread(target=start_scheduler)
    scheduler_thread.start()
    app.run(host='0.0.0.0',debug=True)