from attr import dataclass
from bs4 import BeautifulSoup
import collections


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


def twee_get_passage_name(line):
    name_candidate = line.split(":: ")
    is_passage_name = len(name_candidate) == 2
    if not is_passage_name:
        return None
    return name_candidate[1].strip()


def twee_get_display_attributes(line):
    return False


def twee_encode_display_attributes(attributes: PerPassageDisplayAttributes) -> str:
    return f"/*DA:{attributes}*/"


def get_display_attributes_from_twee_file(twee_position_file):
    # it's a passage if starts w/::
    # it's a passage if starts w/::

    ret = PassageDisplayAttributes()
    lines = open(twee_position_file).readlines()
    last_passage_name = ""
    for line in lines:
        name = twee_get_passage_name(line)
        if name:
            last_passage_name = name
        display_attributes = twee_get_display_attributes(line)
        attribs = PerPassageDisplayAttributes(
            name=last_passage_name, position=display_attributes
        )
        ret.add(last_passage_name, attribs)


def get_display_attributes_from_twine_file(twineHtmlOutputFile):
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


def add_display_attributes_to_twee_file(
    displayAttributes: PassageDisplayAttributes, twee_file, tweeOutputFile
):
    lines = open(twee_file, encoding="utf-8").readlines()
    output = []
    for line in lines:
        # ERROR IF WE FIND
        if twee_get_display_attributes(line):
            raise FileExistsError(f"{twee_file} already contains position data")

        output.append(line)
        name = twee_get_passage_name(line)
        if not name:
            continue

        if not displayAttributes.contains(name):
            print(f"ERROR: {name} found in twee file but no position data")
            continue

        # write out the position.
        # TODO extract this to a place we can reverse it.
        position_output = twee_encode_display_attributes(displayAttributes.get(name))
        print(position_output)
        output.append(position_output)

    open(tweeOutputFile, "w", encoding="utf-8").writelines(output)


def add_display_attributes_to_twine_file(
    displayAttributes: PassageDisplayAttributes, twine_file, output_twine_file
):
    with open(twine_file, encoding="utf-8") as fp:
        soup = BeautifulSoup(fp, "html.parser")

    passages = soup.find_all("tw-passagedata")

    for p in passages:
        if p["position"]:
            # raise FileExistsError(f"{twine_file} already contains position data")
            print(f"{twine_file} already contains position data for {p['name']}")

        output_passage_name = p["name"]
        if displayAttributes.contains(output_passage_name):
            p["position"] = displayAttributes.get(output_passage_name).position
        else:
            print(
                f"ERROR: {output_passage_name} found in twine file but no position data"
            )

    with open(output_twine_file, "w", encoding="utf-8") as file:
        file.write(str(soup))


# hardcode for now, later grab from command line
twine_export_file = ".\\airport_builder\\Airport Builder.html"
twee_file_base = ".\\story"
twee_file = f"{twee_file_base}.twee"
twee_position_file = f"{twee_file_base}.position.twee"
twee_html_file = f"{twee_file_base}.exported.html"
twee_html_position_file = f"{twee_file_base}.exported.position.html"

data = get_display_attributes_from_twine_file(twine_export_file)
add_display_attributes_to_twine_file(data, twee_html_file, twee_html_position_file)
add_display_attributes_to_twee_file(data, twee_file, twee_position_file)
