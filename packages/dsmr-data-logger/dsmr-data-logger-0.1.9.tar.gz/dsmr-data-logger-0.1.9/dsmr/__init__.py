
import os
import sys
import toml
from pathlib import Path
import logging
import time
from threading import Timer

from .datalogger import DataLogger

logging.basicConfig(stream=sys.stdout, level=os.environ.get('LOGLEVEL', logging.INFO))

def get_version():
   path = Path(__file__).resolve().parents[1] / 'pyproject.toml'
   pyproject = toml.loads(open(str(path)).read())
   return pyproject['tool']['poetry']['version']

__version__ = get_version()

class RepeatedJob(object):
  def __init__(self, interval, function, *args, **kwargs):
    self._timer     = None
    self.interval   = interval
    self.function   = function  
    self.args       = args
    self.kwargs     = kwargs
    self.is_running = False
    self.start()

  def _run(self):
    self.is_running = False
    self.start()
    self.function(*self.args, **self.kwargs)

  def start(self):
    if not self.is_running:
      self._timer = Timer(self.interval, self._run)
      self._timer.daemon = True
      self._timer.start()
      self.is_running = True

  def stop(self):
    self._timer.cancel()
    self.is_running = False