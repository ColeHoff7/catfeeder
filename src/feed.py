from schedule import Scheduler
import time
import threading
from gpiozero import Servo
import sqlite3
import datetime

def one_time_feed(kind):
    success = "Success"
    try:
        servo = Servo(18)
        servo.min()
        servo.max()
        servo.min()
        servo.max()
    except Exception as e:
        success = "Failure: {}".format(e)

    now = datetime.datetime.now()
    now_string = now.strftime("%d/%m %H:%M")
    conn = sqlite3.connect('cat.db')
    c = conn.cursor()
    c.execute('''INSERT INTO feedlog values (?,?,?);''', [now_string, kind, success])
    conn.commit()
    conn.close()

class Feed():
    def __init__(self, t):
        # t is time string in HH:mm format
        self.feed_time = t

    def initiate_feed(self, i):
        print('{}: {}'.format(self.feed_time, i))
        one_time_feed("Scheduled")
        return

    def start_schedule(self):
        sch = Scheduler()
        sch.every().day.at(self.feed_time).do(self.initiate_feed,'Feeding')
        cease_continuous_run = threading.Event()

        class ScheduleThread(threading.Thread):
            @classmethod
            def run(cls):
                while not cease_continuous_run.is_set():
                    sch.run_pending()
                    time.sleep(1)

        continuous_thread = ScheduleThread()
        continuous_thread.start()
        return cease_continuous_run