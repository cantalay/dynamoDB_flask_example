from boto.dynamodb2.fields import GlobalAllIndex, HashKey, RangeKey
from boto.dynamodb2.layer1 import DynamoDBConnection
from boto.dynamodb2.table import Table
from boto.exception import JSONResponseError

from resources import settings

def getDBConnection():
    try:
        SECRET_KEY = settings.aws_secret_access_key
        ACCESS_KEY_ID = settings.aws_access_key_id
        HOST = settings.db_host
        PORT = settings.dp_port
        params = {
            'is_secure': True,
            'aws_access_key_id': ACCESS_KEY_ID,
            'aws_secret_access_key': SECRET_KEY
        }
        if HOST is not None:
            params['host'] = HOST
        if PORT is not None:
            params['port'] = PORT
    except Exception as e:
        print e.message

    db = DynamoDBConnection(**params)
    return db

def create_msp_connectwise_table(db):
    mspCwTable = None
    try:

        mspCwTable = Table.create("msp_cw", schema=[HashKey("msp_id")],
                                  throughput={
                                      'read': 1,
                                      'write': 1
                                  },
                                  connection=db)
    except JSONResponseError as jre:
        try:
            mspCwTable = Table("msp_cw", connection=db)
        except Exception as e:
            print e.message
    finally:
        return mspCwTable

def create_remote_access_table(db):
    remote_access_table = None
    try:

        remote_access_table = Table.create("remote_access", schema=[HashKey("msp_id")],
                                  throughput={
                                      'read': 1,
                                      'write': 1
                                  },
                                  connection=db)
    except JSONResponseError as jre:
        try:
            remote_access_table = Table("remote_access", connection=db)
        except Exception as e:
            print e.message
    finally:
        return remote_access_table


