from flask import Flask


app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<h1>Hello, World! 🚀</h1>'

@app.route('/about')
def about_page():
    return '<h2>This is the About Page.</h2>'