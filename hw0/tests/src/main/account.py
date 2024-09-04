import uuid,base64
from datetime import datetime

def generate_session_token():
    uuid_bytes = uuid.uuid4().bytes
    session_token = base64.b64encode(uuid_bytes).rstrip(b'=').decode('utf-8')
    return session_token


class Account:
    def __init__(self, username, password, name, status, updated=None , session_token=None):
        self.username = username
        self.password = password
        self.name = name
        self.status = status
        self.updated = updated if updated is not None else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.session_token = session_token if session_token is not None else generate_session_token()

    def update_status(self, new_status):
        if self.status == new_status:
            return False
        else:
            self.status = new_status
            self.updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return True

    def update_name(self, new_name):
        if self.name == new_name:
            return False
        else:        
            self.name = new_name
            self.updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return True

    def logout(self):
        self.session_token = None

