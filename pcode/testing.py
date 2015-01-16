from bs4 import BeautifulSoup
import urllib2
import SearchingTools
import Searches

def main():
    #page = "http://en.wikipedia.org/wiki/Achilles"
    #urllib2.urlopen(page)
    run()
    return

def run():
    start_url = "http://en.wikipedia.org/wiki/Achilles"
    finish_url = "http://en.wikipedia.org/wiki/Ancient_Greece"
    my_problem = SearchingTools.WikipediaProblem(start_url, finish_url)
    agent = SearchingTools.WikipediaAgent(Searches.breadthFirstSearch, my_problem)
    agent.register()
    agent.printPath()

def problemTesting():
    print("Begin testing")
    my_problem = SearchingTools.WikipediaProblem("http://en.wikipedia.org/wiki/Achilles", "http://en.wikipedia.org/wiki/Greek_mythology")
    start_state = my_problem.getStartState()
    print("Start state: {}".format(start_state))
    print("Start state is goal state?: {}".format(my_problem.isGoalState(start_state)))
    successors = my_problem.getSuccessors(start_state)
    print("Successors: ")
    for successor in successors:
        if my_problem.isGoalState(successor):
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