import logging

class taskLogger():

	def __init__(self, f_name):
		self.f_name = f_name

	# def startLog(self):
	# 	logging.basicConfig(filename=self.f_name + '.log', format='%(asctime)s %(levelname)-8s %(message)s', 
	# 		level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
	# 	logging.info('\n' + 'Starting Logs')

	# def endLog(self):
	# 	logging.basicConfig(filename=self.f_name + '.log', format='%(asctime)s %(levelname)-8s %(message)s', 
	# 		level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
	# 	logging.info('Ending Logs')

	def logged(self, message):
		logging.basicConfig(filename='logger/' + self.f_name + '.log', format='%(asctime)s %(levelname)-8s %(message)s', 
			level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
		logging.info(message)

if __name__ == '__main__':
	logs = taskLogger('Logs')
	logs.startLog()
	logs.endLog()
