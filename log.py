import coloredlogs, logging
from modules import ACModule, TempModule, HumidModule
from user import User
from datetime import datetime
import subprocess

def get_terminal_length():
	tput = 11
	
	return 12
		

		
def divider_line(line_type = '_', length = get_terminal_length()):
	return line_type * length
	
def object_print(name, query):
	return_string = f'\n{name}:\n\n'
	for item in query:
		return_string = return_string + f'{item}\n'
	return return_string
	

def start_up_log(session):
	
	temp_modules = session.query(TempModule)
	users = session.query(User)
	ac_modules = session.query(ACModule)
	modules_dict = {
		'Temperature Modules' : temp_modules,
		'Users' : users,
		'AC Modules'  : ac_modules
		}

	
		
	
	
	#Header
	print(divider_line('*'))
	print('Starting Climate Cat!! 😸 Date:' + str(datetime.now()))
	print(divider_line('*'))
	
	for key in modules_dict: 
		print(object_print(key, modules_dict[key]))
		print(divider_line())
		
		
	
	

	