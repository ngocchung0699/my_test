from unicodedata import name
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Department(Base):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    department_id = Column(Integer, ForeignKey('department.id'))
    department = relationship(Department, backref=backref('employees', uselist=True))

from sqlalchemy import create_engine
engine = create_engine('sqlite:///Database/SQLAlchemy/sqlalchemy_example.db')

from sqlalchemy.orm import sessionmaker
session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)


john = Employee(name='john')
it_department = Department(name='IT')
john.department = it_department
s = session()
# s.add(john)
# s.add(it_department)
# s.commit()
it = s.query(Department).filter(Department.name == 'IT').first()

if it is not None:
    for i in it.employees:
        print(i.__dict__)
    # []
    print(it.employees[0].name)
    # u'john'

from sqlalchemy import select
find_it = select([Department.id]).where(Department.name == 'IT')
rs = s.execute(find_it)
rs

print('1', rs.fetchall())
# (1,)
print('2', rs.fetchone())  # Trả về một đối tượng đầu, nếu có, hoặc trả về None, nếu không có kết quả.
print('3', rs.fetchone())  # Nếu fetchone trả về None, ta lại lấy thêm 1 kết quả trả về tiếp theo.
print('4', rs.fetchone())  # Nếu fetchone trả về None, ta lại lấy thêm 1 kết quả trả về tiếp theo.
print('5', rs.fetchone())  # Nếu fetchone trả về None, ta lại lấy thêm 1 kết quả trả về tiếp theo.

find_john = select([Employee.id]).where(Employee.department_id == 1)
rs = s.execute(find_john)

print('4', rs.fetchone())  # Ta lấy được Employee ID của John
# (1,)
print('5', rs.fetchone())
