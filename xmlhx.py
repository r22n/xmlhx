import sys
import xml.etree.ElementTree as ET
from MXMLNode import MXMLNode
from MXMLNode import makeMXMLNodefromElementTree
from Rule import *
from Queue import Queue

def eprint(message):
    print(message,sys.stderr)

commandline=sys.argv
if not (len(commandline)>=3):
    eprint("hint: mxmlhx <config file path> <mxml file path>")
    quit()
confxmlpath=commandline[1]
mxmlpath=commandline[2]

conf=None
try:
    conf=loadConf(confxmlpath)
except SyntaxError as e:
    eprint("config file of %s have missing syntax: %s"%(confxmlpath,e.message))
except:
    eprint("config file of %s has error"%confxmlpath)
if conf is None:
    quit()
mxmlrules=conf.getMXMLNodeRule()
haxe=conf.getHaxeRule()

mxml=None
try:
    mxml=makeMXMLNodefromElementTree(mxmlpath)
except:
    eprint("failed to parse mxml file")
if mxml is None:
    quit()

ruling=[mxml]
while len(ruling)>0:
    node=ruling.pop()
    for rule in mxmlrules:
        rule.apply(node)
    for child in node.getChildren():
        ruling.append(child)

declareID=haxe.getAttributeDeclareField()
declareIDUnknown=0
fillingID=[mxml]
while len(fillingID)>0:
    node=fillingID.pop()
    variable=None
    try:
        variable=node.getAttribute(declareID)
    except:
        variable="%s%d"%(node.getClassName(),declareIDUnknown)
        declareIDUnknown+=1
    node.addAttribute(declareID,variable)
    for child in node.getChildren():
        fillingID.append(child)

declarations=mxml.getChildren()
declareAccessor=haxe.getAccessorField()
while len(declarations)>0:
    node=declarations.pop()
    variable=node.getAttribute(declareID)
    print("%s var %s: %s;"%(declareAccessor,variable,node.getClassName()))
    for child in node.getChildren():
        declarations.append(child)

initializer=haxe.getMethodInitialize()
indent="\t"
initializations=Queue()
for i in mxml.getChildren():
    initializations.put(i)
haxeSetStyle=haxe.getMethodSetStyle()
haxeAddChild=haxe.getMethodAddChild()
print("%s function %s(): Void {"%(declareAccessor,initializer))
while not initializations.empty():
    node=initializations.get()
    variable=node.getAttribute(declareID)
    print("%s%s = new %s();"%(indent,variable,node.getClassName()))
    for key,value in node.getAttributes().iteritems():
        attformat=\
            "%s%s.%s = \"%s\";" if key==declareID else\
            "%s%s.%s = %s;"
        print(attformat%(indent,variable,key,value))
    for key,value in node.getStyles():
        print("%s%s.%s(\"%s\",%s);"%(indent,variable,haxeSetStyle,key,value))
    parent=node.getParent()
    if parent == mxml:
        print("%s%s(%s);"%(indent,haxeAddChild,variable))
    else:
        print("%s%s.%s(%s);"%(indent,parent.getAttribute(declareID),haxeAddChild,variable))
    for child in node.getChildren():
        initializations.put(child)
print("}")