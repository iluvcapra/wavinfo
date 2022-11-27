from optparse import OptionParser, OptionGroup
import datetime
from . import WavInfoReader
from . import __version__
import sys
import json
from enum import Enum

class MyJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Enum):
            return o._name_
        else:
            return super().default(o)

class MissingDataError(RuntimeError):
    pass

def main():
    parser = OptionParser()

    parser.usage = 'wavinfo (--adm | --ixml) [FILES]'

    # parser.add_option('-f', dest='output_format', help='Set the output format',
    #                   default='json',
    #                   metavar='FORMAT')

    parser.add_option('--adm', dest='adm', help='Output ADM XML', 
        default=False, action='store_true')

    parser.add_option('--ixml', dest='ixml', help='Output iXML',
        default=False, action='store_true')

    (options, args) = parser.parse_args(sys.argv)
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
                    sys.stdout.write(this_file.ixml.xml_bytes())
                else:
                    raise MissingDataError("ixml")
            else:
                ret_dict = {
                    'filename': arg, 
                    'run_date': datetime.datetime.now().isoformat() , 
                    'application': "wavinfo " + __version__, 
                    'scopes': {}
                    }
                for scope, name, value in this_file.walk():
                    if scope not in ret_dict['scopes'].keys():
                        ret_dict['scopes'][scope] = {}

                    ret_dict['scopes'][scope][name] = value

                json.dump(ret_dict, cls=MyJSONEncoder, fp=sys.stdout, indent=2)
        except MissingDataError as e:
            print("MissingDataError: Missing metadata (%s) in file %s" % (e, arg), file=sys.stderr)
            continue
        except Exception as e:
            raise e


if __name__ == "__main__":
    main()
