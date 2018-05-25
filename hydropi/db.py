from sqlalchemy import create_engine

postgres_base_uri = "postgres://{dbuser}@{dbhost}/{dbname}"

db_con = None

'''
must have .pgpass file with valid creds for this to work
'''

if db_con is None:
        db_con = create_engine(
            postgres_base_uri.format(
                dbuser='hydropi_admin',
                dbhost='localhost',
                dbname='hydropi',
            )
        )
