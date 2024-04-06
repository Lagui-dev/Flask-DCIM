from flask import Flask, render_template, request
from app import create_app, db
from models import Rack, Unit

app = create_app()


# @app.shell_context_processor
# def make_shell_context():
#     return {'db': db, 'Rack': Rack, 'Unit': Unit}
@app.route('/')
def home_page():
    if request.method == 'GET':
        return render_template('index.html')
