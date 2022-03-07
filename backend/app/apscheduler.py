from flask_apscheduler import APScheduler

# Initialise scheduler
def create_scheduler():
    global scheduler
    scheduler = APScheduler()
