import schedule
import time
import threading

class Feed():
    def __init__(self, t):
        # t is time string in HH:mm format
        self.feed_time = t

    def initiate_feed(self, i):
        print(i)
        return

    def start_schedule(self):
        schedule.every().day.at(self.feed_time).do(self.initiate_feed,'Doing job')
        cease_continuous_run = threading.Event()

        class ScheduleThread(threading.Thread):
            @classmethod
            def run(cls):
                while not cease_continuous_run.is_set():
                    schedule.run_pending()
                    time.sleep(1)

        continuous_thread = ScheduleThread()
        continuous_thread.start()
        return cease_continuous_run