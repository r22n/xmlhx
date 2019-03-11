import xml.etree.ElementTree as ET

class MXMLNode:
    _classname=None
    _attributes=None
    _styles=None
    _children=None
    _parent=None
    
    def setClassName(self,classname):
        if not(isinstance(classname,basestring)and classname is not None and classname != ""):
            raise ValueError("classname must be string value which is not none and not empty")
        self._classname=classname
    def getClassName(self):
        return self._classname
    def addAttribute(self,key,value):
        if not(isinstance(key,basestring)and key is not None and key != ""):
            raise ValueError("key must be string value which is not none and not empty")
        if not(isinstance(value,basestring)and value is not None and value!=""):
            raise ValueError("value must be string value which is not none and not empty")
        if self._attributes is None:
            self._attributes={}
        self._attributes[key]=value
    def hasAttribute(self,key):
        if not(key is not None and key != ""):
            return False
        if not isinstance(key,basestring):
            raise ValueError("key must be string")
        if self._attributes is None:
            self._attributes={}
        return key in self._attributes
    def removeAttribute(self,key):
        if not self.hasAttribute(key):
            raise ValueError("attributes does not contains key")
        if self._attributes is None:
            self._attributes={}
        del self._attributes[key]
    def getAttribute(self,key):
        if not self.hasAttribute(key):
            raise ValueError("attributes does not contain key")
        if self._attributes is None:
            self._attributes={}
        return self._attributes[key]
    def getAttributes(self):
        if self._attributes is None:
            self._attributes={}
        res={}
        for key,value in self._attributes.iteritems():
            res[key]=value
        return res
    def addStyle(self,key,value):
        if not(isinstance(key,basestring)and key is not None and key != ""):
            raise ValueError("key must be string value which is not none and not empty")
        if not(isinstance(value,basestring)and value is not None and value!=""):
            raise ValueError("value must be string value which is not none and not empty")
        if self._styles is not None:
            self._styles={}
        self._styles[key]=value
    def hasStyle(self,key):
        if not(key is not None and key!=""):
            return False
        if not isinstance(key,basestring):
            raise ValueError("key must be string")
        if self._styles is None:
            self.styles={}
        return key in self._styles
    def removeStyle(self,key):
        if not self.hasStyle(key):
            raise ValueError("styles does not contain key")
        if self._styles is None:
            self._styles={}
        del self._styles[key]
    def getStyle(self,key):
        if not self.hasStyle(key):
            raise ValueError("styles does not contain key")
        if self._styles is None:
            self._styles={}
        return self.styles[key]
    def getStyles(self):
        if self._styles is None:
            self._styles={}
        res={}
        for key,value in self._styles:
            res[key]=value
        return res
    def addChild(self,child):
        if not(isinstance(child,MXMLNode) and child is not None):
            raise ValueError("child must be MXMLNode and not none")
        if child.getParent() is not None:
            raise ValueError("child already has a parent")
        if child is self:
            raise ValueError("child must be different with self")           
        if self._children is None:
            self._children=[] 
        self._children.append(child)
        child._parent=self
    def hasChild(self,child):
        if child is None:
            return False
        if not isinstance(child,MXMLNode):
            raise ValueError("child must be MXMLNode")
        return child._parent == self
    def removeChild(self,child):
        if not self.hasChild(child):
            raise ValueError("child must be in children of parent its self")
        self._children.remove(child)
        child._parent=None
    def getParent(self):
        return self._parent
    def getChildren(self):
        if self._children is None:
            self._children=[]
        res=[]
        for child in self._children:
            res.append(child)
        return res

class ParsingPair:
    _source=None
    _destination=None
    def __init__(self,source,destination):
        if not(source is not None):
            raise ValueError("source is none")
        if not(isinstance(destination,MXMLNode)and destination is not None):
            raise ValueError("destination must be MXMLNode and not none")
        self._source=source
        self._destination=destination
    def getSource(self):
        return self._source
    def getDestination(self):
        return self._destination

def makeMXMLNodefromElementTree(mxmlpath):
    if not(isinstance(mxmlpath,basestring) and mxmlpath is not None and mxmlpath != ""):
        raise ValueError("mxmlpath must be string value which is not none and not empty")
    mxml=ET.parse(mxmlpath)
    res=MXMLNode()
    context=[ParsingPair(mxml.getroot(),res)]
    while len(context)>0:
        current=context.pop()
        src=current.getSource()
        dst=current.getDestination()

        dst.setClassName(src.tag)
        for key,value in src.attrib.iteritems():
            dst.addAttribute(key,value)
        
        for schild in src:
            dchild=MXMLNode()
            dst.addChild(dchild)
            context.append(ParsingPair(schild,dchild))
    return res
