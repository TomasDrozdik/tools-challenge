#!/usr/bin/env python

import sys
import subprocess
import re

def insertAssert(condition, path, line):
    print(f"Add `{condition}` to {path} on {line}")
    with open(path, "r") as file:
        content = file.readlines()
    with open(path, "w") as file:
        content.insert(int(line) - 1, f'assert({condition});\n')
        print(f"Writing content: {content}")
        file.writelines(content)


cbmcPath = "cbmc"
proc = subprocess.run([cbmcPath, *sys.argv[1:], "--bounds-check", "--show-properties"], stdout=subprocess.PIPE)


# Parse this:
#
# Property foo.array_bounds.1:
#   file src/library.h line 7 function foo
#   array 'x' lower bound in x[(signed long int)i]
#   4l * (signed long int)i >= 0l

hasPath = False
hasDescription = False
hasCondition = False
path = ""
pathRegex = re.compile('\s+file (?P<path>[^\s]+) line (?P<lineNum>\d+).*')
pathMatch = None
for line in proc.stdout.decode("utf-8").splitlines():  # parse conditions
    if hasPath:
        print(f"Path> {line}")
        pathMatch = pathRegex.match(line)
        assert pathMatch
        hasPath = False
        hasDescription = True

    elif hasDescription:
        print(f"Description> {line}")
        hasDescription = False
        hasCondition = True

    elif hasCondition:
        print(f"Condition> {line}")
        insertAssert(condition=line.strip(), path=pathMatch.group(
            'path'), line=pathMatch.group('lineNum'))
        hasCondition = False

    elif line.startswith("Property"):
        hasPath = True