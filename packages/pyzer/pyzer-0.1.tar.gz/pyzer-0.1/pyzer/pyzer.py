#
# Author: Ualter Azambuja Junior
# ualter.junior@gmail.com
#
#
# pip install pyyaml
# https://pyyaml.org/wiki/PyYAMLDocumentation
# https://jgraph.github.io/drawio-tools/tools/csv.html
#
#

import os
import yaml
import json
import logging
import sys
import gitlab as G


class Pyzer:
     LOG = logging.getLogger("app." + __name__)
     LOG.setLevel(logging.INFO)

     def __init__(self):
          if not os.path.exists("log"):
             os.makedirs("log")

          rootLogger = logging.getLogger()
          logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")

          fileHandler = logging.FileHandler("{0}/{1}.log".format("./log", "py-analyzer"))
          fileHandler.setFormatter(logFormatter)
          fileHandler.setLevel(logging.INFO)
          rootLogger.addHandler(fileHandler)

          consoleHandler = logging.StreamHandler(sys.stdout)
          consoleHandler.setFormatter(logFormatter)
          consoleHandler.setLevel(logging.INFO)
          rootLogger.addHandler(consoleHandler)

          self.start();

     def start(self):
          if len(sys.argv) < 3 :
               print (" ")
               print ("Missing argument!")
               print (" ")
               print (" usage: py-analyzer.py -gitlab [file Gitlab-CI.yaml]")
               print ("  ")
               print (" Example:")
               print ("    python py-analyzer.py -gitlab .gitlab-ci.yaml")
               print (" ")
               sys.exit()
          else:
               type = sys.argv[1]
               file = sys.argv[2]     
          if type == "-gitlab":   
               gitlab = G.GitLab()     
               gitlab.startAnalysis(file)
          else:
               print (" ")
               print(" Type " + type + "not expected!")  
               print (" ") 


if __name__ == '__main__':
    pyzer = Pyzer()
