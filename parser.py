import sys, argparse

global parser
# Instantiate the parser
parser = argparse.ArgumentParser(
    description="TimeTableParser-UA is a python tool for scraping any timetable page on the University of Aveiro's academic portal (PACO) and exporting it to different formats.\n\nPlease refer to the GitHub repository for further help and instructions.")

# Presents the week's menu
parser.add_argument('-d', dest='dest',
                    help='specify destination filename')

#Specifies buildings to automatically upgrade
parser.add_argument('-u', type=str, nargs='*', dest='urls',
                    default=[],
                    help='specify all timetable urls separated by spaces' )

parser.add_argument('-f', dest='format',
                    help="specify desired output format (eg: sttx)")

def getUrls():
    print("Add all timetable urls seperated by ENTER. When done, press ENTER: ")

    urls = []
    while True:
        url = input("")
        if len(url) == 0:
            break
        urls.append(url)

    return urls

def main():
    # Get arguments
    args = parser.parse_args()

    version = 1.0
    print("TimeTableParser-UA version " + str(version) + " - Rodrigo Rosmaninho, MIECT, 2019\nRepository: https://github.com/RodrigoRosmaninho/TimeTableParser-ua\n")

    if args.dest == None:
        dest = input("Specify destination file: ")
        print("")
    else:
        dest = args.dest

    if len(args.urls) == 0:
        urls = getUrls()
    else:
        urls = args.urls

    if args.format == None:
        format = 1 # sttx
    elif args.format == "sttx":
        format = 1 # sttx
    else:
        print("Invalid format specified")
        sys.exit(1)

    import scraper
    print("Starting to collect timetable information from PACO...")

    classes = []
    for url in urls:
        try:
            classes.extend(scraper.getClasses(url))
        except Exception:
            print("\nError getting information from PACO url \"" + url + "\"\nPlease contact me at r.rosmaninho@ua.pt or open an issue on GitHub")
            sys.exit(2)

    print("Exporting...")

    if format == 1:
        import sttx
        sttx.export(dest, classes)
    else:
        print("Unexpected Error")
        sys.exit(3)

    print("Export Successful!")


if __name__ == "__main__":
    main()