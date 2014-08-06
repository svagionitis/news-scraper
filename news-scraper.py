import site_configuration
import sys

def usage():
    """ Usage function
    """

    print("Usage: %s <json conf file>" % sys.argv[0])
    sys.exit(0)


def main():
    """ Main function
    """

    if len(sys.argv) != 2:
        usage()

    site_configuration.load(sys.argv[1])


if __name__ == '__main__':

  main()

