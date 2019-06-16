from flask import (Flask,
                   render_template,
                   redirect,
                   url_for,
                   request,
                   make_response,
                   flash)

import json

import mysql.connector as mysql

from options import DEFAULTS

app = Flask(__name__)
app.secret_key = 'esauhou>UO>au.sh35@<Uouo52%@#ouo.42!@#42'

def get_saved_data():
    try:
        data = json.loads(request.cookies.get('character'))
    except TypeError:
        data = {}
    return data


@app.route('/')
def index():
    return render_template('index.html', saves=get_saved_data())


@app.route('/builder')
def builder():
    return render_template(
        'builder.html',
        saves=get_saved_data(),
        options=DEFAULTS
    )

@app.route('/save', methods=['POST'])
def save():

    flash("Amazing, We have saved your bear!")

    response = make_response(redirect(url_for('builder')))

    data = get_saved_data()

    save_data_to_db( data )

    data.update(dict(request.form.items()))

    response.set_cookie('character', json.dumps(data))

    return response


mydb = mysql.connect(
  host="localhost",
  user="root",
  passwd="",
  database="python_handin"
)

print(mydb)


def save_data_to_db(data):
    print( data )

    mycursor = mydb.cursor()

    sql = "INSERT INTO bears (name, data) VALUES (%s, %s)"
    print( sql )

    val = [
        (data['name'], json.dumps(data))
    ]
    print( val )

    mycursor.executemany(sql, val)

    mydb.commit()

    print(mycursor.rowcount, "was inserted.")

    return ''


app.run(debug=True,host='localhost',port=8015)