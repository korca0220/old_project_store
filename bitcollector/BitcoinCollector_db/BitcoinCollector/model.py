import settings
from sqlalchemy import Column, Integer, Float
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()

def getDynamicModel(tableName):
    class Store(base):
        __tablename__ = tableName
        __table_args__ = {'extend_existing': True}
        id = Column(Integer, primary_key=True)
        last = Column('last', Float)
        high = Column('high', Float)
        volume = Column('volume', Float)
        first = Column('first', Float)
        low = Column('low', Float)

        def __init__(self, last, high, volume, first, low):
            self.last = last
            self.high = high
            self.volume = volume
            self.first = first
            self.low = low


        def __repr__(self):
            return "<Store('%s', '%s', '%s', '%s', '%s')>" % (self.last, self.high, self.volume, self.first, self.low)
    return Store