from flask import Blueprint, url_for, redirect

# Define the Blueprint
home = Blueprint("home", __name__, template_folder="templates", static_folder="static")


@home.route('/')
def index():
    return redirect(url_for('visualizer.index'))