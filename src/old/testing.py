from feed import Feed
import time 

f = Feed("18:21")
f_scheduler = f.start_schedule()
while True:
    print("waiting on job")
    time.sleep(10)