from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine("sqlite:///fuelcard.db", echo=True)
#echo prints all the SQL commands executed in console for debugging purpose
Session = sessionmaker(bind=engine)

Base = declarative_base()