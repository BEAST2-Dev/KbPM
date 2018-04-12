#!/usr/bin/python3
# parse CBAN


import xml.etree.ElementTree as ET
import os.path
import argparse

class Package():
    def __init__(self, package_xml):
        self.attrs = package_xml.attrib
        self.children = package_xml.findall('depends')
        self.setPackageInfo(self.attrs)

    # set package info
    def setPackageInfo(self, attributes):
        self.name = attributes["name"]
        self.version = attributes["version"]
        self.url = attributes["url"]
        if "projectURL" in attributes:
            self.projectURL = attributes["projectURL"]
        self.description = attributes["description"]

    def printInfo(self):
        print("*****package*****")
        print("name:", self.name)
        print("version:", self.version)
        print("url:", self.url)
        print("projectURL:", self.projectURL)
        print("description:", self.description)


if (__name__ == "__main__"):
    parser = argparse.ArgumentParser()
    parser.add_argument("wp", help="working path to contain all GitHub respositories (packages)")
    args = parser.parse_args()
    print("Change working path to :", args.wp)
    os.chdir(args.wp)

    lastest_packages = {}
    file_path = os.path.join(args.wp, "CBAN/packages.xml")
    if os.path.exists(file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()
        for package_xml in root.iter('package'):
            package = Package(package_xml)
            if package.name in lastest_packages and not (lastest_packages[package.name] is None):
                old_package = lastest_packages[package.name]
                if old_package.version < package.version:
                    lastest_packages[package.name] = package
            else:
                lastest_packages[package.name] = package

        for key, value in lastest_packages.items():
            lastest_packages[key].printInfo()
        print("\nLoad total ", len(lastest_packages), " unique packages.")
    else:
        print("Cannot find package.xml :", file_path, " in current path:", os.getcwd())
