from apps.application import app
from apscheduler.schedulers.background import BackgroundScheduler
from apps.billing.dataProcessor import data_processor


def set_scheduler(hour, min):
    scheduler = BackgroundScheduler()
    if hour is None and min is None:

        scheduler.add_job(data_processor, 'cron', day_of_week='mon-sun', hour=5, minute=30)
    else:

        scheduler.add_job(data_processor, 'cron', day_of_week='mon-sun', hour=hour, minute=min)

    scheduler.start()

    return scheduler


if __name__ == "__main__":
    set_ scheduler(None, None)
    app.run(debug=True, host='0.0.0.0', port=8080, use_reloader=False)

