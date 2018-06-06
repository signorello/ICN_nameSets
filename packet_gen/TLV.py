class tlvc(Packet):
  name = "TLVC"
  fields_desc=[ ByteField("type", 0x08),
                BitFieldLenField("length", None, 8, length_of="value"),
                StrLenField("value", None, length_from = lambda pkt: pkt.length) ]

class tlvn(Packet):
  name = "TLVN"
  fields_desc=[ ByteField("type", 0x07),
                BitFieldLenField("length", None, 8, length_of="cmps"),
                PacketListField("cmps", None, tlvc, length_from=lambda pkt: pkt.length) ]
  

# -- SAMPLE INTERACTION --
# n=tlvn()
# n.cmps.append(tlvc(value='portugal'));
# n.cmps.append(tlvc(value='ulisboa'));
# n.cmps.append(tlvc(value='fciencias'));
# n.cmps.append(tlvc(value='index.html'));
# n.show() # NOTE: This displays None for lengths because they're only calculated when the packet is assembled, with the following line:
# raw(n)

class TLV(Packet):
  name = "TLV"
  fields_desc=[ ByteEnumField("type", 0x05,
                              { 5: "Interest",
                               6: "Data" }),
                               #7: "Name",
                               #8: "Component",
                               #10: "INTEREST-Nonce",
                               #20: "DATA-Metainfo",
                               #21: "DATA-Content",
                               #22: "DATA-SignatureInfo",
                               #23: "DATA-SignatureValue" } ),
                BitFieldLenField("length", None, 8, length_of="tlvn", adjust = lambda pkt, val: val + 4), 
                #Would be nice if it was something like val + pkt.nonce.sz instead, but ok
                PacketField("tlvn", None, tlvn),
                IntField("nonce", 0x00000000) ]
                
# p = TLV()
# p.tlvn = n  # NOTE: n is the result of the interaction in comment above
# p.show()
# raw(p)
# hexdump (p)