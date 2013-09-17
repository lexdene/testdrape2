import sys
import os

path = sys.argv[1]

print '['
for roots, dirs, files in os.walk(path):
    for file_name in files:
        name, ext = os.path.splitext(file_name)
        print '    "%s",' % name

print '  ]'
