from flask import request
from flask import Flask
from flask import render_template
from flask import jsonify
from flask import url_for
from flask import redirect
import sqlite3
import time
import calendar

app = Flask(__name__)
global_headers = ""


@app.before_request
def before_request():
    if "IgnoreMe" in request.headers['Cookie']:
        pass
    elif "AdminTings" in request.headers['Cookie']:
        pass
    else:
        cookie = str(request.headers['Cookie'])
        method = str(request.method)
        parameters = str(request.args)
        full_data = request.data
        print("Full Data: "+ full_data)
        conn = sqlite3.connect("requests.db")
        if global_headers != None:
            sql = 'INSERT INTO requests (cookie, method, parameters) VALUES ("'+cookie+'","'+method+'","'+parameters+'")'
            c = conn.cursor()
            c.execute(sql)
            conn.commit()
            conn.close()
        else: 
            pass


@app.route("/clearDB")
def clearDB():
    sql = "DELETE FROM requests;"
    conn = sqlite3.connect('requests.db')
    c = conn.cursor()
    c.execute(sql)
    conn.commit()
    return redirect(url_for('index'))


@app.after_request
def after_request(response):
    return response


@app.route("/")
@app.route("/index")
def index():
    return render_template("main.html")


@app.route("/poll")
def poll():
    sql = "SELECT cookie,method,parameters FROM requests ORDER BY id DESC LIMIT 10;"
    conn = sqlite3.connect("requests.db")
    c = conn.cursor()
    c.execute(sql)
    conn.commit()
    values = c.fetchall()
    return jsonify(values)


# Dynamic Domain for Filtering with Jquery(?) 
@app.route('/capture/<variable>', methods=['GET'])
def pokemon(variable):
    cookie = request.headers['cookie']
    return str(cookie)


if __name__ == '__main__':
    app.run(debug=True)


