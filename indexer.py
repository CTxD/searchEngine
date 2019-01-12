import json

class Indexer:
    def __init__(self):
        self.docs = self.initDocs()
        self.stripContentsOfDocs()
    
    # Init the crawled json file
    def initDocs(self): 
        with open("crawlContent.json") as json_file:
            data = json.load(json_file)
        
        del data[0] # Delete the "root" data entry

        return data

    def stripContentsOfDocs(self):
        stopwords = []
        docs = self.docs

        with open("stopwords.json") as stopwords_file:
            stopwords = json.load(stopwords_file)["words"]

        for i in range(1, len(self.docs)):
            doc = self.docs[i]["content"]

            newDocs = []
            token = ""
            for char in doc:
                if(char.isalnum()):
                    token += char
                else:
                    if token != "" and (e for e in stopwords if e != token):
                        newDocs.append(token)
                    token = ""

        with open("contentEdited.json", 'wb') as outFile:
            json.dump(newDocs, outFile)



    def tokenize(self, doc):
        return

indexer = Indexer()
