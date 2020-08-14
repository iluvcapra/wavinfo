from optparse import OptionParser, OptionGroup
import datetime
from . import WavInfoReader
import sys
import json


def main():
    parser = OptionParser()

    parser.usage = 'wavinfo [FILE.wav]*'

    # parser.add_option('-f', dest='output_format', help='Set the output format',
    #                   default='json',
    #                   metavar='FORMAT')

    (options, args) = parser.parse_args(sys.argv)
    for arg in args[1:]:
        try:
            this_file = WavInfoReader(path=arg)
            ret_dict = {'file_argument': arg, 'run_date': datetime.datetime.now().isoformat() , 'scopes': {}}
            for scope, name, value in this_file.walk():
                if scope not in ret_dict['scopes'].keys():
                    ret_dict['scopes'][scope] = {}

                ret_dict['scopes'][scope][name] = value

            json.dump(ret_dict, fp=sys.stdout, indent=2)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
