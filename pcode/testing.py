from bs4 import BeautifulSoup
import urllib2
import nltk
import nltk.corpus
from nltk.corpus import PlaintextCorpusReader
import SearchingTools
import Searches

def main():
    #page = "http://en.wikipedia.org/wiki/Achilles"
    #urllib2.urlopen(page)
    #run()
    testCorpus("http://en.wikipedia.org/wiki/Achilles", "corpus")
    return

def testCorpus(url, file_name):
    corpus_context = createCorpus(url, file_name)
    print("Similar: \n{}".format(get_similar_words(corpus_context, "achilles")))
    return

def createCorpus(url, file_name):
    """
    This method takes a
    :param url: url of the web page as a string to start making a corpus from
    :param file_name: name of a file as a string where the corpus will be written to
    :return: return a ContextIndex of a corpus
    """
    page = BeautifulSoup(urllib2.urlopen(url).read())
    __add_from_page__(file_name, page, True)

    #Only expand the first <p> section; doing all <p> sections will take way too long
    #Using only this first <p> section useful information is retrieved anyway
    for link in page.p.find_all('a'):
        #Filter out links not linking to useful content
        if link.string is not None and '&' not in link.get('href') and ':' not in link.get('href'):
            url = "http://en.wikipedia.org" + link.get('href')
            new_page = BeautifulSoup(urllib2.urlopen(url).read())
            __add_from_page__(file_name, new_page, False)

    my_file = open(file_name, 'r')
    length = 0
    for line in my_file:
        length += len(line)
        print line

    #Create the corpus; no list- just the one file, thus the ''
    my_corpus = PlaintextCorpusReader('', '.*').words('corpus')
    #Corpus Context; creating a ContextIndex is necessary for extracting similar words
    #each word is put into lowercase to avoid problems (...similar_words('achilles') != similar_words('Achilles')
    corpus_context = nltk.text.ContextIndex([word.lower() for word in my_corpus])

    return corpus_context

def get_similar_words(corpus_context_index, compare_to):
    """
    :param corpus_context_index: ContextIndex for corpus
    :param compare_to: word used to find similar words
    :return: list containing similar words to compare_to
    """
    #compare_to is cast into lower case to avoid getting empty or unhelpful lists of similar words
    return corpus_context_index.similar_words(compare_to.lower())

def __add_from_page__(file, page, rewrite, only_first = False):
    """
    This method writes all <p> sections of a HTML file (Beautiful Soup) to a file
    :param file: name of file to write to as a string
    :param page: web page read by urllib2 made into BeautifulSoup
    :param only_first: boolean; only write the first paragraph
    :param rewrite: boolean; start the file new by deleting existing data
    :return: do not return anything
    """
    action = 'w' if rewrite else 'a'
    file = open(file, action)

    if only_first:
        paragraph = page.p
        text = paragraph.get_text().encode('ascii', 'ignore')
        file.write(text + '\n')
    else:
        for paragraph in page.find_all('p'):
            text = paragraph.get_text().encode('ascii', 'ignore')
            file.write(text + '\n')
    return

def run():
    start_url = "http://en.wikipedia.org/wiki/Achilles"
    finish_url = "http://en.wikipedia.org/wiki/Wine"
    my_problem = SearchingTools.WikipediaProblem(start_url, finish_url)
    agent = SearchingTools.WikipediaAgent(Searches.breadthFirstSearch, my_problem)
    agent.register()
    agent.printPath()

def problemTesting():
    print("Begin testing")
    my_problem = SearchingTools.WikipediaProblem("http://en.wikipedia.org/wiki/Achilles", "http://en.wikipedia.org/wiki/Greek_mythology")
    start_state = my_problem.get_start_state()
    print("Start state: {}".format(start_state))
    print("Start state is goal state?: {}".format(my_problem.is_goal_state(start_state)))
    successors = my_problem.get_successors(start_state)
    print("Successors: ")
    for successor in successors:
        if my_problem.is_goal_state(successor):
            print("Found goal state!:\n{}".format(successor))
    return

# html_raw = urllib2.urlopen("http://en.wikipedia.org/wiki/Achilles").read()
# html_soup = BeautifulSoup(html_raw)
#
# links = html_soup.find_all('a')
# for link in links:
#     print(link)
#
#
# print("Paragraphs: \n")
# for paragraph in html_soup.find_all('p'):
#     for link in paragraph.find_all('a'):
#         #Each link is a Tag object; sometimes instead of a link there's a #cite_note-##
#         #These are identified by having a string of "None" instead of the name following /wiki/
#         #Sometimes a /w/ is also encountered, I do not know what that means.
#         if link.string is not None:
#             print(link.get('href'))

#for paragraph in html_soup.p():
#   print(paragraph.get_text())

if __name__ == "__main__" : main()