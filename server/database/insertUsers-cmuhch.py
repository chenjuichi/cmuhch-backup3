from tables import User, Setting, Session

import pymysql
from sqlalchemy import exc

from werkzeug.security import generate_password_hash

# --------------------------

# insert 7 users
s = Session()
# user 1
emp_id = "A12345"
emp_name = "陳瑞琪"
password = "a12345678"
new_user = User(emp_id=emp_id, emp_name=emp_name,
                password=generate_password_hash(password, method='sha256'))
s.add(new_user)

# user 2
emp_id = "T55142"
emp_name = "鄭幸文"
password = "a12345678"
new_user = User(emp_id=emp_id, emp_name=emp_name,
                password=generate_password_hash(password, method='sha256'))
s.add(new_user)

try:
    s.commit()
except pymysql.err.IntegrityError as e:
    s.rollback()
except exc.IntegrityError as e:
    s.rollback()
except Exception as e:
    s.rollback()

# --------------------------

# append department and permission data into user table
department = [6, 6]
permission = [2, 2]  # BY permission table id

user_objects = s.query(User).all()
users = [u.__dict__ for u in user_objects]
i = 1
for user in users:
    s.query(User).filter(User.id == i).update(
        {"dep_id": department[i-1], "perm_id": permission[i-1]})
    i = i+1

try:
    s.commit()
except pymysql.err.IntegrityError as e:
    s.rollback()
except exc.IntegrityError as e:
    s.rollback()
except Exception as e:
    s.rollback()

# --------------------------

# create setting table data
obj_list = []
settings = [{'items_per_page': 5, 'message': 'hello1'},  # 1
            {'message': 'hello2'},  # 2
            ]

for record in settings:
    user_setting = Setting(**record)
    obj_list.append(user_setting)

s.add_all(obj_list)
try:
    s.commit()
except pymysql.err.IntegrityError as e:
    s.rollback()
except exc.IntegrityError as e:
    s.rollback()
except Exception as e:
    s.rollback()


# --------------------------

# append setting data into user table
setting_objects = s.query(Setting).all()
new_settings = [u.__dict__ for u in setting_objects]

user_objects = s.query(User).all()
users = [u.__dict__ for u in user_objects]
i = 0
for user in users:
    s.query(User).filter(User.id == i+1).update(
        {"setting_id": new_settings[i]['id']})
    i = i+1

try:
    s.commit()
except pymysql.err.IntegrityError as e:
    s.rollback()
except exc.IntegrityError as e:
    s.rollback()
except Exception as e:
    s.rollback()

# --------------------------

s.close()

print("insert 2 user data is ok...")
