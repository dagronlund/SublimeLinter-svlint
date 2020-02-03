#
# linter.py
# Linter for SublimeLinter4, a code checking framework for Sublime Text 3
#
# Modified from VHDL to Verilog to SystemVerilog by Leon Woestenberg
# Original:
# Written by Bruno JJE
# Copyright (c) 2015 Bruno JJE
#
# License: MIT
#

"""This module exports the SVLinter plugin class."""

from SublimeLinter.lint import Linter
import re
import logging
import os
import os.path
import subprocess


def get_imports_code(code):
    """ Searches a string for import statements """
    imports = []
    for line in iter(code.splitlines()):
        line = line.strip()
        if line.startswith("//!import"):
            import_path = line.split("//!import", 1)[1].strip()
            imports.append(import_path)
        else:
            return imports
    return imports


def get_imports_file(file_path):
    """ Searches a file for import statements """
    imports = []
    with open(file_path, 'r') as f:
        line = f.readline()
        while line:
            line = line.strip()
            if line.startswith("//!import"):
                import_path = line.split("//!import", 1)[1].strip()
                imports.append(import_path)
                line = f.readline()
            else:
                return imports


def get_import_path(import_path, project_dir):
    """ Converts a local import to a full path """
    full_import_path = project_dir
    for piece in import_path.split('/'):
        full_import_path = os.path.join(full_import_path, piece)
    return full_import_path + ".sv"


def build_import_tree(import_path, project_dir):
    """ Recursively iterates through files to create a tree of imports """
    tree = {}
    full_import_path = get_import_path(import_path, project_dir)
    for file_import in get_imports_file(full_import_path):
        tree[file_import] = build_import_tree(file_import, project_dir)
    return tree


def flatten_import_tree(import_tree):
    """ Produces a unique value list from an import tree """
    import_list = []
    for import_node in import_tree:
        for prior_import in flatten_import_tree(import_tree[import_node]):
            if prior_import not in import_list:
                import_list.append(prior_import)
        if import_node not in import_list:
            import_list.append(import_node)
    return import_list


class SVLinter(Linter):

    """Provides an interface to xvlog (from Xilinx Vivado Simulator)."""

    name = "svlint"
    defaults = {
        "lint_mode": "load_save",
        "disable": "false",
        "debug": "true",
        "selector": "source.systemverilog"
    }
    cmd = 'xvlog -sv --nolog'
    #version_args = '--version --nolog'
    #version_re = r'Vivado Simulator (?P<version>\d+\.\d+)'
    #version_requirement = '>= 2014.4'
    #tempfile_suffix = 'sv'
    tempfile_suffix = 'linter'
    # Here is a sample xvhdl error output:
    # ----8<------------
    # ERROR: [VRFC 10-91] td_logic is not declared [/home/BrunoJJE/src/filtre8.vhd:35]
    # ----8<------------

    regex = (
        r"^(?P<error>(ERROR|INFO): )(?P<message>\[.*\].*)"
        r"\[(?P<path>.*):(?P<line>[0-9]+)\]"
    )


    def lint(self, code, view_has_changed):
        """ Modifies linter to use SystemVerilog import comments """

        # Find project base directory
        project_dir = self.get_working_dir()
        found = False
        while not found and project_dir != os.path.dirname(project_dir):
            # print("Searching: " + project_dir)
            if "project.yaml" in os.listdir(project_dir):
                # print("Found in: " + project_dir)
                found = True
                break
            project_dir = os.path.dirname(project_dir)

        # Create tree of imports
        import_tree = {}
        for file_import in get_imports_code(code):
            import_tree[file_import] = build_import_tree(file_import, project_dir)
        import_list = flatten_import_tree(import_tree)
        import_paths = [get_import_path(ip, project_dir) for ip in import_list]

        processes = []
        for ip in import_paths:
            # print("Manual Dependency: " + ip)
            proc = subprocess.Popen("xvlog -sv --nolog " + ip, cwd=self.get_working_dir(), shell=True)

        for p in processes:
            p.communicate()

        # Example tree structure
        # {
        #     "std/std_pkg": {}
        #     "std/std_register":
        #     {
        #         "std/std_pkg": {}
        #     }
        # }

        return super().lint(code, view_has_changed)

    def split_match(self, match):
        """
        Extract and return values from match.

        We override this method to prefix the error message with the
        linter name.

        """

        match, line, col, error, warning, message, near = super().split_match(match)

        # See if we can find a "near" keyword from the message to add a squirly line

        # "...near XXX"
        near_match = re.search(r'.*near (?P<near>\w+).*', message)
        if not near_match:
            # "XXX is not declared"
            near_match = re.search(r'(?P<near>\w+) is not declared.*', message)
        if not near_match:
            # "procedural assignment to a non-register XXX is not permitted..."
            near_match = re.search(r'non-register (?P<near>\w+) is not permitted.*', message)
        if not near_match:
            # "use of undefined macro XXX" for example `if instead of `ifdef
            near_match = re.search(r'use of undefined macro (?P<near>\w+).*', message)
        if not near_match:
            # for example `endif without `if
            near_match = re.search(r'(?P<near>\w+) without `if.*', message)
        if not near_match:
            # "procedural assignment to a non-register XXX is not permitted..."
            near_match = re.search(r'undeclared symbol (?P<near>\w+).*', message)
        # @TODO Extend this Linter here with near matches, as follows:
        # if not near_match:
            #near_match = re.search(r'prefix message (?P<near>\w+) postfix message.*', message)

        if near_match:
            near = near_match.group('near')

        if match:
            message = '[xsvlog] ' + message

        return match, line, col, error, warning, message, near
