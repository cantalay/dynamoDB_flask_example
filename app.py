import time

from flask import Flask, request
from dal.connection_manager import ConnectionManager
from dal.controller.msp_cw_controller import MspCwController
import json

app = Flask(__name__)

cm = None

cm = ConnectionManager()
controller = MspCwController(cm)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/create')
def create():
    cm.createMSPCWTable()

    while controller.check_table_active() == False:
        time.sleep(3)
    return str(controller.check_table_active())


@app.route('/update_msp_cred/', methods=['POST'])
def update_msp_cred():
    msp_id = json.loads(request.get_data())['msp_id']
    credentials = json.loads(request.get_data())['credentials']
    controller.update_isoc_cw(msp_id=msp_id, credentials=credentials)

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/set_msp_cred/', methods=['POST'])
def set_msp_cred():
    msp_id = json.loads(request.get_data())['msp_id']
    credentials = json.loads(request.get_data())['credentials']
    controller.add_new_isoc_cw_item(msp_id=msp_id, credentials=credentials)

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/delete_msp_cred/', methods=['POST'])
def delete_msp_cred():
    msp_id = json.loads(request.get_data())['msp_id']

    result = controller.delete_item_by_mspid_cw(msp_id=msp_id)

    return json.dumps({'success': result}), 200, {'ContentType': 'application/json'}

@app.route('/get_msp_cred/', methods=['GET'])
def get_msp_cred():
    from dal.models.model_msp_cw import ModelMspCw
    data = None
    msp_id = str(json.loads(request.get_data())['msp_id'])
    item = controller.has_item_by_mspid_cw(msp_id=msp_id)
    modelMspCw = ModelMspCw(item)

    if modelMspCw is not None:
        data = modelMspCw.getMspCwJSON()

    return json.dumps({'success': True, 'data': data}), 200, {'ContentType': 'application/json'}


if __name__ == '__main__':
    app.run()
