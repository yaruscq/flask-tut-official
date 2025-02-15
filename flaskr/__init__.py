# flaskr/__init__.py

# Instead of creating a Flask instance globally, you will create it inside a FUNCTION. This function is known as the application FACTORY. Any configuration, registration, and other SETUP the application needs will happen inside the function, then the application will be returned.

# The __init__.py serves double duty: 1) containing the application factory; 2) making the flaskr directory a PACKAGE

import os

from flask import Flask


# "__name__" is the name of the current Python module. App needs to know its location to set up paths
# 
def create_app(test_config=None):  # an app factory func

    # app = Flask(__name__, instance_relative_config=True)

    # 或是自行定義 instance path: 
    # Path to flaskr directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(current_dir)
    # 與 flaskr 同層
    # instance_path=os.path.join(current_dir, '..', 'cq', 'miko')
    
    # 在 flaskr folder 之下
    instance_path = os.path.join(current_dir, '..', 'flaskr', 'cq')

    app = Flask(__name__, instance_path=os.path.abspath(instance_path))
    app.config.from_mapping(
        SECRET_KEY='secerts',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite') 
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    
    # ensure the instance folder exists
    if not os.path.exists(app.instance_path):

        try:
            os.makedirs(app.instance_path)
        except OSError as e:
            print(f"\nError creating instance folder: {e}\n")
    else:
        print(f"\nInstance folder already exists at: {app.instance_path}\n")


    @app.route('/hello')
    def hello():
        return 'Hello World!'
    

    return app