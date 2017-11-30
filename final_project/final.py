import requests
import json
import matplotlib.pyplot as plt
import time
from matplotlib import style
import aiml
import os

kernel = aiml.Kernel()

for f in os.listdir('aiml_data'):
    kernel.learn(os.path.join('aiml_data', f))
