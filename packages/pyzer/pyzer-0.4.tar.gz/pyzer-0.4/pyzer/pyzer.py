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
from pyzer.gitlab import GitLab
#from gitlab import GitLab


class Pyzer:
     LOG = logging.getLogger("app." + __name__)
     LOG.setLevel(logging.INFO)

     def __init__(self):
          if not os.path.exists("log"):
             os.makedirs("log")

          rootLogger = logging.getLogger()
          logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")

          fileHandler = logging.FileHandler("{0}/{1}.log".format("./log", "py-typeAnalysiszer"))
          fileHandler.setFormatter(logFormatter)
          fileHandler.setLevel(logging.INFO)
          rootLogger.addHandler(fileHandler)

          consoleHandler = logging.StreamHandler(sys.stdout)
          consoleHandler.setFormatter(logFormatter)
          consoleHandler.setLevel(logging.INFO)
          rootLogger.addHandler(consoleHandler)

          self.start();

     def start(self):
          color        = False
          typeAnalysis = ""
          file         = ""
          if len(sys.argv) < 3 :
               print ("Missing argument!")
               self.showSyntax()
               sys.exit()
          else:
               index=0
               size=len(sys.argv)
               for p in sys.argv[1:]:
                  index+=1
                  if p == "--color":
                       color = True
                  elif p == "--gitlab":
                       typeAnalysis = p
                       file  = sys.argv[index+1]
          if typeAnalysis == "--gitlab":   
               gitlab = GitLab(color)     
               gitlab.startAnalysis(file)
          elif typeAnalysis == "":     
               print (" ")
               print(" Type of analysis not found")  
               self.showSyntax()
          else:
               print (" ")
               print(" Type of analysis \"" + typeAnalysis + "\" not expected!")  
               self.showSyntax() 

     def showSyntax(self):          
         print (" ")
         print ("**********************************************")
         print (" ")
         print (" usage: pyzer [--color] [--gitlab FILE.yaml]")
         print ("  ")
         print (" Example:")
         print ("    pyzer --gitlab .gitlab-ci.yaml")
         print ("    pyzer --color --gitlab .gitlab-ci.yaml")
         print ("**********************************************")
         print (" ")


if __name__ == '__main__':
    pyzer = Pyzer()
