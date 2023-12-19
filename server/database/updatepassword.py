
from tables import User, Session

from werkzeug.security import generate_password_hash

#userID = (request_data['empID'] or '')
#newPassword = (request_data['newPassword'] or '')
userID = ""
newPassword = ""

s = Session()
s.query(User).filter(User.emp_id == userID).update(
    {'password': generate_password_hash(
        newPassword, method='sha256')})
s.commit()
s.close()