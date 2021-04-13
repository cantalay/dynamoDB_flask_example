import json


class ModelRemoteAccess:
    """
    This model generating for saving isoc user's remote access state to dynamoDB
    """

    def __init__(self, item):
        self.item = item
        self.msp_id = item['msp_id']
        self.remote_access_status = item['remote_access_status']
        self.user_choice = item['user_choice']
        self.action_type = item['action_type']

        created_at = item['created_at']
        updated_at = item['updated_at']

    def get_remote_access_json(self):
        if self.item is not None:
            remote_access_dict = {
                "msp_id": self.item["msp_id"],
                "remote_access_status": self.item["remote_access_status"],
                "user_choice": self.item["user_choice"],
                "action_type": self.item["action_type"],

                "created_at": self.item["created_at"],
                "updated_at": self.item["updated_at"]
            }
            return remote_access_dict
