# %load third.py
from flask import Flask, url_for, request
from fib import  fib
app = Flask(__name__)

Constnats = {"1":1, "2":2}
Constnats.get("1")

@app.route('/')
def root():
    return 'Hello world!'


@app.route('/page')
def my_api():
    return 'I am talking to  ' + url_for('my_api')


@app.route('/page/<pageid>')
def pages(pageid):
    return 'You are at page ' + pageid

@app.route('/fib')
def fib3():
    _no = request.args['no']
    _no = int(_no)
    res = fib(_no)
    return res



@app.route('/greet')
def greet():
    name = request.args['name']
    return 'Hi ' + name


@app.route('/methods', methods=['GET', 'POST'])
def method_type():
    if request.method == 'GET':
        return "Request made through GET method \n"

    elif request.method == 'POST':
        myparam = request.json
        return "Request made through POST method type {} \n".format(type(myparam))


if __name__ == '__main__':
    app.run(port=8889)