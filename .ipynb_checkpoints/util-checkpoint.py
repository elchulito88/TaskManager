import argparse
import arrow
import backup_files as bf
import backup_sql as bs
import pandas as pd
import sqlite3
import time

class utilizationApp():

	def __init__(self, dates=None, total_time=None, label_description=None, drop=None, create=None):
		self.dates = dates
		self.total_time = total_time
		self.description = label_description
		self.create = create
		self.drop = drop
		self.db = 'utilization'
		self.table = 'metrics'
		self.db_file = "E:/utilization/production/utilization"
		self.backup_dir = "E:/utilization/backups/backup_db"
		self.metric_file = "E:/utilization/production/files"
		self.metric_backup_dir = "E:/utilization/backups/backup_files"
		drop_validation = 'Validated' if self.drop is None else self.drop_table()
		create_validation = 'Validated' if self.create is None else self.create_table()


	def drop_table(self):
		db = sqlite3.connect(self.db)
		cursor = db.cursor()
		sql = '''DROP TABLE {}'''.format(self.table)
		cursor.execute(sql)
		db.commit()
		db.close()

		print('\n')
		print('Table was dropped!\n')


	def create_table(self):
		db = sqlite3.connect(self.db)
		cursor = db.cursor()
		sql = '''CREATE TABLE {}(id INTEGER PRIMARY KEY, Dates DATE, 
						total_time INTEGER, label_description TEXT)'''.format(self.table)
		cursor.execute(sql)
		db.commit()
		db.close()

		print('Table was created!\n')


	def insert_data(self):
		db = sqlite3.connect(self.db)
		cursor = db.cursor()
		sql = ''' INSERT INTO {}(Dates, total_time, label_description)
						VALUES(?, ?, ?)'''.format(self.table)
		cursor.execute(sql, (self.dates, self.total_time, self.description))
		db.commit()
		db.close()

		print('Data was inserted!\n')


	def query_data(self):
		db = sqlite3.connect(self.db)
		cursor = db.cursor()
		sql = "SELECT * from {}".format(self.table)
		cursor.execute(sql)
		all_rows = cursor.fetchall()
		db.close()

		return all_rows


	def delete_data(self, remove):
		db = sqlite3.connect(self.db)
		cursor = db.cursor()
		sql = ''' DELETE from {0} WHERE id = {1}'''.format(self.table, remove)
		cursor.execute(sql)
		db.commit()
		db.close()

		print('Data was removed!\n')


	def write_data_to_csv(self):
		db = sqlite3.connect(self.db)
		df = pd.read_sql_query("select * from {}".format(self.table), db)
		df.to_csv("files/{}.csv".format(self.table), index=False)
		db.close()


	def sum_data(self):
		self.write_data_to_csv()
		df = pd.read_csv("files/{}.csv".format(self.table))
		final_df = df.groupby(['Dates','label_description'])['total_time'].sum()
		final_df.to_csv("files/Final_Metrics_{}.csv".format(arrow.now().format('YYYY-MM-DD')))


	def backup_db(self):
		bs.sqlite3_backup(self.db_file, self.backup_dir)
		bs.clean_data(self.backup_dir)


	def backup_files(self):
		bf.run_backup(self.metric_file, self.metric_backup_dir)


if __name__ == '__main__':

	# Example 1
	# python util.py -d "2018-06-21" -t 33  -de "Community time" -dr "Drop" -c "Created"

	# Example 2
	# python util.py -d "2018-06-21" -t 33  -de "Community time"

	# Example 3
	# python util.py -d "2018-06-21" -t 59 -de "Community time" -w "Write" -dr "Drop" -c "Create"

	# Example 4
	# python util.py -d "2018-06-21" -t 59 -de "Community time" -s "sum"

	parser = argparse.ArgumentParser(description='Recording utilization for metrics')
	parser.add_argument('-d', '--dates',  type=str, default=None, help='Enter the date of the activity')
	parser.add_argument('-t', '--time',  type=int, default=None, help='Enter how much time it took you in 15 min intervals')
	parser.add_argument('-de', '--desc',  type=str, default=None, help='Enter the label of the activity')
	parser.add_argument('-dr', '--drop',  default=None, help='Drop a table')
	parser.add_argument('-c', '--create',  default=None, help='Create a table')
	parser.add_argument('-w', '--write',  default=None, help='Write to a table')
	parser.add_argument('-s', '--sum',  default=None, help='Sum all of the values in a table')
	parser.add_argument('-r', '--remove', default=None, help='Remove values from a table')
	parser.add_argument('-b', '--backup', default=None, help='Backup data')

	args, unknown = parser.parse_known_args()

	utilApp = utilizationApp(args.dates, args.time, args.desc, args.drop, args.create)

	if args.sum == "sum":
		utilApp.sum_data()
		if args.backup == "bk":
			utilApp.backup_db()
			utilApp.backup_files()

	elif args.remove is not None:
		utilApp.delete_data(int(args.remove))

	else:
		utilApp.insert_data()
		print(utilApp.query_data())

		if args.write is not None:
			utilApp.write_data_to_csv()