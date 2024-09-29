from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, select
from sqlalchemy.orm import sessionmaker

URL_DATABASE="mysql+pymysql://root:peter@localhost:3306/myapp"

engine = create_engine(URL_DATABASE, echo=True)
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
metadata = MetaData()

# institutes_table = Table('institutes',metadata,autoload_with=engine)
# Define institutes table
institutes_table = Table(
    'institutes', metadata,Column('id', Integer, primary_key=True, autoincrement=True),
    Column('institute_name', String(255)),
    Column('program_name', String(255)),
    Column('institute_type', String(255)),
    Column('seat_type', String(50)),
    Column('gender', String(50)),
    Column('duration', String(50)),
    Column('year', Integer),
    Column('opening_rank', Integer),
    Column('closing_rank', Integer)
)

metadata.create_all(engine)