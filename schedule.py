from sqlalchemy import Column, String, Time, Float
from base import Base
from datetime import  time

class TempModuleEvent(Base):
	__tablename__ = 'Temp Module Schdule'
	start_time = Column(Time, primary_key =True)
	end_time = Column(Time)
	temp_module_name = Column(String)
	
	def __init__(self, start_time, temp_module_name):
		self.start_time = start_time
		self.temp_module_name = temp_module_name

	def __contains__(self, item):
		if self.start_time <= self.end_time:
			return self.start_time <= item <= self.end_time
		else:
			return self.start_time <= item or item <= self.end_time
	
	

class TempEvent(Base):
	__tablename__ = 'Temp Schdule'
	start_time = Column(Time, primary_key=True)
	end_time = Column(Time)
	temp = Column(Float)


	def __init__(self, start_time, end_time, temp_module_name):
		self.start_time = start_time
		self.end_time = end_time
		self.temp_module_name = temp_module_name

	def __contains__(self, item):
		if self.start_time <= self.end_time:
			return self.start_time <= item <= self.end_time
		else:
			return self.start_time <= item or item <= self.end_time





