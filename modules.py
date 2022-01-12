from sqlalchemy import Column, String, Integer, Boolean, orm
from base import Base
from requests import request
import inspect
import json


def represent(dictionary, title=None):
    # this function should be  moved to log.py
    """used to create text repr for are objects in a card like format for use in console and logging"""
    return_string = ''
    # find longest strings for formatting
    longest_key = 0
    longest_value = 0
    for key in dictionary:
        if len(key) > longest_key:
            longest_key = len(key)
        if len(str(dictionary[key])) > longest_value:
            longest_value = len(str(dictionary[key]))
    # build return_string
    if title is None:
        for key in dictionary:
            return_string = return_string + f"  {key:>{longest_key}} : {dictionary[key]:<{longest_value}} \n"
    else:
        if type(title) == str:
            title = dictionary.pop(title)
            return_string = return_string + f' \033[4m{title:<{longest_value + longest_key + 3}}\033[0m\n'
            for key in dictionary:
                return_string = return_string + f" {key:>{longest_key}} : {dictionary[key]:<{longest_value}} \n"


        else:
            raise ValueError('title must be a string ')

    return return_string


class TempModule(Base):
    """class represents a temperature module, a physical device responsible for getting temperature and humidity data"""
    __tablename__ = 'Temp Modules'  # database table name
    address = Column(String, primary_key=True)  # Ipv4 and port Ex: 0.0.0.0:0000
    name = Column(String)  # Ex: Living Room Temp Module

    def __init__(self, address, name):
        self.address = address  # ^
        self.name = name  # ^
        self.temp = None  # defined by get_data()
        self.humidity = None  # defined by get_data()
        self.get_data()

    @orm.reconstructor
    def init_on_load(self):
        """upon recreation by orm this method runs method get_data() """
        self.get_data()

    def get_data(self):
        """sends http 'get request to temp modules for temperature and humidity data in json format.  Then assigns data to
        the object's  self.temp and self.humidity properties if property imperial =  True the temp is also converted
        to fahrenheit. finally returns both self.temp, self.humidity which optional be unpacked format example:  {
        "humidity":28.792858123779297,"temp":25.922584533691406}
        """
        url = f'http://{self.address}/get_data'
        print(url)
        humidty_temperature = request(url=url, method='get')
        humidty_temperature = humidty_temperature.json()
        self.temp = (float(humidty_temperature["temp"]) * 9 / 5) + 32

        self.humidity = float(humidty_temperature['humidity'])
        return self.temp, self.humidity

    def as_dict(self):
        """:returns removes (pops) sqlalchemy's from '_sa_instance_state' if it exists from __dict__ built-in method 
        and then returns object as a object as a dictionary """
        dictionary = self.__dict__
        dictionary.pop('_sa_instance_state', None)
        return dictionary

    def as_json(self):
        """json dumps as_dict() function above"""
        return json.dumps(self.dict())

    def __repr__(self):
        return represent(self.as_dict(), title='name')


class ACModule(Base):
    __tablename__ = 'AC Modules'
    address = Column(String, primary_key=True)
    name = Column(String)
    _on = Column(Boolean)
    _temp = Column(Integer)

    def __init__(self, address, name):
        self.address = address
        self.name = name
        self.on = self._on

        self.max_temp = 75
        self.min_temp = 60
        self._temp = 68
        self.fan_setting = 2
        self.mode = 'fan'

    @orm.reconstructor
    def init_on_load(self):
        self.max_temp = 85
        self.min_temp = 60
        self.fan_setting = 3
        self.on = self._on
        self.mode = 'fan'

    @property
    def temp(self):
        return self._temp

    @temp.setter
    def temp(self, new_temp):
        if new_temp > self.max_temp:
            self._temp = self.max_temp

        elif new_temp < self.min_temp:
            self._temp = self.min_temp

        else:
            self._temp = new_temp

    def _toggle_power(self):
        url = f'http://{self.address}/power'
        print(url)
        request(url=url, method='get')

    def turn_on(self):
        if not self._on:
            self._toggle_power()
            self._on = True
            print(self._on)

    def turn_off(self):
        print('off bitch')
        if self._on:
            self._toggle_power()
            self._on = False

    def set_fan_setting(self, setting: int):
        if self.fan_setting == setting:
            print('setting is the same this request should have no been sent')
        else:
            self.fan_setting = setting

    # function to change fan setting

    def change_mode(self, new_mode):
        if self.mode == new_mode:
            print('same mode might be a bug somewhere')
        else:
            if new_mode == 'fan':
                self.mode = new_mode
            # send change
            elif new_mode == 'ac':
                self.mode = new_mode
            # send chnage

            else:
                print("thats not a vaild option must be ac or fan. bug somwhere?")

    def set_temp(self, temp):

        if temp > self.temp:

            difference = temp - self.temp
            self.temp = temp
            for _ in range(difference):
                pass  # funcation to increase temp

        elif temp < self.temp:

            difference = self.temp - temp
            self.temp = temp
            for _ in range(difference):
                pass  # funcation to decrease temp
        else:
            print("no increase shouldnt be running")

    def as_dict(self):
        dictionary = self.__dict__
        dictionary.pop('_sa_instance_state', None)
        return dictionary

    def as_json(self):
        return json.dumps(self.dict())

    def __repr__(self):
        dictionary = self.as_dict()
        return represent(dictionary)


class HumidModule(Base):
    __tablename__ = 'Humid Modules'
    name = Column(String)
    address = Column(String, primary_key=True)

    def __init__(self, address, name):
        self.address = address
        self.name = name
        self.on = False

    def create_url(self):
        return f'http//:{self.address}/'

    def toggle_power(self):
        request(url=f'{self.create_url()}power', method='get')
        if self.on == False:
            self.on = True
        else:
            self.on = False

    def as_dict(self):
        dictionary = self.__dict__
        dictionary.pop('_sa_instance_state', None)
        return dictionary

    def as_json(self):
        return json.dumps(self.dictx())

    def __repr__(self):
        return_string = ''
        dictionary = self.as_dict()
        for key in dictionary:
            return_string = return_string + key

        return return_string
