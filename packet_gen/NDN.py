# I have committed this file to keep track of the current version I was working on. So, please it is more a personal backup rather sth that should be committed.
# important reminder:
#
# When defining your own layer, you usually just need to define some *2*() methods, and sometimes also the addfield() and getfield().

# Interest ::= INTEREST-TYPE TLV-LENGTH
#              Name
#              CanBePrefix?
# 	       MustBeFresh?
# 	       ForwardingHint?
# 	       Nonce?
# 	       InterestLifetime?
# 	       HopLimit?
# 	       Parameters?
# 

# I think we should define two main classes derivates from the same one
# TLV container
# TLV value: here we can have multiple things too

class TLV(Packet):
  name = "TLV"
  fields_desc=[ ByteField("type", 0x05),
                BitFieldLenField("length", None, 8, length_of="value", adjust = lambda pkt, val: val/8), 
		PacketFieldList("value", None, TLV, length_from=lambda pkt: pkt.length-2)
		]

class Name(Packet):
    name= "Name"
    fields_desc=[ ByteField("type", 0x07),
                BitFieldLenField("length", None, 8, length_of="cmps"),
                PacketListField("cmps", None, Component, length_from=lambda pkt: pkt.length) ]


class Component(Packet):
  name = "Component"
  fields_desc=[ ByteField("type", 0x08),
                BitFieldLenField("length", None, 8, length_of="value"),
                StrLenField("value", None, length_from = lambda pkt: pkt.length) ]

class Interest(Packet):
    name= "Interest"
    fields_desc=[ ByteField("type", 0x05),
		  BitFieldLenField("length", None, 8, length_of="InterestValue",adjust = lambda pkt, val: val/8), 
		  InterestValue
		]

class InterestValue(Packet):
  name= "InterestValue"
  fields_desc=[ Name,

		]
		  Name,

		  CanBePrefix?
# 	       MustBeFresh?
# 	       ForwardingHint?
# 	       Nonce?
# 	       InterestLifetime?
# 	       HopLimit?
# 	       Parameters?

