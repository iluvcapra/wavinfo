from . import WavInfoReader

import datetime
from optparse import OptionParser
import sys
import os
import json
from enum import Enum
import importlib.metadata


class MyJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Enum):
            return o._name_
        else:
            return super().default(o)


class MissingDataError(RuntimeError):
    pass


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

    (options, args) = parser.parse_args(sys.argv)

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

                json.dump(ret_dict, cls=MyJSONEncoder, fp=sys.stdout, indent=2)
        except MissingDataError as e:
            print("MissingDataError: Missing metadata (%s) in file %s" %
                  (e, arg), file=sys.stderr)
            continue
        except Exception as e:
            raise e


if __name__ == "__main__":
    main()
