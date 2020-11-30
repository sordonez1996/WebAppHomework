from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'moviesData'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Oscar Winnings (Men)'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblOscar')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, movies=result)


@app.route('/view/<int:movies_id>', methods=['GET'])
def record_view(movies_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblOscar WHERE id=%s', movies_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', movies=result[0])


@app.route('/edit/<int:movies_id>', methods=['GET'])
def form_edit_get(movies_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblOscar WHERE id=%s', movies_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', movies=result[0])


@app.route('/edit/<int:movies_id>', methods=['POST'])
def form_update_post(movies_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('fldYear'), request.form.get('fldAge'), request.form.get('fldName'),
                 request.form.get('fldMovie'), movies_id)
    sql_update_query = """UPDATE tblOscar t SET t.fldYear = %s, t.fldAge = %s, t.fldName = %s, t.fldMovie = 
    %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/OscarWinnings(Men)/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Movies Form')


@app.route('/OscarWinnings(Men)/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('id'), request.form.get('fldYear'), request.form.get('fldAge'), request.form.get('fldName'),
                 request.form.get('fldMovie'))
    sql_insert_query = """INSERT INTO tblOscar (id,fldYear,fldAge,fldName,fldMovie) VALUES (%s, %s,%s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/delete/<int:movies_id>', methods=['POST'])
def form_delete_post(movies_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM tblOscar WHERE id = %s """
    cursor.execute(sql_delete_query, movies_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/movies', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblOscar')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/movies/<int:movies_id>', methods=['GET'])
def api_retrieve(movies_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblOscar WHERE id=%s', movies_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/movies/<int:movies_id>', methods=['PUT'])
def api_edit(movies_id) -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['id'],content['fldYear'], content['fldAge'], content['fldName'],
                 content['fldMovie'], movies_id)
    sql_update_query = """UPDATE tblOscar t SET t.id = %s, t.fldYear = %s, t.fldAge = %s, t.fldName = %s, t.fldMovie = 
        %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp

@app.route('/api/v1/movies', methods=['POST'])
def api_add() -> str:

    content = request.json

    cursor = mysql.get_db().cursor()
    inputData = (content['id'], content['fldYear'], content['fldAge'],
                 content['fldName'], content['fldMovie'])
    sql_insert_query = """INSERT INTO tblOscar (id,fldYear,fldAge,fldName,fldMovie) VALUES (%s, %s,%s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp

@app.route('/api/v1/movies/<int:movies_id>', methods=['DELETE'])
def api_delete(movies_id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM tblOscar WHERE id = %s """
    cursor.execute(sql_delete_query, movies_id)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)