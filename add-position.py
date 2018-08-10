
# 1) Read position data out
# 2) Write back into twee file (tricky)
# 3)  Write to file
from bs4 import BeautifulSoup
import collections

NameAndPosition = collections.namedtuple('NameAndPosition','name position')

# 1) Read twine->html output, add position to twee output in comments.
# 2) Read twee+position_comments, load position comments,  re-apply position to twee->html output.

# hardcode for now, later grab from command line
input_html_file = ".\\airport_builder\\Airport Builder.html"
input_twee_file = ".\\story.twee"
output_file= ".\\story.twee.post.process"

def getPositonFromTwineHtmlOutput(twineHtmlOutputFile):
    soup = None
    # not sure why utf8 doesn't work
    #with open(input_html_file,encoding='utf8') as fp:
    with open(twineHtmlOutputFile,errors='ignore') as fp:
        soup = BeautifulSoup(fp, 'html.parser')

    #<tw-passagedata pid="3" name="brian&#39;s buidlers"
    #   tags="" position="140,548.5999999046326" size="100,100">

    # gather all tw-passagedata
    passages =  soup.find_all('tw-passagedata')
    data = [ NameAndPosition(p['name'], p['position']) for p in passages]
    return data

def addPositionCommentsToTweeOutput(nameAndPositions,tweeOutputFile):
    # read file
    # walk line by line and match on nameAndPosition
    # insert line with position as comments





data = getPositonFromTwineHtmlOutput(input_html_file)
# addPositionCommentsToTweeOutput
# re-write twee file with comments
for d in data: print(d)

