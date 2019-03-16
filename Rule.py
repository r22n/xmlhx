from MXMLNode import MXMLNode
import xml.etree.ElementTree as ET

class MXMLNodeMatcher:
    def __init__(self):
        pass
    def match(self,mxmlnode):
        return False
class MXMLNodeSupplyer:
    def __init__(self):
        pass
    def supply(self,mxmlnode):
        pass
class MXMLNodeRule:
    _matcher=None
    _supplyer=None
    def __init__(self,matcher,supplyer):
        if not (isinstance(matcher,MXMLNodeMatcher)and matcher is not None):
            raise ValueError("matcher must be MXMLNodeMachter and not none")
        if not(isinstance(supplyer,MXMLNodeSupplyer)and supplyer is not None):
            raise ValueError("supplyer must be MXMLNodeSupplyer and not none")
        self._matcher=matcher
        self._supplyer=supplyer
    def apply(self,mxmlnode):
        if not(isinstance(mxmlnode,MXMLNode)and mxmlnode is not None):
            raise ValueError("mxmlnode must be MXMLNode and not none")
        if self._matcher.match(mxmlnode):
            self._supplyer.supply(mxmlnode)

class TagMatcher(MXMLNodeMatcher):
    _fortag=None
    def __init__(self,fortag):
        MXMLNodeMatcher.__init__(self)
        if not(isinstance(fortag,basestring)and fortag is not None and fortag !=""):
            raise ValueError("fortag must be string value which is not none and none empty")
        self._fortag=fortag
    def match(self,mxmlnode):
        return mxmlnode.getClassName()==self._fortag
class AttributeMatcher(MXMLNodeMatcher):
    _forattribute=None
    def __init__(self,forattribute):
        MXMLNodeMatcher.__init__(self)
        if not(isinstance(forattribute,basestring)and forattribute is not None and forattribute!=""):
            raise ValueError("forattribute must be string value which is not none and not empty")
        self._forattribute=forattribute
    def match(self,mxmlnode):
        return mxmlnode.hasAttribute(self._forattribute)
class SuffixValueMatcher(MXMLNodeMatcher):
    _forattribute=None
    _suffix=None
    def __init__(self,forattribute,suffix):
        MXMLNodeMatcher.__init__(self)
        if not(isinstance(forattribute,basestring)and forattribute is not None and forattribute!=""):
            raise ValueError("forattribute must be string value which is not none and not empty")
        if not(isinstance(suffix,basestring)and suffix is not None and suffix!=""):
            raise ValueError("suffix must be string value which is not none and not empty")
        self._forattribute=forattribute
        self._suffix=suffix
    def match(self,mxmlnode):
        if not mxmlnode.hasAttribute(self._forattribute):
            return False
        attvalue=mxmlnode.getAttribute(self._forattribute)
        return attvalue.endswith(self._suffix)
class AllMatcher(MXMLNodeMatcher):
    _matchers=None
    def __init__(self,matchers):
        MXMLNodeMatcher.__init__(self)
        if not(isinstance(matchers,list)and matchers is not None and len(matchers)>0):
            raise ValueError("matchers must be not empty list")
        self._matcher=[]
        for matcher in matchers:
            if not(isinstance(matcher,MXMLNodeMatcher) and matcher is not None):
                raise ValueError("matchers must contain MXMLNodeMatcher only")
            self._matcher.append(matcher)
    def match(self,mxmlnode):
        for matcher in self._matcher:
            if not matcher.match(mxmlnode):
                return False
        return True

class TagSupplyer(MXMLNodeSupplyer):
    _after=None
    def __init__(self,after):
        MXMLNodeSupplyer.__init__(self)
        if not(isinstance(after,basestring)and after is not None and after!=""):
            raise ValueError("after must be string value which is not empty and not none")
        self._after=after
    def supply(self,mxmlnode):
        mxmlnode.setClassName(self._after)
class AttributeSupplyer(MXMLNodeSupplyer):
    _before=None
    _after=None
    def __init__(self,before,after):
        MXMLNodeSupplyer.__init__(self)
        if not(isinstance(after,basestring)and after is not None and after!=""):
            raise ValueError("after must be string value which is not empty and not none")
        if not(isinstance(before,basestring)and before is not None and before !=""):
            raise ValueError("before must be string value which is not none and not empty")
        self._after=after
        self._before=before
    def supply(self,mxmlnode):
        if not mxmlnode.hasAttribute(self._before):
            return
        attvalue=mxmlnode.getAttribute(self._before)
        mxmlnode.removeAttribute(self._before)
        mxmlnode.addAttribute(self._after,attvalue)
class StyleSupplyer(MXMLNodeSupplyer):
    _forattribute=None
    def __init__(self,forattribute):
        MXMLNodeSupplyer.__init__(self)
        if not(isinstance(forattribute,basestring)and forattribute is not None and forattribute!=""):
            raise ValueError("forattribute must be string value which is not empty and not none")
        self._forattribute=forattribute
    def supply(self,mxmlnode):
        if not mxmlnode.hasAttribute(self._forattribute):
            return
        attvalue=mxmlnode.getAttribute(self._forattribute)
        mxmlnode.removeAttribute(self._forattribute)
        mxmlnode.addStyle(self._forattribute,attvalue)
class QuoteSupplyer(MXMLNodeSupplyer):
    _forattribute=None
    def __init__(self,forattribute):
        MXMLNodeSupplyer.__init__(self)
        if not(isinstance(forattribute,basestring)and forattribute is not None and forattribute!=""):
            raise ValueError("forattribute must be string value which is not empty and not none")
        self._forattribute=forattribute
    def supply(self,mxmlnode):
        if not mxmlnode.hasAttribute(self._forattribute):
            return
        attvalue=mxmlnode.getAttribute(self._forattribute)
        mxmlnode.addAttribute(self._forattribute,"\"%s\""%attvalue)
class NumberSupplyer(MXMLNodeSupplyer):
    _forattribute=None
    def __init__(self,forattribute):
        MXMLNodeSupplyer.__init__(self)
        if not(isinstance(forattribute,basestring)and forattribute is not None and forattribute!=""):
            raise ValueError("forattribute must be string value which is not empty and not none")
        self._forattribute=forattribute
    def supply(self,mxmlnode):
        if not mxmlnode.hasAttribute(self._forattribute):
            return
        attvalue=mxmlnode.getAttribute(self._forattribute)
        mxmlnode.addAttribute(self._forattribute,self.convert(attvalue))
    def convert(self,test):
        begin=0
        size=len(test)
        while begin<size and not self.isdigit(test[begin]):
            begin+=1
        end=0
        while end<size and (self.isdigit(test[end]) or self.isdot(test[end])):
            end+=1
        return test[begin:end] if end - begin > 0 else "0"
    def isdigit(self,test):
        return "0" <= test and test <= "9"
    def isdot(self,test):
        return "."==test

class TagEraser(MXMLNodeSupplyer):
    def __init__(self):
        MXMLNodeSupplyer.__init__(self)
    def supply(self,mxmlnode):
        parent=mxmlnode.getParent()
        parent.removeChild(mxmlnode)
class AttributeEraser(MXMLNodeSupplyer):
    _forattribute=None
    def __init__(self,forattribute):
        MXMLNodeSupplyer.__init__(self)
        if not(isinstance(forattribute,basestring)and forattribute is not None and forattribute!=""):
            raise ValueError("forattribute must be string value which is not none and not empty")
        self._forattribute=forattribute
    def supply(self,mxmlnode):
        mxmlnode.removeAttribute(self._forattribute)

class HaxeRule:
    _methodAddChild=None
    _attributeDeclareField=None
    _setstyle=None
    _accessor=None
    _initialize=None
    def __init__(self,methodAddChild,attributeDeclareField,setstyle,accessor,initialize):
        if not(isinstance(methodAddChild,basestring)and methodAddChild is not None and methodAddChild!=""):
            raise ValueError("methodAddChild must be string value which is not empty and not none")
        if not(isinstance(attributeDeclareField,basestring)and attributeDeclareField is not None and attributeDeclareField!=""):
            raise ValueError("attributeDeclareField must be string value which is not empty and not none")
        if not(isinstance(setstyle,basestring)and setstyle is not None and setstyle!=""):
            raise ValueError("setstyle must be string value which is not empty and not none")
        if not(isinstance(accessor,basestring)and accessor is not None and accessor!=""):
            raise ValueError("accessor must be string value which is not empty and not none")
        if not(isinstance(initialize,basestring)and initialize is not None and initialize!=""):
            raise ValueError("initializ must be string value which is not empty and not none")
        self._methodAddChild=methodAddChild
        self._attributeDeclareField=attributeDeclareField
        self._setstyle=setstyle
        self._accessor=accessor
        self._initialize=initialize
    def getMethodAddChild(self):
        return self._methodAddChild
    def getAttributeDeclareField(self):
        return self._attributeDeclareField
    def getMethodSetStyle(self):
        return self._setstyle
    def getAccessorField(self):
        return self._accessor
    def getMethodInitialize(self):
        return self._initialize

class AppConf:
    _haxe=None
    _rules=None
    def __init__(self,haxe,rules):
        if not(isinstance(haxe,HaxeRule)and haxe is not None):
            raise ValueError("haxe must be not none")
        if not(isinstance(rules,list)and rules is not None):
            raise ValueError("rules must be list and not none")
        self._haxe=haxe
        self._rules=[]
        for rule in rules:
            if not(isinstance(rule,MXMLNodeRule)and rule is not None):
                raise ValueError("rules must contain MXMLNodeRule only")
            self._rules.append(rule)
    def getHaxeRule(self):
        return self._haxe
    def getMXMLNodeRule(self):
        res=[]
        for rule in self._rules:
            res.append(rule)
        return res

def makeRuleFromConfRule(rule):
    if rule is None:
        raise ValueError("rule must be not none")
    matchTag=None
    validMatchTag=False
    matchAttribute=None
    validMatchAttribute=False
    matchAttValueSuffix=None
    validMatchAttValueSuffix=False
    try:
        matchTag=\
            rule.find("./match/tag").text if rule.find("./match/tag") is not None else\
            None
        validMatchTag=matchTag is not None and matchTag != ""
        matchAttribute=\
            rule.find("./match/attribute").text if rule.find("./match/attribute") is not None else\
            None
        validMatchAttribute=matchAttribute is not None and matchAttribute!=""
        matchAttValueSuffix=\
            rule.find("./match/attvaluesuffix").text if rule.find("./match/attvaluesuffix") is not None else\
            None
        validMatchAttValueSuffix=matchAttValueSuffix is not None and matchAttValueSuffix!=""
        if not(validMatchTag or validMatchAttribute or validMatchAttValueSuffix):
            raise ValueError("tag or attribute or attvaluesuffix require valid text")
        if validMatchAttValueSuffix and not validMatchAttribute:
            raise ValueError("attvaluesuffix require attribute element")
    except:
        raise SyntaxError("tag or attribute was required, match/tag and match/attribute text is missing")

    supply=None
    hasSupply=False
    erase=None
    hasErase=False
    try:
        supply=rule.find("./supply")
        hasSupply=supply is not None
        erase=rule.find("./erase")
        hasErase=erase is not None
        if not((hasSupply and not hasErase) or (not hasSupply and hasErase)):
            raise ValueError("supply xor erase was required")
    except:
        raise SyntaxError("supply xor erase was required, both erase and supply is occurred or not occurred")
    
    tag=None
    validTag=False
    attribute=None
    validAttribute=False
    style=None
    validStyle=False
    quote=None
    validQuote=False
    number=None
    validNumber=False
    try:
        tag=\
            supply.find("./tag").text if hasSupply and  supply.find("./tag") is not None else\
            "a" if hasErase and erase.find("./tag") is not None else\
            None
        validTag=tag is not None and tag != ""
        attribute=\
            supply.find("./attribute").text if hasSupply and supply.find("./attribute") is not None else\
            "a" if hasErase and erase.find("./attribute") is not None else\
            None
        validAttribute=attribute is not None and attribute != ""
        style=\
            "a" if hasSupply and supply.find("./style") is not None else\
            "a" if hasErase and erase.find("./style") is not None else\
            None
        validStyle=style is not None
        quote=\
            "a" if hasSupply and supply.find("./quote") is not None else\
            "a" if hasErase and erase.find("./quote") is not None else\
            None
        validQuote=quote is not None
        number=\
            "a" if hasSupply and supply.find("./number") is not None else\
            "a" if hasErase and erase.find("./number") is not None else\
            None
        validNumber=number is not None
        if hasSupply and validAttribute and not validMatchAttribute:
            raise ValueError("supply attribute require match attribute")
        if hasSupply and validStyle and not validMatchAttribute:
            raise ValueError("supply style require match attribute")
        if hasSupply and validQuote and not validMatchAttribute:
            raise ValueError("supply quote require match attribute")
        if hasSupply and validNumber and not validMatchAttribute:
            raise ValueError("supply number require match attribute")
        if hasSupply and not (validTag or validAttribute or validStyle or validQuote or validNumber):
            raise ValueError("supply tag or attribute must be valid")
        if hasErase and not(validTag or validAttribute):
            raise ValueError("erase tag or attribute must be valid")
        if hasErase and validStyle:
            raise ValueError("erase tag can not have style")
        if hasErase and validQuote:
            raise ValueError("erase tag can not have quote")
        if hasErase and validNumber:
            raise ValueError("erase tag can not have number")
    except ValueError as e:
        raise SyntaxError("tag or attribute in supply missing syntax: %s"%e.message)
    except:
        raise SyntaxError("tag or attribute broken")
    
    matchers=[]
    if validMatchTag:
        matchers.append(TagMatcher(matchTag))
    if validMatchAttribute:
        matchers.append(AttributeMatcher(matchAttribute))
    if validMatchAttValueSuffix:
        matchers.append(SuffixValueMatcher(matchAttribute,matchAttValueSuffix))
    matcher=AllMatcher(matchers)
    tagrule=\
        TagEraser() if hasErase and validTag else\
        TagSupplyer(tag) if hasSupply and validTag else\
        None
    attributerule=\
        AttributeEraser(matchAttribute) if hasErase and validAttribute else\
        AttributeSupplyer(matchAttribute,attribute) if hasSupply and validAttribute else\
        None
    stylerule=\
        StyleSupplyer(matchAttribute) if hasSupply and validStyle else\
        None
    numberrule=\
        NumberSupplyer(matchAttribute) if hasSupply and validNumber else\
        None
    quoterule=\
        QuoteSupplyer(matchAttribute) if hasSupply and validQuote else\
        None
    
    res=[]
    if numberrule is not None:
        res.append(MXMLNodeRule(matcher,numberrule))
    if quote is not None:
        res.append(MXMLNodeRule(matcher,quoterule))
    if stylerule is not None:
        res.append(MXMLNodeRule(matcher,stylerule))
    if attributerule is not None:
        res.append(MXMLNodeRule(matcher,attributerule))
    if tagrule is not None:
        res.append(MXMLNodeRule(matcher,tagrule))
    return res


def loadConf(confxmlpath):
    if not(isinstance(confxmlpath,basestring)and confxmlpath is not None and confxmlpath!=""):
        raise ValueError("confxmlpath must be string value which is not empty and not none")
    conf=None
    try:
        conf=ET.parse(confxmlpath).getroot()
    except SyntaxError as e:
        raise SyntaxError("configuration file has missing syntax: %s"%(e.message))
    except:
        raise RuntimeError("configuration file of %s was not found or busy for reading and so on..."%(confxmlpath))
    
    haxeRuleAddChild=None
    haxeRuleDeclareField=None
    haxeRuleSetStyle=None
    haxeRuleAccessor=None
    haxeRuleInitialize=None
    try:
        haxeRuleAddChild=conf.find("./haxe/rule/addchild").text
        if not(haxeRuleAddChild is not None and haxeRuleAddChild!=""):
            raise ValueError("invalid method name addchild")
    except:
        raise SyntaxError("conf/haxe/rule/addchild text is missing")
    try:
        haxeRuleDeclareField=conf.find("./haxe/rule/declarefield").text
        if not(haxeRuleDeclareField is not None and haxeRuleDeclareField!=""):
            raise ValueError("invalid method name declarefield")
    except:
        raise SyntaxError("conf/haxe/rule/declarefield text is missing")
    try:
        haxeRuleSetStyle=conf.find("./haxe/rule/setstyle").text
        if not(haxeRuleSetStyle is not None and haxeRuleSetStyle!=""):
            raise ValueError("invalid method name setstyle")
    except:
        raise SyntaxError("conf/haxe/rule/setstyle text is missing")
    try:
        haxeRuleAccessor=conf.find("./haxe/rule/accessor").text
        if not(haxeRuleAccessor is not None and haxeRuleAccessor!=""):
            raise ValueError("invalid accessor name")
    except:
        raise SyntaxError("conf/haxe/rule/accessor text is missing")
    try:
        haxeRuleInitialize=conf.find("./haxe/rule/initialize").text
        if not(haxeRuleInitialize is not None and haxeRuleInitialize):
            raise ValueError("invalid initialize name")
    except:
        raise SyntaxError("conf/haxe/rule/initialize text is missing")
    haxe=HaxeRule(haxeRuleAddChild,haxeRuleDeclareField,haxeRuleSetStyle,haxeRuleAccessor,haxeRuleInitialize)

    rules=[]
    mxmlrules=conf.findall("./mxml/rule")
    for mxmlrule in mxmlrules:
        try:
            for rule in makeRuleFromConfRule(mxmlrule):
                rules.append(rule)
        except SyntaxError as e:
            raise SyntaxError("missing syntax while parsing rules: %s"%(e.message))
    
    return AppConf(haxe,rules)

