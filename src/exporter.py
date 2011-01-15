# -*- coding: utf-8 -*-
#
# Copyright (C) 2011 by Aevum Softwares LTDA ME
#
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import optparse
import os

__version__ = 0.1
SEQUENCE_SUFFIX = "sequence"

def remove_lines_started_with(word, lines):
    toRemove = []
    for line in lines:
        if line.startswith(word):  
            toRemove.append(line)
    for line in toRemove:
        lines.remove(line)

def remove_lines_with(word, lines):
    toRemove = []
    for line in lines:
        if word in line:  
            toRemove.append(line)
    for line in toRemove:
        lines.remove(line)

def remove_word(word, lines, numberOfNextWords = 0):
    substitute = "@@@"
    for i in range(len(lines)):
        if not numberOfNextWords:
            lines[i] = lines[i].replace(word, "")
        else:
            line = lines[i]
            line = line.replace(word, substitute)
            if substitute in line:
                split = line.split()
                nextWords = []
                for j in range(len(split)):
                    if split[j] == substitute:
                        for k in range(numberOfNextWords):
                            nextWords.append(split[k+j+1])
                replaceString = substitute
                for k in range(numberOfNextWords):
                    replaceString = "{0} {1}".format(replaceString, nextWords[k])
                lines[i] = line.replace(replaceString, "")

def put_semicolons(lines):
    numberOfOpenningParenthesis = 0
    numberOfClosingParenthesis = 0
    for i in range(len(lines)):
        line = lines[i]
        split = lines[i].split()
        if "CREATE" in split and "TABLE" in split:
            if split.index("CREATE") == split.index("TABLE") - 1:
                numberOfOpenningParenthesis = 0
                numberOfClosingParenthesis = 0
                
        while "(" in line:
            line = line.replace("(", "", 1)
            numberOfOpenningParenthesis = numberOfOpenningParenthesis + 1
            
        while ")" in line:
            line = line.replace(")", "", 1)
            numberOfClosingParenthesis = numberOfClosingParenthesis + 1
        
        if numberOfOpenningParenthesis == numberOfClosingParenthesis:
            if numberOfOpenningParenthesis != 0:
                lines[i] =  lines[i].replace("\n", "") + ";\n"
                numberOfOpenningParenthesis = 0
                numberOfClosingParenthesis = 0


def create_sequences(lines):
    sequences = []
    lastTable = None
    for i in range(len(lines)):
        line = lines[i]
        split = line.split()
        if "CREATE" in split and "TABLE" in split:
            if split.index("CREATE") == split.index("TABLE") - 1:
                lastTable =  split[split.index("CREATE")+2]
        elif "AUTO_INCREMENT" in line:
            sequences.append({"table" : lastTable, "column" :split[0]})
    
    for sequence in sequences:
        lines.append("{0} {1}_{2}_{3};\n".format(
                                "DROP SEQUENCE IF EXISTS",
                                sequence["table"], 
                                sequence["column"],
                                SEQUENCE_SUFFIX ))
        lines.append("{0} {1}_{2}_{3};\n".format(
                                "CREATE SEQUENCE ",
                                sequence["table"], 
                                sequence["column"],
                                SEQUENCE_SUFFIX ))

def replace_word(word, replace, lines):
    for i in range(len(lines)):
        lines[i] = lines[i].replace(word, replace)

def add_cascade_to_drops(lines):
    for i in range(len(lines)):
        line = lines[i]
        if line.startswith("DROP"):
            lines[i] = line.replace(";", "CASCADE;")

def convert(input, output):
    lines = input.readlines()
    remove_lines_with("ASC)", lines)
    remove_lines_started_with("SET", lines)
    remove_lines_started_with("COLLATE", lines)
    remove_lines_started_with("ENGINE", lines)
    remove_lines_started_with("COMMENT", lines)
    remove_lines_started_with("USE", lines)
    remove_word("`", lines)
    remove_word("'", lines)
    remove_word("UNSIGNED", lines)
    remove_word("IF NOT EXISTS", lines)
    remove_word("DEFAULT CHARACTER SET =", lines, 1)
    remove_word("DEFAULT CHARACTER SET", lines, 1)
    remove_word("CHARACTER SET", lines, 1)
    remove_word("COLLATE", lines, 1)
    replace_word("DATETIME", "TIMESTAMP", lines)
    put_semicolons(lines)
    add_cascade_to_drops(lines)
    create_sequences(lines)
    remove_word("AUTO_INCREMENT", lines)
    
    
    output.writelines(lines)
    
def main(args):
    """Check arguments from the command line and executed the required action"""
    parser = optparse.OptionParser(
        usage="Usage: %prog [options] <input_file> <output_file>",
        version="%prog {0}".format(__version__))
    #parser.add_option("-o", "--output",
    #                  action="store", dest="output", 
    #                  help="Generates the output")
    (options, args) = parser.parse_args()
    if len(args) == 2:
        input_path = args[0]
        if not os.path.exists(input_path):
            print "First argument should be a valid sql file"
            return
        output_path = args[1]
        input = file(input_path, "r")
        output = file(output_path, "w")
        convert(input, output)
        
    else:
        print "Ivalid parameters. You should run YYY <input> <output>"
        return
    
if __name__ == "__main__":
    main(sys.argv)