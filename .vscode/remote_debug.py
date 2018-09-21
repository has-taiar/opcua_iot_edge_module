import argparse
import pdb
import os
import ptvsd
import runpy
import sys
import time
"""
This module provides an easy interface between the VS Code remote
debugger and vendor-provided code.

Usage
-----
The script is used as follows:

    $ python remote_debug.py --filename target_script.py 
      --args 'optional args separated by spaces'

Notes
-----
    For more details on ptvsd utilites, see:

    https://github.com/Microsoft/vscode-python/blob/master/pythonFiles/
    PythonTools/ptvsd/visualstudio_py_util.py

"""


def args():
    parser = argparse.ArgumentParser(description="""
        Debug a file with optional arguments.
    """)
    parser.add_argument('--filename', '-f',
                        required=True,
                        metavar='path',
                        help='Python file to do remote debugging on.')
    parser.add_argument('--arguments', '-a',
                        required=False,
                        metavar='path',
                        help='Arguments to pass into the Python file.')
    args = vars(parser.parse_args())

    return args


def main(filename, arguments):

    print("Waiting to attach to VS Code")

    # Attach
    address = ('0.0.0.0', 5000)
    ptvsd.enable_attach('my_secret', address)
    ptvsd.wait_for_attach()
    time.sleep(2)

    print("Attached to VS Code")

    # Execute python script
    if arguments is not None:
        new_arguments = [filename]
        new_arguments.extend(arguments.split(' '))
        sys.argv = new_arguments

    # TODO: Test arguments with argument-receiving script.

    ptvsd.visualstudio_py_util.exec_file(filename, globals())
    print("Remote debugging session ended")


if __name__ == "__main__":
    main(**args())
