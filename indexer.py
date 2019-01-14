import json
import copy
import math

class Indexer:
    def __init__(self):
        self.docIdList = []
        self.docs = self.initDocs() # All the documents and their content, this is persistent, meaning that it can be used for DocID's too
        
        self.table = [[]]
        del self.table[0]

        self.tokenize() # Make the tokenized (term, freq, (ids)) list

        self.buildFrequencies() # Trim the table and add frequencies!

    # Init the crawled json file
    def initDocs(self): 
        with open("crawlContent.json") as json_file:
            data = json.load(json_file)
        
        del data[0] # Delete the "root" data entry

        for entry in data:
            self.docIdList.append(entry["url"]) # Init the list of DocId's

        return data

    def tokenize(self):
        stopwords = []
        docs = self.docs

        with open("stopwords.json") as stopwords_file:
            stopwords = json.load(stopwords_file)["words"]

        for i in range(0, len(self.docs)):
            doc = self.docs[i]["content"] # Get the content of i - document

            token = "" # Empty token init
            limit = 0
            for char in doc: # Tokenizing the document
                if limit > 4000: # This is done to limit the number of keywords for each doc (They got too big :o)
                    break
                if(char.isalnum()):
                    token += char
                else:
                    if token != "" and (e for e in stopwords if e != token): # Check if the token is either invalid or in the stopword list
                        self.table.append([token, 0, set([i]), []]) # Saving the token in the table for later - [0]: token, [1]: frequency, [2][i]: docId, [3][i] is the term frequency for doc i
                    token = ""
                    limit += 1
                
    # Merge duplicates of keywords, and count them as frequencies
    def buildFrequencies(self):
        # But first, we sort!
        self.table = sorted(self.table, key=lambda element: (element[0], element[2])) # First we sort after [0]: keyword and then [2]: docId
        
        freqList = []
        for i in range(0, len(self.table)): # Check for each row
            if i + 1 == len(self.table): # Terminate when we reach the end
                break

            frequency = 1
            freqList = []
            freqList.append(frequency)

            keyword1 = self.table[i][0]
            docSet1 = self.table[i][2]
            docVal1 = copy.copy(docSet1).pop()

            delNum = 0 # We need to keep track of how many we have deleted!
            newDocSet = docSet1
            
            for j in range(i+1, len(self.table) - delNum - 1): # But only going forward

                keyword2 = self.table[j - delNum][0]
                docVal2 = copy.copy(self.table[j - delNum][2]).pop()

                if keyword1 == keyword2:
                    if docVal1 == docVal2:
                        frequency += 1
                    else:
                        freqList.append(frequency)
                        frequency = 0

                    newDocSet = set.union(newDocSet, self.table[j-delNum][2]) # Union the docId from the set that is to be deleted

                    del self.table[j - delNum] # Delete the second keyword
                    delNum += 1
                else:
                    break

            self.table[i][1] = math.log10(len(self.table)/len(newDocSet)) # Update document frequency - With the idf value
            self.table[i][2] = newDocSet # Update the docId's

            newFreq = []
            for i in freqList:
                if i <= 0:
                    newFreq.append(1)
                else:
                    newFreq.append(math.log10(i) + 1)

            self.table[i][3] = newFreq # Update term frequency - With term weight

    def boolMatchQuery(self, query): # Query processing for not, and, or
        query = query.split(" ")    

        # A little validation
        if query[len(query) - 1] == "AND" or query[len(query) - 1] == "OR" or query[len(query) - 1] == "NOT" or query[0] == "AND" or  query[0] == "OR":
            print("Invalid Query!")

        # Build the predicate
        predicates = [] # For holding predicates
        returnFunctions = [] # For holding the set return functions
        
        returnDocIds = set() # For populating the set of pages that needs to be returned
        for i in range(0, len(query)):
            if query[i] == "NOT": # Not queries
                predicates.append((lambda entry: entry[0] != query[i])) # If the keyword is not equal to the query word
            elif query[i] == "OR": # Or queries
                predicates.append((lambda entry: entry[0] == query[i])) # If the keyword is equal to the query word
            else: # Any other
                predicates.append((lambda entry: entry[0] == query[i]))

            returnFunctions.append((lambda entry: set.union(returnDocIds, entry[2]))) # The return function for the query


        for entry in self.table: # Check all entries in the table
            for pred in predicates: # Check all predicates on all entries
                if pred(entry): # If it is true
                    returnDocIds = returnFunctions[predicates.index(pred)](entry) # Populate the return site with the return function 


        returnLinks = []
        for index in returnDocIds:
            returnLinks.append(self.docIdList[index]) # Map all the docIds to links

        return returnLinks # Return the links

indexer = Indexer()
print(indexer.boolMatchQuery("google universalauth"))

for row in indexer.table:
    break
    print("idf: ", row[1], " tf*: ", row[3]) # For ranking!
    