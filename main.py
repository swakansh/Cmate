from cmate_class import *
from execution import *
import configparser
import argparse


"""
    TODO:
        1. Update the filenames to use predefined constants
        such as for input_1.txt, output_1.txt
        2. Update the problem code part to remove the bug.
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
    parser.add_argument("-d", "--default", help = "Sets the default site. cf for codeforces. cc for codechef. he for hackerearth. hr for hackerank. Once specified, no need to specify site with -s option again.")
    parser.add_argument("-s", "--site", help = "Sets the site for one time. cf for codeforces. cc for codechef. he for hackerearth. hr for hackerank.")
    parser.add_argument("-a", "-answer", help = "Provide a solution file to check correctness for.")
    parser.add_argument("problem", help = "Specify the problem code. Like 1111A, 1112B or XDCOMP etc")

    args = parser.parse_args()
    site_object = None
    site = None
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
            print("You need to provide the site to use. Use either -s or -d option.")
            exit(0)
    
    """
        Found the site.
    """
    if site == "cf":
        site_object = Codeforces(args.problem)
    elif site == "cc":
        pass
    elif site == "he":
        pass
    elif site == "hr":
        pass

    """
        We now also have the respective site object. We can download the test cases now.
    """
    site_object.get_test_cases(args.problem)

if __name__ == "__main__":
    main()
