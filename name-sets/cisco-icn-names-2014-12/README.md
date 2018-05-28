The full original name-set are excluded on purpose because of their big sizes.

This directory contains files downloaded from http://www.icn-names.net/download/cisco-icn-names-2014-12_en.html. The script download_namesets.sh can be used to download the original compressed files from the main website.

This directory also includes the log file logNameset.py which contains some information about the data-set. This log file is the output of the execution of the python script "Nameset.py" stored in the parent directory. To produce the same logfile, you must run the script as follows:

python -u Nameset.py -f cisco-icn-names-2014-12/uncompressed/ -l 9 -p 2>&1 | tee cisco-icn-names-2014-12/logNameset.txt

The command above will also produce some plots.


