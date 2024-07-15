from warning_system import create_app
from warning_system.custom import logging_utils
from scripts.send_to_dhis2 import *


def start_flask_app():
    app = create_app()
    app.run(debug=True, port=5000)


def start_scheduler():
    job_scheduler()
    run_continuously()


if __name__ == '__main__':
    logging_utils.setup_logging()

    # Create and start a thread for the scheduler
    scheduler_thread = threading.Thread(target=start_scheduler)
    scheduler_thread.start()

    # Start the flask app
    start_flask_app()

