import time

from flask import Flask, request
from dal.connection_manager import ConnectionManager
from dal.controller.msp_cw_controller import MspCwController
import json

from dal.controller.remote_access_controller import RemoteAccessController

app = Flask(__name__)

cm = None

cm = ConnectionManager()
connectwise_controller = MspCwController(cm)
remote_access_controller = RemoteAccessController(cm)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/create')
def create():
    try:
        cm.create_msp_cw_table()
        cm.create_ra_table()
    except Exception as e:
        print e.message
    finally:
        return json.dumps({'success': True, 'data':{
            'connectwise_create_state': connectwise_controller.check_table_active(),
            'remote_access_create_state': remote_access_controller.check_table_active()
        }}), 200, {'ContentType': 'application/json'}


@app.route('/update_msp_cred/', methods=['POST'])
def update_msp_cred():
    msp_id = json.loads(request.get_data())['msp_id']
    credentials = json.loads(request.get_data())['credentials']
    connectwise_controller.update_isoc_cw(msp_id=msp_id, credentials=credentials)

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/set_msp_cred/', methods=['POST'])
def set_msp_cred():
    msp_id = json.loads(request.get_data())['msp_id']
    credentials = json.loads(request.get_data())['credentials']
    connectwise_controller.add_new_isoc_cw_item(msp_id=msp_id, credentials=credentials)

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/delete_msp_cred/', methods=['POST'])
def delete_msp_cred():
    msp_id = json.loads(request.get_data())['msp_id']

    result = connectwise_controller.delete_item_by_mspid_cw(msp_id=msp_id)

    return json.dumps({'success': result}), 200, {'ContentType': 'application/json'}

@app.route('/get_msp_cred/', methods=['GET'])
def get_msp_cred():
    from dal.models.model_msp_cw import ModelMspCw
    data = None
    msp_id = str(request.args['msp_id'])
    item = connectwise_controller.has_item_by_mspid_cw(msp_id=msp_id)
    modelMspCw = ModelMspCw(item)

    if modelMspCw is not None:
        data = modelMspCw.getMspCwJSON()

    return json.dumps({'success': True, 'data': data}), 200, {'ContentType': 'application/json'}




if __name__ == '__main__':
    app.run()
