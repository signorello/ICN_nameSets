import matplotlib
matplotlib.use('Agg')
import sys
import time
import numpy as np
import copy
import os.path as op
import os
import matplotlib.pyplot as plt
import argparse
import statistics as st
import crcmod.predefined as crc

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
  max_comp = 0


  def __init__(self, filename,max_components = None):
    self.filename = filename
    if(max_components is not None):
      self.max_comp = max_components
    self.load_names(filename,max_components)


  def load_names(self, file_name, max_components = None):
    if not op.isfile(file_name):
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
      
      assert max(self.comp_lengths) <= max_components, "Your name-set object has loaded names longer than requested" 
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

    if(max_components is not None):
      if(len(name_components) > max_components):
	return None

    # it is useless to execute the following if already we have read a name whose length is equal
    # to the upper bound max_components
    #if((max_components != None) and not(self.max_comp == max_components)):
    if(max_components is None):
      if (len(name_components) > self.max_comp):
        self.max_comp = len(name_components)

    #print 'Entry: \" %s \"' % name_components

    name = Nameentry(name_components)

    return name

  def add(self,entry):
    self.names.add(entry)

  # this method returns a set containing the different names at a certain position in the prefixes of this nameSet object
  def getComponentsAt(self,index):
    components = set()
    for entry in self.names:
      if(index <= len(entry.components)-1):
	components.add(entry.components[index])
   
    return components

  # this method is meant to extract the common prefixes so to create FIB entries
  # again, I do not write any optimized code, so I am not picking up the most appropriate data-structure
  # for this purpose (most likely would have been a trie).

  def getPrefixes(self):
    prefixes = []
    # to be implemented
    return prefixes

  def printStats(self):

    print 'This name-set contains: \" %s \" entries' % len(self.names)

    print 'The average name length in components is %s with std_dev %s' % (self.avg_num_comp,self.std_num_comp)

    print 'The average name length in characters is %s with std_dev %s' % (self.avg_name_len,self.std_name_len)

    perc_filtered  = 0.0
    if (self.filtered_lines != 0):
      perc_filtered = self.filtered_lines * 100/(self.filtered_lines+len(self.names))
      print 'The percentage of filtered name is %s: ' % perc_filtered

    return self.avg_num_comp,self.std_num_comp,self.avg_name_len,self.std_name_len,perc_filtered

  def plotStats(self,comp_bins=None):
    nbins = (range(comp_bins) if comp_bins is not None else range(max(self.comp_lengths)))
    print 'nbins: %s' % nbins
    print "max components in plot %s " % max(self.comp_lengths)
    plt.hist(self.comp_lengths, bins=(range(comp_bins) if comp_bins is not None else range(max(self.comp_lengths))), normed=True)
    plt.title("Distribution of the number of components")
    plt.xlabel("Num of components")
    plt.ylabel("Probability")
    plt.savefig(self.filename  + "-comp_dist.png")

    plt.close()
    #plt.hist(self.n_lengths, bins=(name_bins if name_bins is not None else range(max(self.n_lengths))), normed=True)
    #plt.title("Distribution of the name lengths")
    #plt.xlabel("Name lengths")
    #plt.ylabel("Probability")
    #plt.savefig(self.filename  + "-name_len_dist.png")

  # This method is meant to retrieve statistical information to compare it with other NameSet objects
  # e.g., assume you want to compare the name length distribution of two different files
  def getStats(self):
    components_hist = plt.hist(self.comp_lengths, bins=range(max(self.comp_lengths)), normed=True)
    names_hist = plt.hist(self.n_lengths, bins=range(max(self.n_lengths)), normed=True)

    return names_hist, components_hist

class Nameentry:
  components = []
  content_id = None
  prefix = False
  name_len = 0

  def __init__(self, components):
    self.components = copy.copy(components)
    content_id = components[-1]
    for x in self.components:
      self.name_len += len(x)

  def length_inComponents(self):
    return len(self.components)

  def comp_lengths(self):
    lenghts = []
    for c in self.components:
      lengths.add(len(c))
    return lengths

  def get_name(self, protocol="", delimiter="/"):
    full_name = protocol 
    for x in self.components:
        full_name += delimiter + str(x)
    return full_name
        
  def plug_contentID(self):
    if(self.prefix and (content_id is not None)):
      self.components.append(content_id) 
      self.prefix = False
 
  def unplug_contentID(self):
    if(not self.prefix):
      del self.components[-1]
      # you do not need to worry about saving the content identifier, since that is stored at the beginning in data member in the object's constructor
      self.prefix = True

def parse_args():
    usage = """Usage:"""

    parser = argparse.ArgumentParser(usage)

    parser.add_argument('-f', help='file or directory containing the ICN names',
                        type=str, action="store", required=True, dest="file_name")

    parser.add_argument('-l', help='max number of components permitted',
                        type=int, action="store", required=False, dest="max_c")

    #parser.add_argument('-n', help='number of bins for the name length hist',
    #                    type=int, action="store", required=False, dest="max_bin_name")

    parser.add_argument('-p', help='Plot the probability distribution of name length in terms of components',
                        action="store_true", required=False, dest="plot")

    parser.add_argument('-c', help='number of bins for the components hist',
                        type=int, action="store", required=False, dest="max_bin_comp")

    return parser.parse_args()

def computeHashProb(name_set, hash_function):
  probability = 1.0
  hash_set = set()
  collisions = 0.0 

  for name in name_set:
    hash_fun = crc.Crc(hash_function)
    hash_fun.update(name)
    hash_res = hash_fun.hexdigest()

    if hash_res not in hash_set:
      hash_set.add(hash_res)
    else:
      collisions += 1.0

  #print "collisions holds %.2f" % collisions
  if(name_set.__len__() is not 0):
    probability = collisions /name_set.__len__()

  return probability

def main():
    global file_name

    args = parse_args()
    if args.file_name is not None:
      file_name = args.file_name

    onlyfiles = []
    if(op.isdir(file_name)):
      path_name = str(file_name)
      onlyfiles = [(path_name + f) for f in os.listdir(path_name) if op.isfile(path_name + f) and f.endswith(".txt")]
      #print "files %s" % onlyfiles
    else:
      onlyfiles.append(file_name)

    stats = {}
    coll_prob = {}
    for f in onlyfiles :
      print "processing file %s " % f
      my_nameset = Nameset(f,args.max_c)
      stats[f] = list( my_nameset.printStats() )

      # test getname function
      print "Test fullname %s " % my_nameset.names[0].get_name()

      if args.plot is not None:
        my_nameset.plotStats(comp_bins=args.max_bin_comp)

      print 'Max comp of the name set is %s ' % my_nameset.max_comp

      prob = []
      for i in range(0,my_nameset.max_comp-1):
        components = my_nameset.getComponentsAt(i)
        print 'There are %s different components at %s' % (components.__len__(),i)
        prob.append(computeHashProb(components, 'crc-16-mcrf4xx'))
        print 'Collision probability is  %s ' % prob

      prob_prefix = [None,None]
      prob_prefix.insert(2, prob[0] * prob[1])

      for j in range(3,len(prob)):
        prob_tmp = prob_prefix[j-1] * prob[j] 
	prob_prefix.insert(j, prob_tmp)
        print 'Collision probability for prefix of length %s is %.10f' % (j,prob_prefix[j])

      print "Prefix collision probabilities:"
      print prob_prefix

      coll_prob[f] = prob_prefix

    # Now that all the data sets have been processed we can compute the avg values
    # remember the tuples in your dictionary look like the following
    # stats[filename] = {avg_num_comp,std_num_comp,avg_name_len,std_name_len,perc_filtered}
    print "\n\nPrinting global stats about the processed name-sets"

    n = float(len(stats))
    for k,v in stats.items():
        print "k: %s and v: %s" % (k,v)

    r = tuple(sum(v[i] for k,v in stats.items())/n for i in range(5))
    print "{avg_num_comp,std_num_comp,avg_name_len,std_name_len,perc_filtered}"
    print r



if __name__ == '__main__':
    main()
