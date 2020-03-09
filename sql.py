import sqlite3

class SQL():
	def avg_coordinates(self, coordinates):
		sum_lat = sum_long = 0

		for coord in coordinates:
			sum_lat += float(coord[1])
			sum_long += float(coord[0])

		return [sum_lat/len(coordinates), sum_long/len(coordinates)]

	def connect_db(self):
		return sqlite3.connect('database.db')

	def create_db(self):
		conn = self.connect_db()
		c = conn.cursor()
		c.execute('''CREATE TABLE tweets (id integer primary key, text_ text, lat real, long real)''')
		conn.commit()

		conn.close()

	def insert_into_db(self, text, coordinates):
		conn = self.connect_db()
		c = conn.cursor()

		coordinates = self.avg_coordinates(coordinates)

		c.executemany('''INSERT INTO tweets(text_, lat, long) VALUES (?,?,?)''', [(text, coordinates[0], coordinates[1])])

		conn.commit()

		conn.close()


#SQL().create_db()

