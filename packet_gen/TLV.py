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
# p=tlvn()
# p.cmps.append(tlvc(value='portugal'));
# p.cmps.append(tlvc(value='ulisboa'));
# p.cmps.append(tlvc(value='fciencias'));
# p.cmps.append(tlvc(value='index.html'));
# p.show()
# raw(p)

# Missing nonce accounting
class TLV(Packet):
  name = "TLV"
  fields_desc=[ ByteEnumField("type", 0x05,
                              { 5: "Interest",
                               6: "Data",
                               #7: "Name",
                               #8: "Component",
                               10: "INTEREST-Nonce",
                               20: "DATA-Metainfo",
                               21: "DATA-Content",
                               22: "DATA-SignatureInfo",
                               23: "DATA-SignatureValue" } ),
                BitFieldLenField("length", None, 8, length_of="tlvn"),# adjust=lambda pkt,x: pkt.length+4),
                PacketField("tlvn", None, tlvn),
                IntField("nonce", 0x00000000) ]