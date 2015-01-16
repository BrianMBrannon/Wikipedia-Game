from bs4 import BeautifulSoup
import urllib2
import Searches

__author__ = 'bubba'

class WikipediaAgent:
    def __init__(self, function, problem):
        self.fuction = function
        self.problem = problem
        self.my_path = []
        self.index = 0 #used for getting the path later on

    def register(self):
        #print("Registering")
        self.my_path = Searches.breadthFirstSearch(self.problem)

    def printPath(self):
        for action in self.my_path:
            print action
        return

    # def getAction(self):
    #     i = self.index
    #     self.index += 1
    #     if i < len(self.my_path):
    #         return self.my_path[i]
    #     else:
    #         return "Finish"


class WikipediaProblem:
    def __init__(self, beginning_url, finishing_url):
        self.url_base = "http://en.wikipedia.org"
        self.beginning_url = beginning_url
        self.finishing_url = finishing_url

    def getStartState(self):
        return self.beginning_url

    def isGoalState(self, state):
        #print("{} = {}?: {}".format(state, self.finishing_url, state == self.finishing_url))
        return state == self.finishing_url

    def getSuccessors(self, state):
        # Reminders: soup is a BeautifulSoup object, states are (URL, 'TITLE', 1)
        successors = []
        #print("Trying to open: {}".format(state))
        print("Trying to read {}.".format(state))
        current_soup = BeautifulSoup(urllib2.urlopen(state).read())
        #print("Soup created for: {}".format(state))
        for paragraph in current_soup.find_all('p'):
            for link in paragraph.find_all('a'):
                # Each link is a Tag object; sometimes instead of a link there's a #cite_note-##
                # These are identified by having a string of "None" instead of the name following /wiki/
                # Sometimes a /w/ is also encountered; I do not know what that means. (Delete after &)? Causes a break
                if link.string is not None:
                    to_add = (self.url_base + link.get('href'), link.string, 1)
                    successors.append(to_add)
                    #print("Appended: {}".format(to_add))
        return successors