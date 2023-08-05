from optparse import OptionParser
import sys

def parse_options():
    """
    Handle command-line options with optparse.OptionParser.

    Return list of arguments, largely for use in `parse_arguments`.
    """

    # Initialize
    parser = OptionParser(usage="lurl [options]")

    parser.add_option(
        '-p','--prod',
        dest='curl_prod',
        default=None,
        help="put your cURL for production"
    )

    parser.add_option(
       '-s','--stag',
        dest='curl_stag',
        default=None,
        help="put your cURL for staging"
    )

    parser.add_option(
        '--stag-har-folder',
        dest='stag_har_folder',
        default=None,
        help="put your har folder path for staging"
    )

    parser.add_option(
        '--prod-har-folder',
        dest='prod_har_folder',
        default=None,
        help="put your har folder path for production"
    )

    parser.add_option(
        '-i','--interactive',
        dest='is_interactive',
        default=False,
        action='store_true',
        help="interactively create files"
    )

    # parser.add_option(
    #    '--skip-response',
    #     dest='skip_response',
    #     action='store_true',
    #     default=False,
    #     help="skip set response"
    # )

    # Finalize
    # Return three-tuple of parser + the output from parse_args (opt obj, args)
    opts, args = parser.parse_args()
    return parser, opts, args