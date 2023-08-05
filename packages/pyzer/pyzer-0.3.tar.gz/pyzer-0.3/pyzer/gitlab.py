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

class GitLab:

      FILL={}
      FILL["stage"]="#f5f5f5"
      FILL["job"]="#dae8fc"
      FILL["terraform"]="#99ffcc"
      FILL["branch"]="#d5e8d4"
      FILL["ansible"]="#f8cecc"

      STROKE={}
      STROKE["stage"]="#6c9ebf"
      STROKE["job"]="#6c8ebf"
      STROKE["terraform"]="#82b366"
      STROKE["branch"]="#82b366"
      STROKE["ansible"]="#82b366"

      IMAGE={}
      IMAGE["stage"]="https://www.dropbox.com/s/ddf9xfjvete6xmv/stage-logo.png?raw=1"
      IMAGE["job"]="https://www.dropbox.com/s/xinbwsjsh0ezi8n/job-logo.png?raw=1"
      IMAGE["terraform"]="https://www.dropbox.com/s/ngptqgmji59j3h7/terraform-logo-1.png?raw=1"
      IMAGE["branch"]="https://www.dropbox.com/s/vf0nzuvj8lr61u2/gitbranch-logo.png?raw=1"
      IMAGE["ansible"]="https://www.dropbox.com/s/louj6pc6a3xb4gi/ansible-logo-1.png?raw=1"
      IMAGE["manual"]="https://www.dropbox.com/s/gjw7xqd7de23wmp/manual-logo.png?raw=1"

      PLAYBOOKS={}
      PLAYBOOKS["make -e run_playbook_repository"]="deploy-repository.yaml"
      PLAYBOOKS["make -e run_playbook_efs"]       ="deploy-efs.yaml"
      PLAYBOOKS["make -e run_playbook_services"]  ="deploy-services.yaml"

      HEADER="id,name,type,stage,when,terraform,branch,ansible,fill,stroke,image"

      LOG = logging.getLogger("app." + __name__)
      LOG.setLevel(logging.INFO)

      #def __init__(self):


      def startAnalysis(self, gitlabFile):
         print("\n**************************************************************************************")
         print(" ")
         print("   ____ _ _   _          _      ____ ___        _                _           _      ")
         print("  / ___(_) |_| |    __ _| |__  / ___|_ _|      / \   _ __   __ _| |_   _ ___(_)___  ")
         print(" | |  _| | __| |   / _` | '_ \| |    | |_____ / _ \ | '_ \ / _` | | | | / __| / __| ")
         print(" | |_| | | |_| |__| (_| | |_) | |___ | |_____/ ___ \| | | | (_| | | |_| \__ \ \__ \ ")
         print("  \____|_|\__|_____\__,_|_.__/ \____|___|   /_/   \_\_| |_|\__,_|_|\__, |___/_|___/ ")
         print("                                                                   |___/            ")
         print("\n**************************************************************************************")
         print(" ")
         self.loadYaml(gitlabFile)
         print ("\n ----------")
         print (" ---> Done!")
         print (" ----------")
         print("\n**************************************************************************************\n")

      def loadYaml(self, gitlabFile):
         GitLab.LOG.info("- Loading and Parsing " + gitlabFile)   
         with open(gitlabFile, 'r') as file:
            documents = yaml.load(file, Loader=yaml.FullLoader)

            drawio={}
            index_job=0

            for item, doc in documents.items() :
                  if item == "stages" :
                     self.loadStages(drawio, doc)

                  elif isinstance(doc,dict):
                     index_job += 1
                     id_job = "job-" + item + "-" + str(index_job) 
                     drawio[id_job] = {}
                     drawio[id_job]["id"]=id_job
                     drawio[id_job]["name"]=item
                     drawio[id_job]["type"]="job"
                     drawio[id_job]["stage"]=drawio["stage-" + doc["stage"]]["id"]
                     if  'when' in doc:
                        drawio[id_job]["when"]=doc["when"]
                     else:    
                        drawio[id_job]["when"]=""

                     GitLab.LOG.info("  - Parsing Job " + id_job + " (Stage " + drawio[id_job]["stage"] + ")")

                     # Terraform Commands
                     self.loadTerraformCommands(id_job, drawio, item, doc)

                     # Git Branches Applied
                     self.loadGitBranches(id_job, drawio, item, doc)

                     # Ansible
                     self.loadAnsible(id_job, drawio, item, doc)

            self.completeWihRelationShips(drawio)
            self.writeFile(drawio, gitlabFile)

      def loadStages(self, drawio, doc):
            for stage in doc:
               GitLab.LOG.info("  - Parsing Stage " + stage)
               id_stage = "stage-" + stage
               drawio[id_stage]={}
               drawio[id_stage]["id"]=id_stage
               drawio[id_stage]["name"]=stage
               drawio[id_stage]["type"]="stage"
               drawio[id_stage]["stage"]=""
               drawio[id_stage]["when"]=""
               drawio[id_stage]["terraform"]=""
               drawio[id_stage]["branch"]=""
               drawio[id_stage]["ansible"]=""

      def loadTerraformCommands(self, id_job, drawio, item, doc):
            terraformCommands=""
            script = doc["script"]
            for lineScript in script:
               if    "make -e init" in lineScript:
                     if len(terraformCommands) > 0:
                        terraformCommands=terraformCommands+","
                     terraformCommands = terraformCommands + "terraform-init"
               elif "make -e plan" in lineScript:     
                     if len(terraformCommands) > 0:
                        terraformCommands=terraformCommands+","  
                     terraformCommands = terraformCommands + "terraform-plan"
               elif "make -e apply" in lineScript:      
                     if len(terraformCommands) > 0:
                        terraformCommands=terraformCommands+","
                     terraformCommands = terraformCommands + "terraform-apply"
               elif "make -e destroy" in lineScript:      
                     if len(terraformCommands) > 0:
                        terraformCommands=terraformCommands+","
                     terraformCommands = terraformCommands + "terraform-destroy"            
            drawio[id_job]["terraform"]=terraformCommands        

      def loadGitBranches(self, id_job, drawio, item, doc):
            branches=""
            if "only" in doc:
               script = doc["only"]
               for lineBranch in script:
                  if len(branches) > 0:
                     branches=branches+","
                  branches = branches + "git-"+lineBranch
            drawio[id_job]["branch"]=branches

      def loadAnsible(self, id_job, drawio, item, doc):
            playbooks=""
            if "script" in doc:
               script = doc["script"]
               for lineScript in script:
                  found = False
                  for playbook in GitLab.PLAYBOOKS:
                     if playbook in lineScript:
                        if len(playbooks) > 0:
                           playbooks=playbooks+","
                        playbooks = playbooks + "ansible-" + GitLab.PLAYBOOKS[playbook]
                        found = True
                  if not found:
                     playbook = self.lookupAnsiblePlaybook(lineScript)
                     if playbook != "":
                        if len(playbooks) > 0:
                              playbooks=playbooks+","
                        playbooks = playbooks + "ansible-"+playbook      
            drawio[id_job]["ansible"]=playbooks

      def lookupAnsiblePlaybook(self, str):
            index1 = str.find("PLAYBOOK=")
            index2 = str.find(".yml",index1)
            if index1 > 0:
               if index2 < 0:
                  index2 = str.find(".yaml",index1)  
                  index2+=len("yaml")
               else:
                  index2+=len("yml")
               playbook=str[index1:index2+1].replace("'","").split("=")[1].split("/")[1]
               return playbook
            return ""   

      def completeWihRelationShips(self, drawio):
            # Inserting the others in order the relationship works
            listTerraformCommands=[]
            listGitBranches=[]
            listAnsiblePlaybook=[]

            for name in drawio:
               for str in drawio[name]["terraform"].split(","):
                     if str != "":
                        listTerraformCommands.append(str)
               for str in drawio[name]["branch"].split(","):
                     if str != "":
                        listGitBranches.append(str)
               for str in drawio[name]["ansible"].split(","):
                     if str != "":
                        listAnsiblePlaybook.append(str)              

            listTerraformCommands = list(dict.fromkeys(listTerraformCommands))
            listGitBranches       = list(dict.fromkeys(listGitBranches))
            listAnsiblePlaybook   = list(dict.fromkeys(listAnsiblePlaybook))

            for terra in listTerraformCommands:
                  drawio[terra]={}
                  drawio[terra]["id"]=terra
                  drawio[terra]["name"]=terra
                  drawio[terra]["type"]="terraform"
                  drawio[terra]["stage"]=""
                  drawio[terra]["when"]=""
                  drawio[terra]["terraform"]=""
                  drawio[terra]["branch"]=""
                  drawio[terra]["ansible"]=""

            for git in listGitBranches:
               drawio[git]={}
               drawio[git]["id"]=git
               drawio[git]["name"]=git
               drawio[git]["type"]="branch"
               drawio[git]["stage"]=""
               drawio[git]["when"]=""
               drawio[git]["terraform"]=""
               drawio[git]["branch"]=""
               drawio[git]["ansible"]=""

            for ansible in listAnsiblePlaybook:
               drawio[ansible]={}
               drawio[ansible]["id"]=ansible
               drawio[ansible]["name"]=ansible
               drawio[ansible]["type"]="ansible"
               drawio[ansible]["stage"]=""
               drawio[ansible]["when"]=""
               drawio[ansible]["terraform"]=""
               drawio[ansible]["branch"]=""
               drawio[ansible]["ansible"]=""


      def writeFile(self, drawio, gitlabFile):
         GitLab.LOG.info("- CVS Writing...")
         fileName=gitlabFile.replace(".yaml","").replace(".yml","") + ".csv"
         fileNameNoLayout=gitlabFile.replace(".yaml","").replace(".yml","")+"-nolayout.csv"

         if os.path.exists(fileName):
            os.remove(fileName)
         if os.path.exists(fileNameNoLayout):
            os.remove(fileNameNoLayout)   

         f   = open(fileName, "w")
         fnl = open(fileNameNoLayout, "w")
         self.writeLayoutHeader(f)
         f.write(GitLab.HEADER + "\n")
         fnl.write(GitLab.HEADER + "\n")

         for name in drawio:
            line = self.composeLine(name, drawio)
            f.write(line + "\n")
            fnl.write(line + "\n")

         f.close()
         GitLab.LOG.info("- CVS File writen")

      def composeLine(self, name, drawio):
         fill   = GitLab.FILL  [drawio[name]["type"]]
         stroke = GitLab.STROKE[drawio[name]["type"]]
         image  = GitLab.IMAGE [drawio[name]["type"]]

         if drawio[name]["when"] == "manual":
            image = GitLab.IMAGE["manual"]

         line =       drawio[name]["id"] + \
               ","   + drawio[name]["name"] + \
               ","   + drawio[name]["type"] + \
               ","   + drawio[name]["stage"] + \
               ","   + drawio[name]["when"] + \
               ",\"" + drawio[name]["terraform"] + "\"" + \
               ",\"" + drawio[name]["branch"]    + "\"" + \
               ","   + drawio[name]["ansible"] + \
               ","   + fill + \
               ","   + stroke + \
               ","   + image
         return line

      def writeLayoutHeader(self, f):
         f.write("#" + "connect: {\"from\": \"stage\",     \"to\": \"id\", \"invert\": true, \"style\": \"curved=1;fontSize=11;\"}\n")
         f.write("#" + "connect: {\"from\": \"terraform\", \"to\": \"id\",                 \"style\": \"curved=1;fontSize=11;\"}\n")
         f.write("#" + "connect: {\"from\": \"branch\",    \"to\": \"id\",                 \"style\": \"curved=1;fontSize=11;\"}\n")
         f.write("#" + "connect: {\"from\": \"ansible\",   \"to\": \"id\",                 \"style\": \"curved=1;fontSize=11;\"}\n")
         f.write("#" + "# Node label with placeholders and HTML.\n")
         f.write("#" + "# Default is '%name_of_first_column%'.\n")
         f.write("#" + "# label: %label%<br><i style=\"color:gray;\">%type%</i><br><a href=\"mailto:%email%\">Email</a>\n")
         f.write("#" + "# label: %label%<br><i style=\"color:gray;\">%type%</i>\n")
         f.write("#" + "label: %name%<br><b><i style=\"color:gray;\">%type%</i></b>\n")
         f.write("#" + "# Node style (placeholders are replaced once).\n")
         f.write("#" + "# Default is the current style for nodes.\n")
         f.write("#" + "style: label;image=%image%;whiteSpace=wrap;html=1;rounded=1;fillColor=%fill%;strokeColor=%stroke%;fontColor=#000000\n")
         f.write("#" + "# Node width. Possible value is a number (in px), auto or an @ sign followed by a column\n")
         f.write("#" + "# name that contains the value for the width. Default is auto.\n")
         f.write("#" + "width: auto\n")
         f.write("#" + "# Node height. Possible value is a number (in px), auto or an @ sign followed by a column\n")
         f.write("#" + "# name that contains the value for the height. Default is auto.\n")
         f.write("#" + "height: auto\n")
         f.write("#" + "# Padding for autosize. Default is 0.\n")
         f.write("#" + "padding: 0\n")
         f.write("#" + "# Name of layout. Possible values are auto, none, verticaltree, horizontaltree,\n")
         f.write("#" + "# verticalflow, horizontalflow, organic, circle. Default is auto.\n")
         f.write("#" + "layout: verticalflow\n")
         f.write("#" + "# Comma-separated list of ignored columns for metadata. (These can be\n")
         f.write("#" + "# used for connections and styles but will not be added as metadata.)\n")
         f.write("#" + "ignore: image, fill, stroke\n")
         f.write("#" + "# Node x-coordinate. Possible value is a column name. Default is empty. Layouts will\n")
         f.write("#" + "# override this value.\n")
         f.write("#" + "left: \n")
         f.write("#" + "# Node y-coordinate. Possible value is a column name. Default is empty. Layouts will\n")
         f.write("#" + "# override this value.\n")
         f.write("#" + "top: \n")
         f.write("#" + "# Node width. Possible value is a number (in px), auto or an @ sign followed by a column\n")
         f.write("#" + "# name that contains the value for the width. Default is auto.\n")
         f.write("#" + "width: auto\n")
         f.write("#" + "# Node height. Possible value is a number (in px), auto or an @ sign followed by a column\n")
         f.write("#" + "# name that contains the value for the height. Default is auto.\n")
         f.write("#" + "height: auto\n")
         f.write("#" + "# Parent style for nodes with child nodes (placeholders are replaced once).\n")
         f.write("#" + "parentstyle: swimlane;whiteSpace=wrap;html=1;childLayout=stackLayout;horizontal=1;horizontalStack=0;resizeParent=1;resizeLast=0;collapsible=1;\n")

         #with open('layout.py') as layout:
         #   for line in layout:
         #      f.write("#"+line)

      def loadLayoutHeader(self):
         with open('layout.py') as f:
            my_list = list(f)
         return my_list