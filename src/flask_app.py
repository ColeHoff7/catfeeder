from flask import Flask, render_template, url_for, request
import sqlite3
from feed import Feed, one_time_feed
import datetime
#import os, re
#this is absolutely horrible code, don't judge me
app = Flask(__name__)

log = open("/home/pi/feeder_logs/feeder_log_{}.log".format(datetime.datetime.now()), "w+")

#trying to prevent multiple instances running because for some reason it does that. idk why. 
#def find(pat, string):
#    match = re.findall(pat, string)  # find function for searches below
#    if len(match) > 1:
#        return True
#    else:
#        return None

#allProcessIDs = os.popen('pgrep -lf python3').read()
#sameProcessID = find('\d{3} python3', allProcessIDs)
#if sameProcessID:
#    log.write("I'm a clone... I'm gonna kill myself\n")
#    log.close()
#    raise SystemExit

morning_feed = None
afternoon_feed = None
night_feed = None

def setFeedScheduler(morning, afternoon, night):
    global morning_feed
    global afternoon_feed
    global night_feed
    global log
    # delete previous Feed jobs
    if(morning_feed and night_feed and afternoon_feed):
        log.write("deleting previous jobs\n")
        log.flush()
        morning_feed.set()
        afternoon_feed.set()
        night_feed.set()
    # create new feed jobs
    log.write("creating new feed jobs at {} {} {}\n".format(morning, afternoon, night))
    log.flush()
    morning_feed = Feed(morning).start_schedule()
    afternoon_feed = Feed(afternoon).start_schedule()
    night_feed = Feed(night).start_schedule()

def initial_load():
    global morning_feed
    global afternoon_feed
    global night_feed
    global log
    log.write("Starting up service!\n")
    log.flush()
    conn = sqlite3.connect('cat.db')
    c = conn.cursor()

    #creating tables if they don't exist
    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='feedtimes'; ''')
    if not c.fetchone()[0]==1:
        log.write("feedtimes table not present! Creating new one\n")
        log.flush()
        c.execute(''' CREATE TABLE feedtimes (morning text, afternoon text, night text); ''')
        c.execute(''' INSERT INTO feedtimes values ("06:30", "13:00", "19:00"); ''')

    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='feedlog'; ''')
    if not c.fetchone()[0]==1:
        log.write("feedlog table not present! Creating new one\n")
        log.flush()
        c.execute(''' CREATE TABLE feedlog (time datetime, type text, success text); ''')

    conn.commit()

    # set off the scheduler for the stored feeding times so it works on boot
    c.execute(''' SELECT morning, afternoon, night FROM feedtimes;''')
    times = c.fetchone()
    conn.commit()
    conn.close()
    log.write("setting initial feed time schedulers\n")
    log.flush()
    setFeedScheduler(times[0], times[1], times[2])


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
    global log
    if request.method == 'POST':
        log.write("recieved set feed request {}\n".format(request.form))
        log.flush()
        # TODO: lookup best practices for this
        conn = sqlite3.connect('cat.db')
        c = conn.cursor()
        # delete previous times from database
        c.execute('''DELETE FROM feedtimes;''')
        # add new times to database
        c.execute('''INSERT INTO feedtimes VALUES (?,?,?);''', [request.form['morning'], request.form['afternoon'], request.form['night']])
        conn.commit()
        conn.close()
        setFeedScheduler(request.form['morning'], request.form['afternoon'], request.form['night'])

    conn = sqlite3.connect('cat.db')
    c = conn.cursor()
    # delete previous times from database
    c.execute('''select * from feedtimes; ''')
    times = c.fetchone()
    conn.commit()
    conn.close()
    m_time = times[0]
    a_time = times[1]
    n_time = times[2]
    paw_pic = url_for('static', filename='paw_cursor.png')
    bootstrap_js = url_for('static', filename='bootstrap.bundle.min.js')
    jquery_js = url_for('static', filename='jquery.min.js')
    bootstrap_css = url_for('static', filename='bootstrap.min.css')
    return render_template('setfeed.html', paw_pic=paw_pic, bootstrap_js=bootstrap_js, bootstrap_css=bootstrap_css, jquery_js=jquery_js, m_time=m_time, a_time=a_time, n_time=n_time)
    

@app.route('/feedlog')
def feed_log():
    paw_pic = url_for('static', filename='paw_cursor.png')
    bootstrap_js = url_for('static', filename='bootstrap.bundle.min.js')
    jquery_js = url_for('static', filename='jquery.min.js')
    bootstrap_css = url_for('static', filename='bootstrap.min.css')
    conn = sqlite3.connect('cat.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM feedlog ORDER BY date(time) DESC LIMIT 50; ''')
    log = c.fetchall()
    conn.commit()
    conn.close()
    return render_template('feedlog.html', paw_pic=paw_pic, bootstrap_js=bootstrap_js, bootstrap_css=bootstrap_css, jquery_js=jquery_js, log=log)

@app.route('/feednow')
def feed_now():
    global log
    log.write("recieved feed now request!\n")
    log.flush()
    one_time_feed("Manual")
    return "True"

if __name__ == "__main__":
    initial_load()
    app.run(host='0.0.0.0', port=1234)
