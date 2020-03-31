from flask import Flask, render_template, url_for, request
import sqlite3
from feed import Feed

morning_feed = None
night_feed = None

app = Flask(__name__)
conn = sqlite3.connect('cat.db')
c = conn.cursor()

#creating feedtimes table if it doesn't exist
c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='feedtimes'; ''')
if not c.fetchone()[0]==1:
    c.execute(''' CREATE TABLE feedtimes (morning text, night text); ''')
    conn.commit()
    conn.close()


@app.route('/')
def home():
    paw_pic = url_for('static', filename='paw_cursor.png')
    pork_pic = url_for('static', filename='porko.png')
    bootstrap_js = url_for('static', filename='bootstrap.bundle.min.js')
    jquery_js = url_for('static', filename='jquery.min.js')
    bootstrap_css = url_for('static', filename='bootstrap.min.css')
    return render_template('index.html', paw_pic=paw_pic, pork_pic=pork_pic, bootstrap_js=bootstrap_js, bootstrap_css=bootstrap_css, jquery_js=jquery_js)

@app.route('/setfeed', methods=['GET', 'POST'])
def set_feed():
    if request.method == 'POST':
        global morning_feed
        global night_feed
        # TODO: lookup best practices for this
        conn = sqlite3.connect('cat.db')
        c = conn.cursor()
        # delete previous times from database
        c.execute('''DELETE FROM feedtimes;''')
        # add new times to database
        c.execute('''INSERT INTO feedtimes VALUES (?,?);''', [request.form['morning'], request.form['night']])
        conn.commit()
        conn.close()
        # delete previous Feed jobs
        if(morning_feed and night_feed):
            morning_feed.set()
            night_feed.set()
        # create new feed jobs
        morning_feed = Feed(request.form['morning']).start_schedule()
        night_feed = Feed(request.form['night']).start_schedule()

    conn = sqlite3.connect('cat.db')
    c = conn.cursor()
    # delete previous times from database
    c.execute('''select * from feedtimes; ''')
    times = c.fetchone()
    conn.commit()
    conn.close()
    m_time = times[0]
    n_time = times[1]
    paw_pic = url_for('static', filename='paw_cursor.png')
    bootstrap_js = url_for('static', filename='bootstrap.bundle.min.js')
    jquery_js = url_for('static', filename='jquery.min.js')
    bootstrap_css = url_for('static', filename='bootstrap.min.css')
    return render_template('setfeed.html', paw_pic=paw_pic, bootstrap_js=bootstrap_js, bootstrap_css=bootstrap_css, jquery_js=jquery_js, m_time=m_time, n_time=n_time)
    

@app.route('/feedlog')
def feed_log():
    paw_pic = url_for('static', filename='paw_cursor.png')
    bootstrap_js = url_for('static', filename='bootstrap.bundle.min.js')
    jquery_js = url_for('static', filename='jquery.min.js')
    bootstrap_css = url_for('static', filename='bootstrap.min.css')
    return render_template('feedlog.html', paw_pic=paw_pic, bootstrap_js=bootstrap_js, bootstrap_css=bootstrap_css, jquery_js=jquery_js)

@app.route('/feednow')
def feed_now():
    print("TODO: FEED NOW")
    return "True"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
