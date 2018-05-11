#!/usr/bin/python3
# parse CBAN xml

from xml.etree.ElementTree import Element
import os.path
import glob
from kbpm.Citations import Citations


def git_cmd(cmd=None):
    if cmd is None:
        cmd = ['git', 'pull']
    import subprocess
    PIPE = subprocess.PIPE
    process = subprocess.Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdoutput, stderroutput = process.communicate()

    if b'fatal' in stdoutput:
        msg = "Failed :"
    else:
        msg = "Succeed :"
    print(msg, ' '.join([str(a) for a in cmd]))


# grep lines from 1 java to get 1 or many citations
def get_citations(name, version, java_file):
    citations = Citations()  # false
    with open(java_file, 'rt') as in_file:
        for line in in_file:
            # print(line)
            # if "@Description" in line:
            if " class " in line or " interface " in line or "enum" in line:
                break
            if -1 < line.find("@Citation") < 6:
                citations = Citations(name, version, java_file)
            # print(java_file)
            # @Citation may have multiple lines
            if citations:
                citations.add_citation_lines(line)
            # print(line)
    return citations


class Package:
    def __init__(self, package_xml: Element):
        self.name = ""
        self.version = ""
        self.url = ""
        self.projectURL = ""
        self.description = ""
        self.url_source = ""  # add, because projectURL is not always src
        self.project_dir = ""
        self.attrs = package_xml.attrib
        self.children = package_xml.findall('depends')
        self.set_package_info(self.attrs)
        # suppose to be unique citations only, no java file name
        self.unique_citations = []

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
            print("Warning : package", self.name, self.version, "source not in github.com or bitbucket.org !", items[2])
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

    # update project
    def update_src(self):
        if len(self.url_source) < 2 or len(self.project_dir) < 2:
            print("Skip package", self.name, self.version, ", which have no source !")
        else:
            cwd = os.getcwd()
            if os.path.exists(self.project_dir):
                proj_cwd = os.path.join(cwd, self.project_dir)
                os.chdir(proj_cwd)
                git_cmd(['git', 'pull'])
                os.chdir(cwd)
            else:
                print("Warning :", self.project_dir, "does not exist under", cwd)
                git_cmd(['git', 'clone', self.url_source])

    ### citations ###
    # recursively search *.java,
    # is_print_cite=True to print java file name + citations
    def find_all_java_files(self, is_print_cite=True):
        cwd = os.getcwd()
        if os.path.exists(self.project_dir):
            proj_cwd = os.path.join(cwd, self.project_dir)
            os.chdir(proj_cwd)

            java_files = glob.glob('**/*.java', recursive=True)
            if len(java_files) < 1:
                print("Error: cannot find java file in", self.project_dir, "!")
            else:
                print("Find", len(java_files), "java files in", self.project_dir, ":\n")
                for java_file in java_files:
                    citations = get_citations(self.name, self.version, java_file)
                    if citations:
                        if is_print_cite:
                            print(citations)
                        str_cite_only = citations.get_citations()
                        if "Citation(\"\")" in str_cite_only:
                            print("Warning: skip empty @Citation in", java_file, ":", str_cite_only)
                            continue
                        if str_cite_only not in self.unique_citations:
                            self.unique_citations.append(str_cite_only)

            os.chdir(cwd)
        else:
            raise OSError(self.project_dir, "does not exist under", cwd)
