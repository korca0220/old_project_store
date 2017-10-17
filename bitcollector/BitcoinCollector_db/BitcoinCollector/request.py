# coding=utf-8
import requests
import settings
import model
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
import logging
logging.basicConfig()


class MysqlRequest:
    def __init__(self):
        """
            데이터 베이스 접속을 위한 엔진 설정
            엔진은 선언만해서 바로연결이 안됨 , 첫 실행이 될때 연결이 됨
        """
        self.tables = ['btc', 'etc', 'eth', 'xrp', 'bch', 'qtum']
        # settings 커스텀 필요
        self.engine = create_engine(URL(**settings.DATABASE), echo=True)
        self.session = sessionmaker(bind=self.engine)()

    def create_table(self):
        for colum in self.tables:
            model.getDynamicModel(colum).metadata.create_all(self.engine)

    def drop_table(self):
        for type in self.tables:
            model.getDynamicModel(type).__table__.drop(self.engine)

    def insert_Data(self):
        url = "" #API URL
        r = requests.get(url)
        data = r.json()
        for type in self.tables:
            coin_data = data[type]
            coin_data = {'low': coin_data['low'],
                         'high': coin_data['high'],
                         'last': coin_data['last'],
                         'volume': coin_data['volume'],
                         'first': coin_data['first']
                         }

            coin_data = model.getDynamicModel(type)(**coin_data)
            self.session.add(coin_data)
            self.session.commit()
            self.session.close()


def schudler_func():
    request = MysqlRequest()
    request.insert_Data()


if __name__ == '__main__':
    schduler = BlockingScheduler()
    schduler.add_job(func=schudler_func, trigger='cron', minute="10")
    schduler.start()

    # 테이블 생성
    # request = MysqlRequest()
    # request.create_table()

    # 테이블 삭제
    # request.drop_table()
