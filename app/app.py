from flask import Flask
from logging import FileHandler

from new_group.ext import NewGroupApp

app = Flask(__name__)

file_handler = FileHandler('/var/log/cache-db/uwsgi.log')
app.logger.addHandler(file_handler)
app.logger.setLevel('INFO')

NewGroupApp(app)

if __name__ == '__main__':
    app.run()