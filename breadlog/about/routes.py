from flask import render_template, Blueprint 

about = Blueprint('about', __name__)

@about.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
