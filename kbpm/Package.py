#!/usr/bin/python3
# parse CBAN xml

from xml.etree.ElementTree import Element
import os.path


class Package:
    def __init__(self, package_xml: Element):
        self.name = ""
        self.version = ""
        self.url = ""
        self.projectURL = ""
        self.description = ""
        self.url_source = "" # add, because projectURL is not always src
        self.project_dir = ""
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
        self.get_url_source(self.url)

    def get_url_source(self, url):
        items = url.split('/')
        if len(items) < 2:
            print("Error : package", self.name, self.version, "does not have url !", url)
        elif "github.com" not in items[2] and "bitbucket.org" not in items[2]:
            # [2] is 'github.com' or 'bitbucket.org'
            print("Error : package", self.name, self.version, "source not in github.com or bitbucket.org !", items[2])
        else:
            # [4] is project name in github or bitbucket
            self.project_dir = items[4]
            self.url_source = '/'.join([str(a) for a in items[:5]])

    def print_info(self):
        print("*****package*****")
        print("name:", self.name)
        print("version:", self.version)
        print("url:", self.url)
        print("projectURL:", self.projectURL)
        print("description:", self.description)
        print("url_source:", self.url_source)
        print("project_dir:", self.project_dir)

    # update all projects
    def update_src(self):
        if len(self.url_source) < 2 or len(self.project_dir) < 2:
            print("Skip package", self.name, self.version, ", which have no source !")
        else:
            cwd = os.getcwd()
            if os.path.exists(self.project_dir):
                proj_cwd = os.path.join(cwd, self.project_dir)
                os.chdir(proj_cwd)
                self.git_cmd(['git', 'pull'])
                os.chdir(cwd)
            else:
                print("Warning :", self.project_dir, "does not exist under", cwd)
                self.git_cmd(['git', 'clone', self.url_source])

    @staticmethod
    def git_cmd(cmd=None):
        if cmd is None:
            cmd = ['git', 'pull']
        import subprocess
        PIPE = subprocess.PIPE
        process = subprocess.Popen(cmd, stdout=PIPE, stderr=PIPE)
        stdoutput, stderroutput = process.communicate()

        if b'fatal' in stdoutput:
            msg = "Error : "
        else:
            msg = "Succeed "
        print(msg, ' '.join([str(a) for a in cmd]))


