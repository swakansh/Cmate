from cmate_class import *
# from execution import *
import configparser
import argparse
import os


"""
    TODO:
        1. Update the filenames to use predefined constants
        such as for input_1.txt, output_1.txt
"""
parser = argparse.ArgumentParser()
config = configparser.ConfigParser()


home_dir = os.path.expanduser("~")
config_folder = os.path.join(home_dir, ".cmate")
config_file_name = "config.ini"
config_file_name = os.path.join(config_folder, config_file_name)

def main():
    """
        Set the optional and postional argument required
    """
    parser.add_argument("-d", 
                        "--default", 
                        help = "Sets the default site. cf for codeforces. cc for codechef. he for hackerearth. hr for hackerank. Once specified, no need to specify site with -s option again.")
    parser.add_argument("-s", 
                        "--site", 
                        help = "Sets the site for one time. cf for Codeforces. cc for Codechef. hr for Hackerank. ac for Atcoder. Use as -s site")
    parser.add_argument("-a", 
                        "--answer", 
                        help = "Provide a solution file to check correctness for. Use as -a answer")
    parser.add_argument("-b",
                        "--bulk",
                        action = "store_true",
                        help = "Fetch all the test cases for the given contest. Use as -b")
    parser.add_argument("-c", 
                        "--contest", 
                        help = "Use this option to provide the contest code. Like 1111, JAN19A. Use as -c contest")
    parser.add_argument("-p",
                        "--problem", 
                        help = "Specify the problem code. Like A, B or XDCOMP etc. Use as -p problem")
    parser.add_argument("-z",
                        "--zero",
                        action = "store_true",
                        help = "Use this option to free up the space occupied by the test input and output files. Use as -z")
    
    args = parser.parse_args()

    #Initializing the class variables
    home_dir = os.path.expanduser('~')
    CODEFORCES.folder = (os.path.join(home_dir, ".cmate", CODEFORCES.site))
    CODECHEF.folder = (os.path.join(home_dir, ".cmate", CODECHEF.site))
    ATCODER.folder = (os.path.join(home_dir, ".cmate", ATCODER.site))
    site_object = None
    site = None



    if args.zero:
        # we need to clean the directory structure
        print("Deleting all the previous input and output files.")
        CODEFORCES.clean_structure(CODEFORCES.folder)
        CODECHEF.clean_structure(CODECHEF.folder)
        ATCODER.clean_structure(ATCODER.folder)
        print("Done...")
    
    
    if args.site:
        """
            If -s option has been specified than it will be given higher priority.
        """
        site = args.site
    elif args.default:
        """
            If -s option has not been specified but default is then pick up the default site and set the new default.
        """
        config['DEFAULT'] = {
            'site' : args.default
        }
        with open(config_file_name, "w") as config_file:
            config.write(config_file)
        site = args.default
    else:
        """
            If no option has been specified, check whether a default state is already available.
            If not available force user to specify the site.
        """
        try:
            config.read(config_file_name)
            site = config['DEFAULT']['site']
        except:
            pass
    """
        Found the site.
    """
    if site == "cf":
        if not args.contest:
            print("You need to provide the contest code for the problem. Like 1111, 1113 the one that is present in the link.")
            exit(0)
        site_object = CODEFORCES(args.contest)
    elif site == "cc":
        site_object = CODECHEF(args.contest)
    elif site == "ac":
        if not args.contest:
            print("You need to provide the contest code for the problem. Like arc101, ar102 the one that is present in the link.")
            exit(0)
        site_object = ATCODER(args.contest)
    elif site == "hr":
        pass
    
    """
        If site and problem code is available, we can download the test cases now.
    """
    if site_object and args.problem:
        site_object.get_test_cases(args.problem)
    elif site_object and args.bulk:
        site_object.bulk_request()
    elif site_object:
        print("Error: Pass the problem code to proceed further. Use -p option.")
        exit(0)

    

if __name__ == "__main__":
    init(autoreset=True)
    main()
