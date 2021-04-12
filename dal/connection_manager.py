from .setup_dynamo_db import getDBConnection, createMspCWTable

from boto.dynamodb2.table import Table

class ConnectionManager:
    """
    DynamoDB connection manager
    """

    def __init__(self):
        self.db = None
        self.msp_connectWiseTable = None

        self.db = getDBConnection()
        self.setupMspCWTable()

    def setupMspCWTable(self):
        try:
            self.msp_connectWiseTable = Table("msp_cw", connection=self.db)
        except Exception as e:
            print e.message

    def getMspCWTable(self):
        if self.msp_connectWiseTable == None:
            self.setupMspCWTable()
        return self.msp_connectWiseTable

    def createMSPCWTable(self):
        self.msp_connectWiseTable = createMspCWTable(self.db)