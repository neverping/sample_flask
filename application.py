from flask import Flask
from polls import create_app
import os

# Please use run.sh script to set this var to run locally:
if os.environ.get('FLASK_ENV'):
    application = create_app(debug_state=True)
    application.run()
else:
    application = create_app(debug_state=False)

