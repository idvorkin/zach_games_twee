
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
twee_file_base=".\\story"
input_twee_file = f'{twee_file_base}.twee'
output_file= f'{twee_file_base}.position.twee'

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
    lines = open(input_twee_file).readlines()
    output = []
    nameToPos = dict(nameAndPositions)
    for line in lines:
        output.append(line)
        # echo existing line to output
        nameCandidate = line.split(":: ")
        isName = len(nameCandidate) == 2
        if not isName:
            continue
        name = nameCandidate[1].strip()
        if name in nameToPos:
            # write out the position.
            positionOutput = f'+ /* POSITION: {nameToPos[name]} */\n' # TBD what's teh story with the \n's
            print (positionOutput)
            output.append(positionOutput)
        else:
            print (f"ERROR: {name} found in twee file but no position data")

    # open(output_file,"w",lines)
    open(output_file,"w").writelines(output)
    
    return

data = getPositonFromTwineHtmlOutput(input_html_file)
addPositionCommentsToTweeOutput(data,output_file)
