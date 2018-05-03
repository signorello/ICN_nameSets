We leverage the data-sets available at http://www.icn-names.net

# Preliminary doc, this will be changed soon, since the code has been all written in a few hours time 

# Reading the file names
The class Nameset allows you to read the icn-names from a txt file and store them into a single object. A Nameset object holds a list of Entry objects, each containing a single name.
Follows a simple example on how to use the class:

#caveat: the following code snippet has been not tested, so it may contain errors
from Nameset.py import Nameset, Entry
...
...
...
# load the file and create the object
filename="./sample_names.txt"
my_nameset = Nameset(file_name)
# print and plot some stats about the names of the loaded data-set
my_nameset.printStats()
my_nameset.plotStats()

#if you wish to access every single name, for example, to create Interets packets, you only need to iterate the object's contents like follows:
for name in my_nameset.names:
  components = name.components // to extract the list of components
  // do whatever you like with the list of components, for ex., assuming you have written a scapy library to create an Interest
  ndn_interest = NDN(type=Interest, name=components, ......)
  pkt = Eth(...)/ndn_interest
  .......
  


