#!/usr/bin/python3
# parse CBAN xml

import os.path
import argparse
from xml.etree.ElementTree import parse


class Packages:
    def __init__(self):
        self.latest_version_packages = {}

    # incrementally add to latest_version_packages
    def get_latest_version_packages(self, file_path, excl_beast2=True):
        from kbpm.Package import Package
        if os.path.exists(file_path):
            tree = parse(file_path)
            root = tree.getroot()
            for package_xml in root.iter('package'):
                package = Package(package_xml)
                if excl_beast2 and package.name.lower() == "beast":
                    print("Exclude core package", package.name, package.version, "from list.")
                    continue
                # no source url, manually copy src.jar from BEAUti lib path
                if package.name.upper() == "DENIM" or package.name.upper() == "STACEY":
                    package.project_dir = package.name.upper()
                    # denim.src.jar, stacey.src.jar
                    package.url_source = package.name.lower() + ".src.jar"
                    print("Add", package.name, package.version, "from", package.url_source)
                # validate project_dir or url_source
                if not package.project_dir or not package.url_source:
                    print("Warning : remove package", package.name, package.version,
                          "from list ! project_dir =", package.project_dir, ", url_source =", package.url_source)
                    continue
                # add/replace by latest version package
                if package.name in self.latest_version_packages and not (
                        self.latest_version_packages[package.name] is None):
                    old_package = self.latest_version_packages[package.name]
                    if old_package.version < package.version:
                        self.latest_version_packages[package.name] = package
                else:
                    self.latest_version_packages[package.name] = package
        else:
            print("Cannot find package.xml :", file_path, " in current path:", os.getcwd())

    def print_packages_info(self):
        for key, value in self.latest_version_packages.items():
            self.latest_version_packages[key].print_info()
        print("\nLoad total ", len(self.latest_version_packages), " unique packages.\n")

    # trig git command
    def update_projects(self):
        for key, value in self.latest_version_packages.items():
            self.latest_version_packages[key].update_src()

    # read all java
    def find_all_citations(self):
        print("\n****** Java @Citation ******\n")
        for key, value in self.latest_version_packages.items():
            self.latest_version_packages[key].find_all_java_files()

    def print_all_citations(self):
        print("\n****** Summary ******\n")
        total = 0
        for key, value in self.latest_version_packages.items():
            package = self.latest_version_packages[key]
            # not accurate, may have 2 citations in one @Citation
            for str_citations in package.unique_citations:
                print(str_citations)
            total += len(package.unique_citations)
        print("\nFind total ", total, " citations.\n")



if (__name__ == "__main__"):
    parser = argparse.ArgumentParser()
    parser.add_argument("wp", help="working path to contain all GitHub repositories (packages)")
    args = parser.parse_args()
    print("Change working path to :", args.wp)
    os.chdir(args.wp)

    packages = Packages()
    xml_path = os.path.join(args.wp, "CBAN/packages.xml")
    packages.get_latest_version_packages(xml_path)
    xml_path = os.path.join(args.wp, "CBAN/packages2.5.xml")
    packages.get_latest_version_packages(xml_path)

    packages.print_packages_info()

    # git pull/clone
    #packages.update_projects()

    packages.find_all_citations()
    packages.print_all_citations()

