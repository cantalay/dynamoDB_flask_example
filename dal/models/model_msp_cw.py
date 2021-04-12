import json


class ModelMspCw:
    """
    This model generating for saving connectWise credential to dynamoDB
    """

    def __init__(self, item):
        self.item = item
        self.msp_id = item['msp_id']
        self.credentials = item['credentials']

        created_at = item['created_at']
        updated_at = item['updated_at']

    def getMspCwJSON(self):
        if self.item is not None:
            credentials_dict = {
                "msp_id": self.item["msp_id"],
                "credentials": self.item["credentials"],

                "created_at": self.item["created_at"],
                "updated_at": self.item["updated_at"]
            }
            return credentials_dict
