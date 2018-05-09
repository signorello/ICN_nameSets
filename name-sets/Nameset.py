import sys
import time
import numpy as np
import copy
import os.path
import matplotlib.pyplot as plt
import argparse
import statistics as st

class Nameset:
  names = []
  n_lengths = []
  comp_lengths = []
  filtered_lines = 0
  avg_name_len = 0.0
  std_name_len = 0.0
  var_name_len = 0.0
  avg_num_comp = 0.0
  std_num_comp = 0.0
  var_num_comp = 0.0
  filename = ""


  def __init__(self, filename,max_components = None):
    self.filename = filename
    self.load_names(filename,max_components)


  def load_names(self, file_name, max_components = None):
    if not os.path.isfile(file_name):
            print "File %s does not exist" % file_name
	    sys.exit(-1)
    else:
      print "Reading ICN names from %s" % file_name

    f = open(file_name,'r')
    start = time.time()
    try: 

      for entry in f:
        name = self.process_entry(entry,max_components) 
	if(name != None):
	  self.names.append(name)
          self.n_lengths.append(name.name_len)
          self.comp_lengths.append(name.length_inComponents())
	else:
	  self.filtered_lines += 1

      self.compute_stats()

    finally:
      end = time.time()
      print "File read in %s sec" % (end-start)
      f.close()



  def compute_stats(self):
    self.avg_num_comp = st.mean(self.comp_lengths) 
    self.std_num_comp = st.stdev(self.comp_lengths) 
    self.var_num_comp = st.variance(self.comp_lengths,self.avg_num_comp) 

    self.avg_name_len = st.mean(self.n_lengths) 
    self.std_name_len = st.stdev(self.n_lengths) 
    self.var_name_len = st.variance(self.n_lengths,self.avg_name_len) 

  def process_entry(self, entry, max_components = None):
    #print 'Name: \" %s \"' % entry
    
    name_components = entry.split('/')
    #print 'Split: \" %s \"' % name_components

    if(max_components != None):
      if(len(name_components) > max_components):
	return None

    #print 'Entry: \" %s \"' % name_components

    name = Nameentry(name_components)

    return name

  def add(self,entry):
    self.names.add(entry)


  def printStats(self):
    print 'This name-set contains: \" %s \" entries' % len(self.names)

    print 'The average name length in components is %s with variance %s' % (self.avg_num_comp,self.var_num_comp)

    print 'The average name length in characters is %s with variance %s' % (self.avg_name_len,self.var_name_len)

    if (self.filtered_lines != 0):
      perc_filtered = self.filtered_lines * 100/(self.filtered_lines+len(self.names))
      print 'The percentage of filtered name is %s: ' % perc_filtered

  def plotStats(self):
    plt.hist(self.comp_lengths, bins=range(max(self.comp_lengths)), normed=True)
    plt.title("Distribution of the number of components")
    plt.xlabel("Num of components")
    plt.ylabel("Probability")
    plt.savefig("Components_distribution.png")

    plt.hist(self.n_lengths, bins=range(max(self.n_lengths)), normed=True)
    plt.title("Distribution of the name lengths")
    plt.xlabel("Name lengths")
    plt.ylabel("Probability")
    plt.savefig("Name_lengths_distribution.png")

  # This method is meant to retrieve statistical information to compare it with other NameSet objects
  # e.g., assume you want to compare the name length distribution of two different files
  def getStats(self):
    components_hist = plt.hist(self.comp_lengths, bins=range(max(self.comp_lengths)), normed=True)
    names_hist = plt.hist(self.n_lengths, bins=range(max(self.n_lengths)), normed=True)

    return names_hist, components_hist

class Nameentry:
  components = []
  name_len = 0

  def __init__(self, components):
    self.components = copy.copy(components)
    for x in self.components:
      self.name_len += len(x)

  def length_inComponents(self):
    return len(self.components)

  def comp_lengths(self):
    lenghts = []
    for c in self.components:
      lengths.add(len(c))
    return lengths

def parse_args():
    usage = """Usage:"""

    parser = argparse.ArgumentParser(usage)

    parser.add_argument('-f', help='file containing the ICN names',
                        type=str, action="store", required=True, dest="file_name")

    parser.add_argument('-c', help='max number of components permitted',
                        type=int, action="store", required=False, dest="max_c")

    return parser.parse_args()

def main():
    global file_name

    args = parse_args()
    if args.file_name is not None:
      file_name = args.file_name

    my_nameset = Nameset(file_name,args.max_c)
    my_nameset.printStats()
    my_nameset.plotStats()
    

if __name__ == '__main__':
    main()
