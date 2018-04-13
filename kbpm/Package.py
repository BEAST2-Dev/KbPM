#!/usr/bin/python3
# parse CBAN xml

from xml.etree.ElementTree import Element


class Package:
    def __init__(self, package_xml: Element):
        self.attrs = package_xml.attrib
        self.children = package_xml.findall('depends')
        self.set_package_info(self.attrs)

    # set package info
    def set_package_info(self, attributes):
        self.name = attributes["name"]
        self.version = attributes["version"]
        self.url = attributes["url"]
        if "projectURL" in attributes:
            self.projectURL = attributes["projectURL"]
            if self.name == "BEAST":
                self.projectURL = "https://github.com/CompEvol/beast2"
        self.description = attributes["description"]

    def print_info(self):
        print("*****package*****")
        print("name:", self.name)
        print("version:", self.version)
        print("url:", self.url)
        print("projectURL:", self.projectURL)
        print("description:", self.description)
