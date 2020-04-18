import subprocess
import sys
import os

subprocess.call([sys.executable, "-m", "pip", "install", "-r", os.path.abspath(".." + os.sep + "requirements.txt")])
