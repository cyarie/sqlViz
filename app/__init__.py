# Import flask and template operators
from flask import Flask, render_template
from flask.ext.cors import CORS
import MySQLdb as Database
import MySQLdb.cursors as cursors

from app import config


# Define the WSGI app object
app = Flask(__name__)

# Config
app.config.from_pyfile("config.py")
cors = CORS(app)


# Define the database object which is imported
# by modules and controllers
def replica_connect():
    dnc = Database.connect(host=config.DATABASE_URI,
                           port=config.DATABASE_PORT,
                           user=config.DATABASE_USER,
                           passwd=config.DATABASE_PW,
                           db=config.DATABASE_NAME,
                           ssl=config.DATABASE_SSL_CERT,
                           cursorclass=cursors.DictCursor)
    db_cur = dnc.cursor()
    return db_cur

# 404 Handling
@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


# 500 Handling
@app.errorhandler(503)
def server_done_broke():
    return render_template("503.html"), 503

from app.visualizer.controllers import visualizer
app.register_blueprint(visualizer)

from app.home.controllers import home
app.register_blueprint(home)