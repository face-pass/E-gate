import os

db_config = {
'host': os.environ['HOST'],
'port': int(os.environ['PORT']),
'user': os.environ['USER'],
'password': os.environ['PASSWD'],
'database': os.environ['DB'],
'ssl': {'ssl':
            {'ca': os.environ['SSL']}
        }
}

blob_config = os.environ['Connect_str']