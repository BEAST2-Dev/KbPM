#!/usr/bin/python3
# 1 java file many have 1 or many citations


class Citations:
    def __init__(self, package="", version="", java_file=""):
        self.package = package
        self.version = version
        self.java_file = java_file
        self.citations = ""

    def __bool__(self):
        return len(self.java_file) > 0

    def set_citations(self, lines):
        self.citations = lines

    def add_citation_lines(self, line):
        self.citations = self.citations + line

    def get_citations(self):
        return self.citations

    def __str__(self):
        return '\n'.join([self.java_file, self.get_citations()])








