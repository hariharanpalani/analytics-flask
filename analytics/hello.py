from flask import Flask, request, redirect, url_for, jsonify, Response
import sqlite3
import json
import pandas as pd
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
CORS(app)

db = sqlite3.connect("dump.db", check_same_thread = False)
cur = db.cursor()

@app.route('/')
def index():
    return 'Welcome to Analytics API'

@app.route( '/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    upload_file_to_db(filename)
    return 'saved'

@app.route('/getdata', methods=['get'])
def getData():
    pageSize = 20
    page = int(request.args.get('page'))
    sql = 'select * from opdata limit ' + str(pageSize) + ' offset ' + str((page - 1) * 20)
    dataFrame = pd.read_sql_query(sql, db)
    return Response(dataFrame.to_json(orient='records'), mimetype='application/json')
    
def upload_file_to_db(filename):
    fileDate = filename.replace('op', '').replace('.csv', '')
    for chunk in pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename), chunksize=4):
        chunk.columns = [col.strip().replace('*', '') for col in chunk.columns]
        chunk.insert(len(chunk.columns), 'FILE_DATE', fileDate)
        chunk.to_sql(name="opdata", con=db, if_exists="append", index=False)
    
    cur.execute("insert into file_uploaded(filename, uploaddate) values (?, ?)", (filename, str(datetime.now())))
    cur.execute("delete from opdata where SYMBOL is null")
    db.commit()
    return True


if __name__ == '__main__':
    app.run()