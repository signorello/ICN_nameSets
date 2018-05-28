#!/bin/bash

# This script downloads and uncompress the name sets from icn-names.net
# You need to have xz-utils installed on your system

mkdir compressed uncompressed

for i in `seq 1 14`
do
	NAMESET=cisco-icn-names-2014-12_${i}.txt.xz
	wget http://www.icn-names.net/download/datasets/cisco-icn-names-2014-12/$NAMESET -P ./compressed
	unxz -k ./compressed/$NAMESET
	filename=${NAMESET%.*xz}
	mv ./compressed/$filename ./uncompressed/
done
