"""

"""

from optparse import OptionParser, OptionGroup
import sys


def main():
    parser = OptionParser()

    parser.usage = "wavfind [--scene=SCENE] [--take=TAKE] [--desc=DESC] <PATH> +"

    primaries = OptionGroup(parser, title="Search Predicates",
        description="Argument values can be globs, and are logically-AND'ed.")

    primaries.add_option("--scene", 
        help='Search for this scene', 
        metavar='SCENE')
    
    primaries.add_option("--take",
        help='Search for this take',
        metavar='TAKE')

    primaries.add_option("--desc",
        help='Search descriptions',
        metavar='DESC')
        

    (options, args) = parser.parse_args(sys.argv)


if __name__ == "__main__":
    main()
