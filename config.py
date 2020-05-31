import string
import os

root_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    graphviz_dir = root_dir + '/graphviz'
