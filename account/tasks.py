import threading
import time
import schedule


def thread():
    while True:
        schedule.run_pending()
        time.sleep(1)


def prune_task():
    from channels_presence.tasks import prune_presence, prune_rooms
    print('Prunning tasks')
    prune_presence()
    prune_rooms()


def schedule_tasks():
    schedule.every(10).seconds.do(prune_task)
    threading.Thread(target=thread, daemon=True).start()
