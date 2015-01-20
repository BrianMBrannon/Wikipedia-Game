from bs4 import BeautifulSoup
import urllib2
import Searches
import nltk
import nltk.corpus
from nltk.corpus import PlaintextCorpusReader
__author__ = 'bubba'

class WikipediaAgent:
    def __init__(self, function, problem):
        self.fuction = function
        self.problem = problem
        self.my_path = []
        self.index = 0 #used for getting the path later on

    def register(self):
        #print("Registering")
        self.my_path = [self.problem.get_start_state()] + Searches.breadthFirstSearch(self.problem)

    def printPath(self):
        path = ""
        for action in self.my_path:
            path += action + ' -> '
        print(path + "FINISH")
        return

    # def getAction(self):
    #     i = self.index
    #     self.index += 1
    #     if i < len(self.my_path):
    #         return self.my_path[i]
    #     else:
    #         return "Finish"


class WikipediaProblem:
    """
        Defines a problem for the Wikipedia Game
        A state is defined as a tuple of three elements, the first being a url
        of the web page as a string, the second is the title of that web page, and
        the third is the cost of the state

        Each cost for now is one; it will be updated to something more meaningful later
    """
    def __init__(self, beginning_url, finishing_url):
        self.url_base = "http://en.wikipedia.org"
        self.beginning_url = beginning_url
        self.finishing_url = finishing_url

    def get_start_state(self):
        return self.beginning_url, "BEGIN", 1

    def is_goal_state(self, state):
        #print("{} = {}?: {}".format(state, self.finishing_url, state == self.finishing_url))
        return state.lower() == self.finishing_url.lower()

    def get_successors(self, state):
        """
        Reminder: soup is a BeautifulSoup object, states are (URL, 'TITLE', 1)
        :param state: A given state passed by a search algorithm in the form of a tuple: ('URL', 'TITLE', COST)
        :return: a list of successors to the state with a cost of 1 (to be updated) each
        """
        successors = []
        print("Trying to read {}.".format(state[1]))
        current_soup = BeautifulSoup(urllib2.urlopen(state[0]).read())
        for paragraph in current_soup.find_all('p'):
            for link in paragraph.find_all('a'):
                # Each link is a Tag object; sometimes instead of a link there's a #cite_note-##
                # These are identified by having a string of "None" instead of the name following /wiki/
                # Sometimes a /w/ is also encountered; I do not know what that means. Causes a break
                if link.string is not None and '&' not in link.get('href'):
                    to_add = (self.url_base + link.get('href'), link.string, 1)
                    successors.append(to_add)
                    #print("Appended: {}".format(to_add))
        return successors

    def createCorpus(self, url, file_name):
        """
        This method takes a
        :param url: url of the web page as a string to start making a corpus from
        :param file_name: name of a file as a string where the corpus will be written to
        :return: return a ContextIndex of a corpus
        """
        page = BeautifulSoup(urllib2.urlopen(url).read())
        self.__add_from_page__(file_name, page, True)

        #Only expand the first <p> section; doing all <p> sections will take way too long
        #Using only this first <p> section useful information is retrieved anyway
        for link in page.p.find_all('a'):
            #Filter out links not linking to useful content
            if link.string is not None and '&' not in link.get('href') and ':' not in link.get('href'):
                url = "http://en.wikipedia.org" + link.get('href')
                new_page = BeautifulSoup(urllib2.urlopen(url).read())
                self.__add_from_page__(file_name, new_page, False)

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

    def get_similar_words(self, corpus_context_index, compare_to):
        """
        :param corpus_context_index: ContextIndex for corpus
        :param compare_to: word used to find similar words
        :return: list containing similar words to compare_to
        """
        #compare_to is cast into lower case to avoid getting empty or unhelpful lists of similar words
        return corpus_context_index.similar_words(compare_to.lower())

    def __add_from_page__(self, file, page, rewrite, only_first = False):
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