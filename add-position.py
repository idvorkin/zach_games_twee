from bs4 import BeautifulSoup
import collections

# TODO: Support the other attributes like size and tags.
NameAndPosition = collections.namedtuple("NameAndPosition", "name position")

# Two approaches:

# 1) Read twine->html output, add position to twee output in comments.
# 2) Read twee+position_comments, load position comments,  re-apply position to twee->html output.

# hardcode for now, later grab from command line
twine_export_file = ".\\airport_builder\\Airport Builder.html"
twee_file_base = ".\\story"
twee_file = f"{twee_file_base}.twee"
twee_position_file = f"{twee_file_base}.position.twee"
twee_html_file = f"{twee_file_base}.html"
twee_html_position_file = f"{twee_file_base}.position.html"


def getPositionFromTweeFile(tweeFile):
    # it's a passage if starts w/::
    # it's a passage if starts w/::
    pass


def getPositonFromTwineHtmlOutput(twineHtmlOutputFile):
    soup = None
    with open(twineHtmlOutputFile, encoding="utf-8") as fp:
        soup = BeautifulSoup(fp, "html.parser")

    # <tw-passagedata pid="3" name="brian&#39;s buidlers"
    #   tags="" position="140,548.5999999046326" size="100,100">

    # gather all tw-passagedata
    passages = soup.find_all("tw-passagedata")
    data = [NameAndPosition(name=p["name"], position=p["position"]) for p in passages]
    return data


# addPositionCommentsToTweeOutput(data, twee_position_file)
def addPositionCommentsToTweeOutput(nameAndPositions, tweeOutputFile):
    lines = open(twee_file).readlines()
    output = []
    nameToPos = dict(nameAndPositions)
    for line in lines:
        output.append(line)
        # echo existing line to output
        nameCandidate = line.split(":: ")
        isPassageName = len(nameCandidate) == 2
        if not isPassageName:
            continue
        name = nameCandidate[1].strip()
        if name in nameToPos:
            # write out the position.
            positionOutput = (
                f"+ /* POSITION: {nameToPos[name]} */\n"
            )  # TBD what's teh story with the \n's
            print(positionOutput)
            output.append(positionOutput)
        else:
            print(f"ERROR: {name} found in twee file but no position data")

    # open(output_file,"w",lines)
    open(tweeOutputFile, "w").writelines(output)

    return


# Interesting idea - skip the middle input file with twee, do input to output.
def addPositionDataToTweeHtmlOutput(nameAndPositions, generatedHtmlFile, outputFile):
    nameToPos = dict(nameAndPositions)
    with open(generatedHtmlFile, encoding="utf-8") as fp:
        soup = BeautifulSoup(fp, "html.parser")

    passages = soup.find_all("tw-passagedata")
    for p in passages:
        outputPassageName = p["name"]
        if outputPassageName in nameToPos:
            p["position"] = nameToPos[outputPassageName]
        else:
            print(f"ERROR: {outputPassageName} found in twee file but no position data")

    with open(outputFile, "w", encoding="utf-8") as file:
        file.write(str(soup))


data = getPositonFromTwineHtmlOutput(twine_export_file)
addPositionDataToTweeHtmlOutput(data, twee_html_file, twee_html_position_file)
