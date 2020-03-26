"""
This python file will consists of an analysis of the logs
"""
from parse_logs import parseLog as parse
import matplotlib

# Location can be either a folder location or
# a list of logs
file = 'G:\My Drive\Workload Logs'


def main():
    parse(file)



