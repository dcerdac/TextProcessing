# -*- coding: utf-8 -*-
"""
USE: python <PROGNAME> (options) 
OPTIONS:
-h: help
-s: Enable the use of Stopwords.
-c FILENAME: Enter documents file
-q FILENAME: Enter queries file.
-i FILENAME: index.txt file.
-b: Enable Binary Weighting.
-m: Enter Manual Search Mode.
-e: Remove Stemming.
-o FILENAME:  Filename Results standard.

@author: Diego A .Cerda Contreras 
    Text Processing

"""

import sys, re, getopt, glob, json, math,operator
from nltk.stem import PorterStemmer
from read_documents import ReadDocuments


opts, args = getopt.getopt(sys.argv[1:],'bmhnes:c:i:q:o:')
opts = dict(opts)

def printHelp():
    help = __doc__.replace('<PROGNAME>',sys.argv[0],1)
    print('-' * 60, help, '-' * 60, file=sys.stderr)
    sys.exit() 

if '-h' in opts:
    printHelp()
   

######################################################
# STOPLIST option

stops = set()
if '-s' in opts:
    with open(opts['-s'],'r') as stop_fs:
        for line in stop_fs :
            stops.add(line.strip())
            

######################################################
# Identify collection documents

if '-c' in opts:
    collection_file = glob.glob(opts['-c'])
    documents = ReadDocuments(collection_file[0])
    print('Collection File:', ' '.join(collection_file), file=sys.stderr)

######################################################
# Identify Queries documents

if '-q' in opts:
    queries_files = glob.glob(opts['-q'])
    queries = ReadDocuments(queries_files[0]) 
    print('Queries File:', ' '.join(queries_files), file=sys.stderr)

######################################################
# Importing Dictionary

if '-i' in opts:
    index_file = glob.glob(opts['-i'])
    
    with open(index_file[0]) as f:
        invertedIndexDoccuments = json.load(f)        
    print('Index File: ', ' '.join(index_file), file=sys.stderr)
    print('<reading index file ....>', file=sys.stderr)

##############################-i invertedIndex.txt
  
################  GLOBAL VARIABLES ###################

wordRE = re.compile(r'[A-Za-z]+')
stemmer = PorterStemmer()

######################################################

# Returns the intersection of  two dictionaries.
def booleanRetreival ( document , queries):
    keys_a = set(document.keys())
    keys_b = set(queries.keys())
    intersection = keys_a & keys_b 
    #for key in intersection:        
        #inverseDocumentFrequency(document)
        #print("Documents found: ",document[key], key)    
    return intersection
 

#Returns a Dictionary of each word in the collection.
def indexingInvertedIndex(filename, id):
    totalDocuments =0
    invertedIndex = {}
    for index, doc in enumerate(filename):
        totalDocuments +=1
        for line in doc.lines:
             for word in wordRE.findall(line.lower()):
                if '-e' not in opts: 
                    word = stemmer.stem(word)
                if '-s' in opts:
                    #print("Stopwords Enabled")                    
                    if word not in stops:            
                        if word not in invertedIndex:
                           invertedIndex[word] = {}
                        if doc.docid in invertedIndex[word]:
                            invertedIndex[word][doc.docid] += 1
                        else:
                            invertedIndex[word][doc.docid] = 1
                else:  
                    #print("Stopwords Disable")                    
                    if word not in invertedIndex:
                        invertedIndex[word] = {}
                    if doc.docid in invertedIndex[word]:
                        invertedIndex[word][doc.docid] += 1
                    else:
                        invertedIndex[word][doc.docid] = 1
        #print(doc.printDoc())
        if index+1 == id:
            break
    print ("Total words in Collection: ",  len(invertedIndex), file=sys.stderr )
    return invertedIndex 
    
    
#Returns a dictionary of words for a Query Doc given its ID    
def indexingInvertedIndexByQueryID(filename, id):
    #Limit the Documents to index
    totalDocuments =0
    invertedIndex = {}
    for index, doc in enumerate(filename):
       # print("ID: ", doc.docid)
       if id == doc.docid: #Just one query
            totalDocuments +=1
            for line in doc.lines:
                 for word in wordRE.findall(line.lower()):
                    if '-e' not in opts: 
                        word = stemmer.stem(word)
                    if '-s' in opts:
                        #print("Stopwords Enabled")                    
                        if word not in stops:            
                            if word not in invertedIndex:
                               invertedIndex[word] = {}
                            if doc.docid in invertedIndex[word]:
                                invertedIndex[word][doc.docid] += 1
                            else:
                                invertedIndex[word][doc.docid] = 1
                    else:  
                        #print("Stopwords Disable")                    
                        if word not in invertedIndex:
                            invertedIndex[word] = {}
                        if doc.docid in invertedIndex[word]:
                            invertedIndex[word][doc.docid] += 1
                        else:
                            invertedIndex[word][doc.docid] = 1
    #print ("Total words in Queries: ",  len(invertedIndex) )
    return invertedIndex 
    
#This method its for the user input index.    
def manualUserQuery (line): 
    invertedIndex = {}
    for word in wordRE.findall(line.lower()):
        if '-e' not in opts: 
            word = stemmer.stem(word)
        if '-s' in opts:
            #print("Stopwords Enabled")                    
            if word not in stops:         
                if word not in invertedIndex:
                    invertedIndex[word] = {}
                if word in invertedIndex[word]:
                    invertedIndex[word][1] += 1
                else:
                    invertedIndex[word][1] = 1
        else:  
            if word not in invertedIndex:
                invertedIndex[word] = {}
            if word in invertedIndex[word]:
                invertedIndex[word][1] += 1
            else:
                invertedIndex[word][1] = 1
    print ("Total words in Query: ",  len(invertedIndex) )
    return invertedIndex  
    
#Number of Documents in the Collection.
def getTotalDocumentsCollection(documents):
    count = 0
    for doc in documents:
        count += 1
    return count

#IDF  inverseDocumentFrequency.
def inverseDocumentFrequency(dictionary, word, total):       
    value = dictionary.get(word, 0)
    if value is 0:
        return 0
    else: 
        inverseFrequency =len(dictionary[word])
        return math.log10(total/inverseFrequency)
    
#TF termFrequency / -b Binary
def termWeighting(dictionary, word, docID):    
    if '-b' in opts:
        #print ("Binary Weigthing Mode")
        if dictionary.get(word, {}).get(docID, 0) >= 1:
            return 1
        else:
            return 0
    else:
        return dictionary.get(word, {}).get(docID, 0)

#documentSize gives the size of a given Document ID -Not in Use-
def documentSize(dicctionary, docid, totalDocuments):
    count = 0
    for word in dicctionary:        
        TF = termWeighting(dicctionary,word,docid)        
        IDF = inverseDocumentFrequency(dicctionary,word,totalDocuments)        
        count +=math.pow(TF*IDF,2)
        #print(count)        
    return math.sqrt(count)
           
# Returns a Dictionary containing every size of each document in a collection.
def totalDocumentSize(index):
    dfw = {}#dfw
    idf = {}#log(\D\dfw) idf
    TFIDF = {} #TF.IDF
    for word in index:
        dfw[word]= len(index[word])        
    totalDocuments = getTotalDocumentsCollection(documents)         
    for word in dfw:
            idf[word] = math.log10(totalDocuments/dfw[word])    
    for word in index:
        for doc in index[word]:
            if doc in TFIDF:
                if '-b' in opts:  
                    TFIDF[doc] += math.pow(idf[word] * (index[word][doc]/index[word][doc]), 2)
                else:
                    TFIDF[doc] += math.pow(idf[word] * (index[word][doc]), 2)               
            else:
                 TFIDF[doc] = 0
                 if '-b' in opts: 
                     TFIDF[doc] += math.pow(idf[word] * (index[word][doc]/index[word][doc]), 2)
                 else:
                     TFIDF[doc] += math.pow(idf[word] * (index[word][doc]), 2)
    for doc in TFIDF:
         TFIDF[doc] = math.sqrt(TFIDF[doc])
    return TFIDF   
    
# Calculates the Qi*Di of the each word within the Document.
def qidi (invertedIndexDoccuments, invertedIndexQueries,QueryID ):
    inter = booleanRetreival(invertedIndexDoccuments,invertedIndexQueries) #Intersection Query VS Document
    tfidf_w ={}    
    totalDocuments = getTotalDocumentsCollection(documents) # |D|    
    for wd in inter:
        for doc in invertedIndexDoccuments[wd]:     
            IDF = inverseDocumentFrequency(invertedIndexDoccuments, wd, totalDocuments )            
            doc_TF_IDF=  (termWeighting(invertedIndexDoccuments, wd, doc) *IDF)
            que_TF_IDF=  (termWeighting(invertedIndexQueries, wd, QueryID)*IDF) 
            TOTAL_TFIDF = doc_TF_IDF*que_TF_IDF
            if doc in tfidf_w:
                 tfidf_w[doc] += TOTAL_TFIDF
            else:
                tfidf_w[doc] = TOTAL_TFIDF               
    return tfidf_w 

# Get the Distance between Doc. vs. Query. 
def vectorCompute (size, numerator, invertedIndexDoccuments):    
    master = {}
    for doc in size:    
        master[doc] = numerator.get(doc,0)/size[doc]
    return master

######################################################
# -i [filename] If no index file specified then      #
#               save it into a new index file        #
######################################################
totalDocuments = getTotalDocumentsCollection(documents) 
if '-i' not in opts:
    invertedIndexDoccuments = indexingInvertedIndex(documents,totalDocuments)
    with open('index.txt', 'w') as f:
        json.dump(invertedIndexDoccuments, f)
        print("\n** Writting Inverted Index on File <index.txt> **", file=sys.stderr)
        
        
########## MAIN / VARIABLE DECLARATION ############### 

print("-"*30)

#invertedIndexDoccuments = indexingInvertedIndex(documents,totalDocuments)
totalQueries =getTotalDocumentsCollection(queries)
size = totalDocumentSize(invertedIndexDoccuments)


######################################################
# -m [option] Switch between Manual/QueryID mode.    #
######################################################
if '-m' in opts:     
    var = input("Please enter search query: ")
    invertedIndexQueries= manualUserQuery(var)
    numerator =qidi (invertedIndexDoccuments, invertedIndexQueries, 1)
    vector = vectorCompute(size,numerator,invertedIndexDoccuments)

else:
    try:
        QueryID = int(input("Enter Query ID 1-64: "))      
        if not (1 <= QueryID <= 64):
            raise ValueError()
        #Get the invertedIndex from the Query
        invertedIndexQueries =indexingInvertedIndexByQueryID(queries, QueryID)
        numerator =qidi (invertedIndexDoccuments, invertedIndexQueries, QueryID)
        vector = vectorCompute(size,numerator,invertedIndexDoccuments) #Doc distance
    except ValueError:
        print ("Invalid Option, you needed to type between 1-64.")
        sys.exit()

######################################################
#   Always show the top 5 Results of any search.     #
######################################################
sorted_x = sorted(vector.items(), key=operator.itemgetter(1), reverse=True)
print ("Showing top 5 results: ", file=sys.stderr)
for doc in range(5):
   print("%s) Doc. No: %s " % (doc+1,sorted_x[doc][0]), file=sys.stderr)
   

######################################################
# -o [filename] Computes 10 Top results of each      #
#               query and saves it in the file.      #
######################################################
if '-o' in opts:    
    lex = open(opts['-o'],'w')
    for i in range(1,totalQueries+1,1):
        invertedIndexQueries =indexingInvertedIndexByQueryID(queries, i)
        numerator =qidi (invertedIndexDoccuments, invertedIndexQueries, i)
        vector = vectorCompute(size,numerator,invertedIndexDoccuments)
        sorted_x = sorted(vector.items(), key=operator.itemgetter(1), reverse=True)
        for doc in range(10): 
            print(i, sorted_x[doc][0], end="\n", file=lex)
    print(file=lex)
    lex.close()


    