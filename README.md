# TextProcessing
The task was to implement and test a basic document retrieval system based on the vector space model, and to evaluate its performance over the CACM test collection under alternative configurations such as:stoplist, stemming or term weighting.

-----------------------------------------------------------------------------------------
Document retrieval system based on the vector space model.
Author: Diego Alejandro Cerda Contreras

Option List:
-h: help
-s: Enable the use of Stopwords.
-c FILENAME: Enter documents file
-q FILENAME: Enter queries file.
-i FILENAME: index.txt file.
-b: Enable Binary Weighting.
-m: Enter Manual Search Mode.
-e: Remove Stemming.
-o FILENAME:  Filename Results standard.

-----------------------------------------------------------------------------------------

Basic configuraion examples:
To run the scipt in default mode run:

CLI CODE:
		python assign.py -s stop_list.txt -c documents.txt -q queries.txt
		
The previous command will generate a "index.txt" containing the inverted Index dictionary,
once generated you may be use option -i to load the dictionary.

CLI CODE:
		python assign.py -s stop_list.txt -c documents.txt -q queries.txt -i index.txt

When using Stemming/Stopword you must remove the -i option to generate a new dictionary 
otherwise it will load the previous dictionary.

To disable Stemming use -e option:

CLI CODE:
		python assign.py -e -s stop_list.txt -c documents.txt -q queries.txt 
		
To disable Stopwords remove -s option:

CLI CODE:
		python assign.py -c documents.txt -q queries.txt 
		
MANUAL MODE:
The program also have manual search capability to enable it please use option "-m"

CLI CODE:
		python assign.py -m -s stop_list.txt -c documents.txt -q queries.txt

BINARY MODE:
To activate Binary Weighting please use "-b" option.

CLI CODE:		
		python assign.py -b -s stop_list.txt -c documents.txt -q queries.txt
		
OUTPUT MODE:
To print the top 10 results of each query on a file please use "-o:FILENAME" option.

CLI CODE:
		python assign.py -s stop_list.txt -c documents.txt -q queries.txt -o output_result.txt
