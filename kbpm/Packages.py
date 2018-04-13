#!/usr/bin/python3
# parse CBAN xml

import os.path
import argparse
from xml.etree.ElementTree import parse


class Packages:
    def __init__(self):
        self.latest_version_packages = {}

    # incrementally add to latest_version_packages
    def get_latest_version_packages(self, file_path):
        from kbpm.Package import Package
        if os.path.exists(file_path):
            tree = parse(file_path)
            root = tree.getroot()
            for package_xml in root.iter('package'):
                package = Package(package_xml)
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
        print("\nLoad total ", len(self.latest_version_packages), " unique packages.")


if (__name__ == "__main__"):
    parser = argparse.ArgumentParser()
    parser.add_argument("wp", help="working path to contain all GitHub respositories (packages)")
    args = parser.parse_args()
    print("Change working path to :", args.wp)
    os.chdir(args.wp)

    packages = Packages()
    xml_path = os.path.join(args.wp, "CBAN/packages.xml")
    packages.get_latest_version_packages(xml_path)
    xml_path = os.path.join(args.wp, "CBAN/packages2.5.xml")
    packages.get_latest_version_packages(xml_path)

    packages.print_packages_info()
