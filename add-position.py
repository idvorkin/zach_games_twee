from attr import dataclass
from bs4 import BeautifulSoup
import collections

# TODO: Support the other attributes like size and tags.
NameAndPosition = collections.namedtuple("NameAndPosition", "name position")


@dataclass
class PerPassageDisplayAttributes:
    name: str
    position: str  # TODO: strengthen the types.
    tags: str = ""
    size: str = ""


class PassageDisplayAttributes:
    # nameToPassages: Mapping[str,PerPassageDisplayAttributes] = {}
    def __init__(self):
        self.nameToPassages = {}

    def get(self, name: str) -> PerPassageDisplayAttributes:
        return self.nameToPassages[name]

    # TODO learn how to do 'in' syntax.
    def contains(self, name: str) -> bool:
        return name in self.nameToPassages

    def add(self, name: str, displayAttributes: PerPassageDisplayAttributes):
        self.nameToPassages[name] = displayAttributes


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
    with open(twineHtmlOutputFile, encoding="utf-8") as fp:
        soup = BeautifulSoup(fp, "html.parser")

    # <tw-passagedata pid="3" name="brian&#39;s buidlers"
    #     tags="" position="140,548.5999999046326" size="100,100">
    # gather all tw-passagedata
    ret = PassageDisplayAttributes()
    passages = soup.find_all("tw-passagedata")
    for p in passages:
        attribs = PerPassageDisplayAttributes(name=p["name"], position=p["position"])
        ret.add(p["name"], attribs)

    return ret


def addPositionCommentsToTweeOutput(
    displayAttributes: PassageDisplayAttributes, twee_file, tweeOutputFile
):
    lines = open(twee_file).readlines()
    output = []
    for line in lines:
        output.append(line)
        # echo existing line to output
        name_candidate = line.split(":: ")
        is_passage_name = len(name_candidate) == 2
        if not is_passage_name:
            continue
        name = name_candidate[1].strip()
        if displayAttributes.contains(name):
            # write out the position.
            positionOutput = (
                f"+ /* POSITION: {displayAttributes.get(name)} */\n"
            )  # TBD what's teh story with the \n's
            print(positionOutput)
            output.append(positionOutput)
        else:
            print(f"ERROR: {name} found in twee file but no position data")

    # open(output_file,"w",lines)
    open(tweeOutputFile, "w").writelines(output)

    return


# Interesting idea - skip the middle input file with twee, do input to output.
def addPositionDataToTweeHtmlOutput(
    displayAttributes: PassageDisplayAttributes, generatedHtmlFile, outputFile
):
    with open(generatedHtmlFile, encoding="utf-8") as fp:
        soup = BeautifulSoup(fp, "html.parser")

    passages = soup.find_all("tw-passagedata")
    for p in passages:
        output_passage_name = p["name"]
        if displayAttributes.contains(output_passage_name):
            p["position"] = displayAttributes.get(output_passage_name)
        else:
            print(
                f"ERROR: {output_passage_name} found in twee file but no position data"
            )

    with open(outputFile, "w", encoding="utf-8") as file:
        file.write(str(soup))


data = getPositonFromTwineHtmlOutput(twine_export_file)
addPositionCommentsToTweeOutput(data, twee_file, twee_position_file)
addPositionDataToTweeHtmlOutput(data, twee_html_file, twee_html_position_file)
