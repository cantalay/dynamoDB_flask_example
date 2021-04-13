from .setup_dynamo_db import getDBConnection, create_msp_connectwise_table, create_remote_access_table

from boto.dynamodb2.table import Table


class ConnectionManager:
    """
    DynamoDB connection manager
    """

    def __init__(self):
        self.db = None
        self.msp_connectWise_table = None
        self.remote_access_table = None

        self.db = getDBConnection()
        self.setup_msp_cw_table()

    # MSP ConnectWise Credentials Table Configuration
    def setup_msp_cw_table(self):
        try:
            self.msp_connectWise_table = Table("msp_cw", connection=self.db)
        except Exception as e:
            print e.message

    def get_msp_cw_table(self):
        if self.msp_connectWise_table == None:
            self.setup_msp_cw_table()
        return self.msp_connectWise_table

    def create_msp_cw_table(self):
        self.msp_connectWise_table = create_msp_connectwise_table(self.db)


    # MSP Remote Access State Table Configuration

    def setup_ra_table(self):
        try:
            self.remote_access_table = Table("remote_access", connection=self.db)
        except Exception as e:
            print e.message

    def get_ra_table(self):
        if self.remote_access_table == None:
            self.setup_msp_cw_table()
        return self.remote_access_table

    def create_ra_table(self):
        self.remote_access_table = create_remote_access_table(self.db)
