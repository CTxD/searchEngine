from bs4 import BeautifulSoup
import urllib2

def readTextFromHtml(url):
    # Open request and extract source
    response = urllib2.urlopen(url)
    page_source = response.read()

    # Parse and return result
    soup = BeautifulSoup(page_source, 'html.parser')
    return soup.get_text()

def editDistance(doc1, doc2):
    # k-shrinkle factor
    k = 4

    # Process shrinkles of each file
    set1 = processShrinkle(doc1, k)
    set2 = processShrinkle(doc2, k)

    # Get jaccard Similarity of these shrinkles and return
    return processJaccardSimilarity(set1, set2)

def processJaccardSimilarity(shrinkle1, shrinkle2):
    # Get intersection and unions
    union_length = len(shrinkle1 | shrinkle2)
    intersection_length = len(shrinkle1 & shrinkle2)

    similarity = float(intersection_length) / float(union_length)

    return similarity

def processShrinkle(doc, k):
    # Get each word in the file
    split_doc = doc.split(' ')

    shrinkle_set = set()

    # Process shrinkles
    for i in range(len(split_doc)):
        shrinkle_string = ""

        for j in range(k):
            if i + k < len(split_doc):
                shrinkle_string += " " + split_doc[i + j]
            else:
                break
        shrinkle_set.add(shrinkle_string)

    return shrinkle_set