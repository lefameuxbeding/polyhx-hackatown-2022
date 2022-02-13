import os

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Enum

from actions.sentiment import Sentiment

host = os.environ.get("DB_HOST", "postgresql-cfc120d9-o4d8d3c08.database.cloud.ovh.net")
database = os.environ.get("DB_NAME", "rasa")
user = os.environ.get("DB_USER", "rasa")
password = os.environ["DB_PASSWD"]
port = int(os.environ.get("DB_PORT", 20184))

db_engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}?sslmode=require')
meta = MetaData()

service_comments = Table(
    'service_comments', meta,
    Column('id', Integer, primary_key=True),
    Column('message', String),
    Column('service', String),
    Column('sentiment', Enum(Sentiment))
)
db_conn = db_engine.connect()
