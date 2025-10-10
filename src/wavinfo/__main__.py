from . import WavInfoReader

import datetime
from optparse import OptionParser
import sys
import os
import json
from enum import Enum
import importlib.metadata
from base64 import b64encode
from cmd import Cmd
from shlex import split
from typing import List, Dict, Union


class MyJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Enum):
            return o._name_
        elif isinstance(o, bytes):
            return 'base64:' + b64encode(o).decode('ascii')
        else:
            return super().default(o)


class MissingDataError(RuntimeError):
    pass


class MetaBrowser(Cmd):
    prompt = "(wavinfo) "

    metadata: Union[List, Dict]
    path: List[str] = []

    @property
    def cwd(self):
        root: List | Dict = self.metadata
        for key in self.path:
            if isinstance(root, list):
                root = root[int(key)]
            else:
                root = root[key]

        return root

    @staticmethod
    def print_value(collection, key):
        val = collection[key]
        if isinstance(val, int):
            print(f" - {key}: {val}")
        elif isinstance(val, str):
            print(f" - {key}: \"{val}\"")
        elif isinstance(val, dict):
            print(f" - {key}: Dict ({len(val)} keys)")
        elif isinstance(val, list):
            print(f" - {key}: List ({len(val)} keys)")
        elif isinstance(val, bytes):
            print(f" - {key}: ({len(val)} bytes)")
        elif val is None:
            print(f" - {key}: (NO VALUE)")
        else:
            print(f" - {key}: Unknown")

    def do_ls(self, _):
        'List items at the current node: LS'
        root = self.cwd

        if isinstance(root, list):
            print("List:")
            for i in range(len(root)):
                self.print_value(root, i)

        elif isinstance(root, dict):
            print("Dictionary:")
            for key in root:
                self.print_value(root, key)

        else:
            print("Cannot print node, is not a list or dictionary.")

    def do_cd(self, args):
        'Switch to a different node: CD node-name | ".."'
        argv = split(args)
        if argv[0] == "..":
            self.path = self.path[0:-1]
        else:
            if isinstance(self.cwd, list):
                if int(argv[0]) < len(self.cwd):
                    self.path = self.path + [argv[0]]
                else:
                    print(f"Index {argv[0]} does not exist")
            elif isinstance(self.cwd, dict):
                if argv[0] in self.cwd.keys():
                    self.path = self.path + [argv[0]]
                else:
                    print(f"Key \"{argv[0]}\" does not exist")

        if len(self.path) > 0:
            self.prompt = "(" + "/".join(self.path) + ") "
        else:
            self.prompt = "(wavinfo) "

    def do_bye(self, _):
        'Exit the interactive browser: BYE'
        return True


def main():
    version = importlib.metadata.version('wavinfo')
    manpath = os.path.dirname(__file__) + "/man"
    parser = OptionParser()

    parser.usage = 'wavinfo (--adm | --ixml) <FILE> +'

    # parser.add_option('--install-manpages',
    #                   help="Install manual pages for wavinfo",
    #                   default=False,
    #                   action='store_true')

    parser.add_option('--man',
                      help="Read the manual and exit.",
                      default=False,
                      action='store_true')

    parser.add_option('--adm', dest='adm',
                      help='Output ADM XML',
                      default=False,
                      action='store_true')

    parser.add_option('--ixml', dest='ixml',
                      help='Output iXML',
                      default=False,
                      action='store_true')

    parser.add_option('-i',
                      help='Read metadata with an interactive prompt',
                      default=False,
                      action='store_true')

    (options, args) = parser.parse_args(sys.argv)

    interactive_dict = []

    # if options.install_manpages:
    #     print("Installing manpages...")
    #     print(f"Docfiles at {__file__}")
    #     return

    if options.man:
        import shlex
        print("Which man page?")
        print("1) wavinfo usage")
        print("7) General info on Wave file metadata")
        m = input("?> ")

        args = ["man", "-M", manpath, "1", "wavinfo"]
        if m.startswith("7"):
            args[3] = "7"

        os.system(shlex.join(args))
        return

    for arg in args[1:]:
        try:
            this_file = WavInfoReader(path=arg)
            if options.adm:
                if this_file.adm:
                    sys.stdout.write(this_file.adm.xml_str())
                else:
                    raise MissingDataError("adm")
            elif options.ixml:
                if this_file.ixml:
                    sys.stdout.write(this_file.ixml.xml_str())
                else:
                    raise MissingDataError("ixml")
            else:
                ret_dict = {
                    'filename': arg,
                    'run_date': datetime.datetime.now().isoformat(),
                    'application': f"wavinfo {version}",
                    'scopes': {}
                }
                for scope, name, value in this_file.walk():
                    if scope not in ret_dict['scopes'].keys():
                        ret_dict['scopes'][scope] = {}

                    ret_dict['scopes'][scope][name] = value

                if options.i:
                    interactive_dict.append(ret_dict)
                else:
                    json.dump(ret_dict, cls=MyJSONEncoder, fp=sys.stdout,
                              indent=2)

        except MissingDataError as e:
            print("MissingDataError: Missing metadata (%s) in file %s" %
                  (e, arg), file=sys.stderr)
            continue
        except Exception as e:
            raise e

        if len(interactive_dict) > 0:
            cli = MetaBrowser()
            cli.metadata = interactive_dict
            cli.cmdloop()


if __name__ == "__main__":
    main()
