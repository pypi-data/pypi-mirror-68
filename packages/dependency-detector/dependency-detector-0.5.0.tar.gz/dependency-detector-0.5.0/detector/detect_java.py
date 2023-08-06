from os import path
from typing import List
from xml.dom.minidom import Element, parse

from detector.dependency import Dependency


def detect_java(directory_path: str) -> List[Dependency]:
    result: List[Dependency] = []
    possibly_pom_xml = f"{directory_path}/pom.xml"
    if path.exists(possibly_pom_xml):
        dom = parse(possibly_pom_xml)
        properties_list = dom.getElementsByTagName("properties")
        if len(properties_list) > 0:
            for prop in properties_list[0].childNodes:
                if isinstance(prop, Element):
                    if prop.tagName == "java.version":
                        java_version = prop.firstChild.data
                        if java_version == "1.8":
                            result.append(Dependency.JAVA8)
                        elif java_version == "11":
                            result.append(Dependency.JAVA11)
        result.append(Dependency.MAVEN)
    return result
