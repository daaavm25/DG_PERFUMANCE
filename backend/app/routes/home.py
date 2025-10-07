from flask import Blueprint, render_template


home_bp = Blueprint('home', __name__, url_prefix='/')

def index():
    return render_template('home.html')
