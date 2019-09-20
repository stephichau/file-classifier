import argparse

def create_arguments_main(parser: argparse.ArgumentParser) -> argparse.Namespace:
    parser.add_argument('-s', "--setup", action="store_true", dest="setup", help="Setup mode")
    parser.add_argument('-m' ,"--make", action="store_true", dest="make", help="Create ocr")
    parser.add_argument('-c' ,"--classify", action="store_true", dest="classify", help="Classify ocr")
    parser.add_argument('-f' ,"--file", action="store", dest="filename",
        help="Info either for creating ocr's or classifying")
    return parser

def check_option(arguments: argparse.Namespace) -> int: # rename function
    option = 0

    option = 1 if check_setup(arguments) else option

    option = 2 if option == 0 and check_ocr_make(arguments) else option

    option = 3 if option == 0 and check_ocr_classify(arguments) else option

    return option
    
def check_setup(arguments: argparse.Namespace) -> bool:
    return arguments and arguments.setup

def check_ocr_make(arguments: argparse.Namespace) -> bool:
    return arguments and arguments.make and arguments.filename and not arguments.classify

def check_ocr_classify(arguments: argparse.Namespace) -> bool:
    return arguments and arguments.classify and arguments.filename and not arguments.make


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    p = create_arguments_main(parser)
    print(check_option(p))
