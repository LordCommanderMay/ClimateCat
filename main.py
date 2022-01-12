from time import sleep, time
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from base import Base
from temp_record import TempRecord
from modules import ACModule, TempModule, HumidModule
from log import start_up_log
from Profile import Profile
from user import User


def main_func():
    engine = create_engine('sqlite:///climatecat.db')
    Base.metadata.create_all(bind=engine)
    session = sessionmaker(bind=engine)
    session = session()
    temp = 72
    start_up_log(session)
    while True:
        temp_modules = session.query(TempModule)
        ac_module = session.query(ACModule)[0]
        profile = session.query(Profile)[0]

        for temp_module in temp_modules:
            if profile.current_temp_module == temp_module.name:
                temp_module.get_data()
                temp = temp_module.temp
                humid = temp_module.humidity
            else:
                raise EnvironmentError('No temp modules found!')

        if profile.mode == 'cool':
            if temp > profile.high_temp:
                print(f'high: {profile.high_temp}')
                print(ac_module.on)
                ac_module.turn_on()
            elif temp < profile.low_temp:
                print(f'low: {profile.low_temp}')
                ac_module.turn_off()

        session.commit()
        session.close()
        sleep(1)
        print(f' temp: {temp} humid: {humid}')


if __name__ == "__main__":
    main_func()
