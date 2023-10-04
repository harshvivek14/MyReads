from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello():
    return '<h1>Hello World!</h1>'

@app.route('/home')
def show_home():
    return render_template('/home.html')

# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()