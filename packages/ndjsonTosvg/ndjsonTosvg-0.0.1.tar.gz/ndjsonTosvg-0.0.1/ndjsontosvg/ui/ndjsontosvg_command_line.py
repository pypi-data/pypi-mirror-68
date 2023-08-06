# coding=utf-8

"""Command line ui for ndjsontosvg"""

import argparse
from ndjsontosvg import __version__
from ndjsontosvg.ndjsontosvg import ndjsontosvg

def main(args=None):
    """Entry point for ndjsonTosvg application"""

    parser = argparse.ArgumentParser(description='ndjsonTosvg')

    ## ADD POSITIONAL ARGUMENTS
    parser.add_argument('--filein', '-i',
                        required=True,
                        type=str,
                        help="the input file (ndjson format)")

    parser.add_argument("-n", "--numberofsamples",
                        required=True,
                        type=int,
                        help="The number of samples to write out.")

    # ADD OPTINAL ARGUMENTS
    parser.add_argument("-s", "--outsize",
                        default=256,
                        type=int,
                        help="The desired out put size (pixels)")

    parser.add_argument("-lc", "--linecolour",
                        default="black",
                        help="The line colour to use."
                        )

    parser.add_argument("-bc", "--backgroundcolour",
                        default="white",
                        help="The background colour to use."
                        )

    parser.add_argument("-o", "--outdir",
                        default="./",
                        help="The output directory."
                        )

    parser.add_argument("-ci", "--checkifidentified",
                        action="store_true",
                        help="Only select entries that were recognized by" + \
                            " google AI",
                        )

    parser.add_argument("-rs", "--randomsort",
                        action="store_true",
                        help="Make a random selection, rather than the" + \
                            "first n lines",
                        )


    parser.add_argument("-is", "--inputsize",
                        default=256,
                        help="The input image size, 256 pixels for the " +\
                            "simplified quickdraw data set"
                        )

    version_string = __version__
    friendly_version_string = version_string if version_string else 'unknown'
    parser.add_argument(
        "--version",
        action='version',
        version='ndjsonTosvg version ' + friendly_version_string)

    args = parser.parse_args(args)

    ndjsontosvg(args.filein, args.numberofsamples, args.outsize,
                args.linecolour,
                args.backgroundcolour, args.outdir, args.checkifidentified,
                args.randomsort, args.inputsize)
