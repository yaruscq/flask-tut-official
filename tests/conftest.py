import sys
import os
import tempfile
import pytest
# Add the 'flaskr' directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../flaskr')))

print(sys.path)
from flaskr import create_app
from flaskr.db import get_db, init_db



# current_dir = os.path.dirname(os.path.abspath(__file__))

# instance_path = os.path.join(current_dir, '..', 'flaskr', 'cq')

# app = Flask(__name__, instance_path=os.path.abspath(instance_path))


# Read the data.sql file
with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE' : db_path,
    })

    with app.app_context():
        init_db()
        # get_db().execute(_data_sql)
        get_db().executescript(_data_sql)
    
    yield app

    os.close(db_fd)
    os.unlink(db_path)



@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


""" Authentication """

class AuthActions(object):
    def __init__(self, client):
        self._client = client
    
    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password' : password}
        )
    
    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)
