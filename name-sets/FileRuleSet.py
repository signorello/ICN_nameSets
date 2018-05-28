from abc import ABCMeta, abstractmethod
import copy
import crcmod.predefined as crc
from Nameset import Nameset

class PrefixTrie():
  entries = {}
  
  def __init__(self, rootPrefix = "/"):
    self.rootNode = self.TrieNode(rootPrefix,0)
    self.prefix_counter = 1 # I do count the root one

  class TrieNode(object):
    component = ""
    children = []
    full_prefix = False # This is a very important flag which I use to mark a TrieNode as a complete prefix
    out_interface = None
  
    def __init__(self,component,level=0):
      self.component = component
      self.children = []
      self.level = level
      self.full_prefix = False
  
    def markAsPrefix(self):
      if(not self.full_prefix):
	self.full_prefix = True
	return True
      else:
	return False
      

    def specifyIface(self, interface):
      if self.full_prefix:
	self.out_interface = interface
	return 0
      else:
	return -1


  # not sure now that the root is always the point where you may need to add a prefix
  def add(self, prefix):
    # I assume node is passed as a list of strings/components
    if (prefix is not None):
      node = self.rootNode
      newPrefix = False
      out_level = 0

      for i,component in enumerate(prefix):
        foundInChild = False
        for child in node.children:
          if child.level == i+1 and child.component == component:
            node = child
            foundInChild = True
            break

        if foundInChild and i == len(prefix)-1:
          if(child.markAsPrefix()): 
            newPrefix = True
	    out_level = child.level
            
        if not foundInChild:
          new_node = self.TrieNode(component,i+1)
          node.children.append(new_node)
          node = new_node

          # now mark the last node as full prefix...how should that be done?
          if i == len(prefix)-1:
            new_node.markAsPrefix()
            newPrefix = True
	    out_level = new_node.level

      if (newPrefix):
        self.prefix_counter += 1
	return (True,out_level)
    
    return (False,0)

  def printPrefixes(self):
    node = self.rootNode
    prefix_str = self.rootNode.component
    print prefix_str
    for child in node.children:
      self.traverse(child,prefix_str,True)

  def getPrefixes(self):
    prefixes = {}
    node = self.rootNode
    prefix_str = self.rootNode.component
    print prefix_str
    for child in node.children:
      self.traverse(child,prefix_str,True)
    return prefixes
      
  def traverse(self,node,out_str,printFlag = False):
    if (not node.level == 0):
      out_str +=  (node.component + '/')

    if printFlag and node.full_prefix:
      print out_str
    for child in node.children:
      self.traverse(child,out_str,printFlag)



# The main idea of this class is to filter duplicate prefixes in a NameSet object
class FileRuleSet:
  nameset = None
  rules = {} # this should be a sort of a generic container where different kind/class of rules can be inserted
  entries = []

  def __init__(self, nameset):
    self.nameset = nameset
    self.prefixes = PrefixTrie()
    self.extractPrefixes()

  def extractPrefixes(self):
    for entry in self.nameset.names:
      entry.unplug_contentID()
      print entry.get_name()
      res,priority = self.prefixes.add(entry.components)
      if (res):
	self.entries.append((entry,priority))

  def get_length(self):
    return self.prefixes.prefix_counter

  def printRuleSet(self):
    self.prefixes.printPrefixes()


  #def createFibRules(self,ruleClass):
    # ideally I should iterate the prefix Trie and create the rule according to the type of rule specified via the constructor
    # hold on this until I decide how to implement the abstractFactory mechanism.

  
  def createNDNp4Rules(self,params,max_components,file_name = "ndnP4-fib.txt"):
    f = open(file_name,"w") 
    for entry,priority in self.entries:
      rule = Ndnp4FIBrule(entry,params, max_components,priority)
      f.write(rule.printEntry())
    f.close()

  #def updateRule(self):
    # tbd


#class RuleFactory:
#  factories = {}
#  def add

class AbstractFIBrule():
  __metaclass__ = ABCMeta
  nameEntry = "" # we assume the name is always passed as a Name Entry object, no matter how this is then converted to anything meaningful for the specific target
  parameters = {} # this is meant to include additional specific command names, like table_add, name of the tables, which may be needed to set once for all the rules generated

  def __init__(self, name,parameters):
    self.nameEntry = name
    self.parameters  = copy.copy(parameters)

  # we define an abstract method so that every subclass can feature its own way to print the FIB entry
  @abstractmethod
  def printEntry(self):pass


# Format of the rule by example:
# Entry: " /snt/sedan/state 1 " maps into:
# table_add fib_table set_egr 3 0&&&0 0&&&0 0x7ede&&&0xffff 0&&&0 0&&&0 => 2 3
# table_add fib_table set_egr 4 0&&&0 0&&&0 0x7ede&&&0xffff 0&&&0 0&&&0 => 2 3
# table_add fib_table set_egr 5 0&&&0 0&&&0 0x7ede&&&0xffff 0&&&0 0&&&0 => 2 3
# where 5 is the max number of components.
class Ndnp4FIBrule(AbstractFIBrule):
  num_ofC = 0 # this variable contains the max number of components for this ndn.p4 impl
  hash_func = "crc-16-mcrf4xx"
  # What follows 
  TABLE_NAME = "table_name"
  TABLE_CMD = "cmd"
  ACTION = "action"
  PARAM_DELIMITER = "param_delimiter"
  ACTION_DATA = "action_data" 

  def __init__(self, name, params,components,priority = 0):
    self.num_ofC = components
    self.priority = priority
    super(Ndnp4FIBrule,self).__init__(name, params)

  def setHashFunction(self,hashF):
    self.hash_func = hashF

  def printEntry(self):
    self.nameEntry.unplug_contentID()
    prefix = self.nameEntry.components

    rule_str = ""

    hashes_str = ['0&&&0'] * self.num_ofC

    hashes_str[len(prefix)-1] = self.computeHash()
    
    hash_str = ""
    for x in range(0,self.num_ofC - 1):
      hash_str += hashes_str[x] + " "

    for i in range(len(prefix),self.num_ofC):
      # table_add fib_table set_egr 3 0&&&0 0&&&0 0x7ede&&&0xffff 0&&&0 0&&&0 => 2 3
      rule_str += self.parameters[Ndnp4FIBrule.TABLE_CMD] + " " + self.parameters[Ndnp4FIBrule.TABLE_CMD] + " " + self.parameters[Ndnp4FIBrule.ACTION] + " " + str(i) + " " + hash_str + self.parameters[Ndnp4FIBrule.PARAM_DELIMITER] + " " + self.parameters[Ndnp4FIBrule.ACTION_DATA] + " " + str(self.priority) + "\n"

    return rule_str

  def computeHash(self):
    hash_fun = crc.Crc(self.hash_func)
    hash_fun.update(self.nameEntry.get_name(delimiter=""))

    return hash_fun.hexdigest()

  class Factory:
    def create(self): return Ndnp4FIBrule()



def main():
  params = {'table_name': 'fib_table', 'cmd': 'table_add', 'action': 'set_egr', 'param_delimiter': '=>', 'action_data': '1'}

  # let's test step by step
  # 1st: the subclass Ndnp4FIBrule and its methods to create and print the rule

 # my_nameset = Nameset("verysmallNameSet.txt",9)

 # for entry in my_nameset.names:
 #   rule = Ndnp4FIBrule(entry,params, 9)
 #   print rule.printEntry()

  # let's now the PrefixTrie implementation
  prefix_ns = Nameset("smallPrefixNameSet.txt",9)
  ns = FileRuleSet(prefix_ns) 
  print "The prefix name-set contains %s different prefixes" % ns.get_length()
  ns.printRuleSet()

  # let's print the NDNp4rules
  ns.createNDNp4Rules(params,9)

  # let's now try to create a factory class instead


if __name__ == '__main__':
    main() 
