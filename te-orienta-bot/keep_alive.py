from flask import Flask
from threading import Thread

app = Flask('')


@app.route('/')
def home():
  return "I'm alive"


def run():
  app.run(host='0.0.0.0',
          port=8080,
          debug=False,
          use_reloader=False,
          threaded=False)


def keep_alive():
  t = Thread(target=run)
  t.start()
