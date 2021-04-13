from datetime import datetime

from boto.dynamodb2.exceptions import ItemNotFound
from boto.dynamodb2.items import Item
from boto.exception import JSONResponseError


class RemoteAccessController:

    def __init__(self, connection_manager):
        self.cm = connection_manager

    def add_new_isoc_remote_item(self, msp_id=None, remote_access_status=None, action_type=None, user_choice=None):
        now = str(datetime.now())
        item = Item(self.cm.get_ra_table(), data={
            "msp_id": msp_id,
            "remote_access_status": remote_access_status,
            "user_choice": user_choice,
            "action_type": action_type,
            "created_at": now,
            "updated_at": now,
        })
        return item.save()

    def check_table_active(self):
        description = self.cm.db.describe_table("remote_access")
        status = description['Table']['TableStatus']
        return status == 'ACTIVE'

    def has_item_by_mspid_remote(self, msp_id):
        try:
            item = self.cm.get_ra_table().get_item(msp_id=msp_id)
        except ItemNotFound as inf:
            return None
        except JSONResponseError as jre:
            return None
        return item


    def delete_isoc_remote(self, msp_id):
        try:
            item = self.cm.get_ra_table().get_item(msp_id=msp_id)
            result = item.delete()
        except ItemNotFound as inf:
            return None
        except JSONResponseError as jre:
            return None
        return result

    def update_isoc_remote(self, msp_id, credentials):
        old_msp_item = self.has_item_by_mspid_remote(msp_id=msp_id)
        now = str(datetime.now())
        item = Item(self.cm.get_ra_table(), data={
            "msp_id": old_msp_item['msp_id'],
            "credentials": credentials,

            "created_at": old_msp_item['created_at'],
            "updated_at": str(now)

        })
        return item.save(overwrite=True)

