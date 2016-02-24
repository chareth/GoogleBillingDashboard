import logging
from flask.app import Flask
from apps.config.apps_config import db_session


app = Flask(__name__)


from apps.billing.views import mod as billingModule
from apps.login.views import mod as loginModule
import os

app.register_blueprint(billingModule)
app.register_blueprint(loginModule)



@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
    db_session.close()


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()
