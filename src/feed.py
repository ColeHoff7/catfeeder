from schedule import Scheduler
import time
import threading

#TODO: THEY ARE SHARING THE SAME SCHEDULER
class Feed():
    def __init__(self, t):
        # t is time string in HH:mm format
        self.feed_time = t

    def initiate_feed(self, i):
        print('{}: {}'.format(self.feed_time, i))
        return

    def start_schedule(self):
        sch = Scheduler()
        sch.every().day.at(self.feed_time).do(self.initiate_feed,'Doing job')
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