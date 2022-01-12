from base import Base
from sqlalchemy import Column, Integer, String, Boolean, orm


class Profile(Base):
    __tablename__ = 'Profile'
    temp = Column(Integer, primary_key=True)
    humidity = Column(Integer)
    current_temp_module = Column(String)
    temp_diff = Column(Integer)
    mode = Column(String)
    active = Column(Boolean)

    def __init__(self, temp, humidity, current_temp_module, temp_diff, mode, active):
        self.temp = temp
        self.humidity = humidity
        self.current_temp_module = current_temp_module
        self.temp_diff = temp_diff
        self.mode = mode
        self.active = active
        self.high_temp = self.temp + self.temp_diff
        self.low_temp = self.temp - self.temp_diff

    @orm.reconstructor
    def init_on_load(self):
        self.high_temp = self.temp + self.temp_diff
        self.low_temp = self.temp - self.temp_diff
