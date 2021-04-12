from datetime import datetime

from boto.dynamodb2.exceptions import ItemNotFound
from boto.exception import JSONResponseError

from dal.models.model_msp_cw import ModelMspCw

from boto.dynamodb2.items import Item


class MspCwController:

    def __init__(self, connection_manager):
        self.cm = connection_manager

    def add_new_isoc_cw_item(self, msp_id=None, credentials=None):
        now = str(datetime.now())
        item = Item(self.cm.getMspCWTable(), data={
            "msp_id": msp_id,
            "credentials": credentials,

            "created_at": str(datetime.now()),
            "updated_at": str(datetime.now())

        })
        return item.save()

    def check_table_active(self):
        description = self.cm.db.describe_table('msp_cw')
        status = description['Table']['TableStatus']
        return status == "ACTIVE"

    def has_item_by_mspid_cw(self, msp_id):
        try:
            item = self.cm.getMspCWTable().get_item(msp_id=msp_id)
        except ItemNotFound as inf:
            return None
        except JSONResponseError as jre:
            return None
        return item


    def delete_item_by_mspid_cw(self, msp_id):
        try:
            item = self.cm.getMspCWTable().get_item(msp_id=msp_id)
            result = item.delete()
        except ItemNotFound as inf:
            return None
        except JSONResponseError as jre:
            return None
        return result

    def update_isoc_cw(self, msp_id, credentials):
        old_msp_item = self.has_item_by_mspid_cw(msp_id=msp_id)
        now = str(datetime.now())
        item = Item(self.cm.getMspCWTable(), data={
            "msp_id": old_msp_item['msp_id'],
            "credentials": credentials,

            "created_at": old_msp_item['created_at'],
            "updated_at": str(now)

        })
        return item.save(overwrite=True)
