from pathlib import Path
import sqlite3


conn = sqlite3.connect(str(Path(__file__).parent.parent) + "/SqlLite/example.db")
c = conn.cursor()

# #Tạo bảng dữ liệu
# c.execute('''
#             CREATE TABLE person
#             (id INTEGER PRIMARY KEY ASC, name varchar(250) NOT NULL)
#             ''')
# c.execute('''
#             CREATE TABLE address
#             (id INTEGER PRIMARY KEY ASC, street_name varchar(250), street_number varchar(250),
#             post_code varchar(250) NOT NULL, person_id INTEGER NOT NULL,
#             FOREIGN KEY(person_id) REFERENCES person(id))
#             ''')

# c.execute('''
#             INSERT INTO person VALUES(1, 'pythoncentral')
#             ''')
# c.execute('''
#             INSERT INTO address VALUES(1, 'python road', '1', '00000', 1)
#             ''')
# conn.commit()
# conn.close()

#Lấy dữ liệu
c.execute('SELECT * FROM person')
print(c.fetchall())
c.execute('SELECT * FROM address')
print(c.fetchall())
conn.close()