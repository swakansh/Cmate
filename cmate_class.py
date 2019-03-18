'''
    This is a project that will provide the functionality to test code right in
    your terminal against the sample test cases that are provided in the question

    I solve lot of programming questions and what i have to do is to fetch the test case by 
    copying them and then pasting them. Lot of repetitive task which can be automated 
    using power of languages such as python.

    The basic idea of this project is to fetch the required problem page and parse it 
    to get the required test cases and their output and then test it against the output 
    generated by the code submitted for the problem.

    Enough talking let's start implementing!!

    Currently developing for Codeforces, Codechef, AtCoder
    
    Will extend for :
    Hackerrank
'''

#All the necessary imports

from bs4 import BeautifulSoup as bs 
import requests
import os
import re
import itertools
import shutil
from colorama import init, Fore, Style, Back

class SITE:
    """
        Base class to support reusability of modules that work on same functionality.
        Basically implementing abstraction
    """
    def __init__(self):
        pass
    
    def get_contest_url(self):
        pass

    def get_problem_url(self, problem_code):
        pass

    def get_page_data(self, page_url):
        '''
            Description:
                Given the page url this function is responsible 
                for fetching html page from appropriate it.
            I/O: 
                problem_url(string)
            O/P:
                html_page_data
        '''
        headers = {'User-Agent' : "Mozilla/5.0"}
        try:
            for tries in range(self.MAX_TRIES):
                page_data = requests.get(page_url, headers = headers)
                if page_data.status_code == 200:
                    print("Fetched Page to parse test cases")
                    return page_data
        except:
            print("Could not connect to the {} site. Try again later.".format(self.site))
            exit(0)

    def bulk_request(self):
        pass

    @staticmethod
    def clean_structure(dirc):
        if dirc:
            for cur_file in os.listdir(dirc):
                file_path = os.path.join(dirc, cur_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except:
                    print("Error: Issues occurred while deleting files. Please try again later.")
        return

#Class Codeforces
class CODEFORCES(SITE):
    '''
    Description:
        This class will contain all the functions
        and properties related to how things need to be done for Codeforces website
    '''
    folder = None
    url = 'https://www.codeforces.com'
    MAX_TRIES = 5
    site = 'Codeforces'
    def __init__(self, contest_code):
        #constructor
        '''
            Description:
                Initialize all the properties of Codeforces Class
        '''
        self.contest_code = contest_code
        #   Check whether necessary folder structure is in place or not
        #   So that the test files could be saved there
        self.cp_dir = (os.path.join(CODEFORCES.folder, self.contest_code))
        if(not os.path.exists(self.cp_dir)):
            os.makedirs(self.cp_dir)

    def get_contest_url(self):
        """
            Description:
                Return the apt contest url.
            I/P:
                None
            O/P:
                Contest url
        """
        if self.contest_code:
            return self.url + '/contest/' + self.contest_code
        else:
            print("Error: No contest code available. Please provide the contest code.")

    def get_problem_url(self, problem_code):
        '''
            Description:
                Given the problem code like 1111C which means problem C from contest 1111
                this function is responsible for constructing the appropriate problem url.
            I/O: 
                problem_code(string)
            O/P:
                url(string)
        '''
        if problem_code:
            return self.url + '/contest/' + self.contest_code + '/problem/' + problem_code
        else:
            print("Could not construct page url.")
            exit(0)
        return None

    def get_test_cases(self, problem_code):
        '''
            Description:
                Given the HTML page data of the problem that we want to work on 
                this function parses the data to get the test cases and create the
                input and output files and store them in a respective folder.
            I/O:
                problem_page_data
            O/P:
                test cases file
        '''
        test_case_folder = os.path.join(self.cp_dir, problem_code)
        if(not os.path.exists(test_case_folder)):
            os.makedirs(test_case_folder)
        else:
            print("Test cases for {} problem already present.".format(problem_code))
            return    
        page_url = self.get_problem_url(problem_code)
        page_data = self.get_page_data(page_url)
        soup = bs(page_data.text, features = 'html.parser')
        tests = soup.findAll("div", {"class" : "sample-tests"})
        if len(tests) > 0:
            #There are some inputs and output files to be considered    
            inputs = tests[0].findAll("div" , {"class" : "input"})
            outputs = tests[0].findAll("div" , {"class" : "output"})

            for case in range(len(inputs)):
                data = inputs[case].find('pre').text.strip()
                filename = ("input_%s" % (case + 1))
                with open(os.path.join(test_case_folder,filename), "w") as file_ptr:
                    file_ptr.write(data)

            for case in range(len(outputs)):
                data = outputs[case].find('pre').text.strip()
                filename = ("output_%s" % (case + 1))
                with open(os.path.join(test_case_folder,filename), "w") as file_ptr:
                    file_ptr.write(data)

        else:
            print("No test cases associated with this problem code.")
        print("Parsing of test cases done...")

    def bulk_request(self):
        try:
            contest_url = self.get_contest_url()
            data = self.get_page_data(contest_url)
            soup = bs(data.text, "html.parser")
            problem_rows = soup.find("table", class_= "problems").find_all("tr")
            problem_codes = []
            for each_row in problem_rows:
                a_tags = each_row.find_all('a')
                if len(a_tags) and a_tags[0]['href']:
                    problem_codes.append(a_tags[0]['href'].split('/')[-1])
            
            for each in problem_codes:
                print(Style.BRIGHT + ("*" * 30))
                print(Style.BRIGHT + "Getting test case for the problem : {} - {} ....".format(self.contest_code, each))
                self.get_test_cases(each)
                print(Style.BRIGHT + Fore.GREEN + "Done!")
                print(Style.BRIGHT + ("*" * 30))
            
            print(Style.BRIGHT + Fore.GREEN + "All problem's test cases fetched.")
        except:
            print("Error: Issues encountered while fetching test cases. Please try again later.")
            exit(0)

class CODECHEF(SITE):
    """
        Description:
            This class encapsulates all the properties of the Codechef class
            and how things need to be done for codechef website
    """
    folder = None
    site = "Codechef"
    MAX_TRIES = 5
    url = 'https://www.codechef.com/'
    def __init__(self, contest_code):
        """
            Description:
                Initialise properties related to the Codechef class
        """
        self.contest_code = (contest_code if contest_code else 'PRACTICE')
        #   Check whether necessary folder structure is in place or not
        #   So that the test files could be saved there
        self.cp_dir = (os.path.join(CODECHEF.folder, self.contest_code))
        if(not os.path.exists(self.cp_dir)):
            os.makedirs(self.cp_dir)

    def get_contest_url(self):
        if self.contest_code != 'PRACTICE':
            return self.url + "/" + self.contest_code
        else:
            print("Error: No contest code available. Please provide the contest code.")
            exit(0)

    def get_problem_url(self, problem_code):
        if problem_code:
            return (self.url + "api/contests/" + self.contest_code + '/problems/' + problem_code)
        else:
            print("Could not construct page url.")
            exit(0)
        return None
    
    
    def get_test_cases(self, problem_code):
        """
            Codechef site has data in a variety of format.
            This function parses test cases from most of the formats.
        """
        test_case_folder = os.path.join(self.cp_dir, problem_code)
        if(not os.path.exists(test_case_folder)):
            os.makedirs(test_case_folder)
        else:
            print("Test cases for {} problem already present.".format(problem_code))
            return
        try:
            page_url = self.get_problem_url(problem_code)
            response = self.get_page_data(page_url)
            page_data = response.json()
            page_data = page_data['body']
            data_list = page_data.split("```")
            page_data = "</pre>".join("<pre>".join(data_list[i:i + 2]) for i in range(0, len(data_list), 2))
            soup = bs(page_data, "html.parser")
            test_pre_list = soup.find_all('pre')
            test_cases = []
            for each_pre in test_pre_list:
                tt_tags = each_pre.find_all('tt')
                if len(tt_tags) == 2:
                    test_cases.append((tt_tags[0].text, tt_tags[1].text))
                code_tags = each_pre.find_all('code')
                if len(code_tags) == 2:
                    test_cases.append((code_tags[0].text, code_tags[1].text))
                    
            if len(test_cases) == 0:
                for each_pre in test_pre_list:
                    # print(each_pre)
                    b_tags = each_pre.find_all('b')
                    if len(b_tags) == 2:
                        test_cases.append((b_tags[0].nextSibling, b_tags[1].nextSibling))
                

            if len(test_cases) == 0:
                current = 0
                while(current < len(test_pre_list)):
                    text_one = str(test_pre_list[current].text)
                    constr_regex = "-?[0-9]+\ *((≤|<=|<)\ *[\w<>//|]+\ *)+\ *(≤|<|<=)\ *-?[0-9]+"
                    if (re.search(constr_regex, text_one)):
                        #We need to skip this pre as this is a constraint
                        current += 1
                    else:
                        if current + 1 >= len(test_pre_list):
                            break
                        text_two = str(test_pre_list[current + 1].text)
                        if(re.search("input", text_one, re.IGNORECASE)):
                            text_one = "\n".join(text_one.split("\n")[2:])
                        if(re.search("output", text_two, re.IGNORECASE)):
                            text_two = "\n".join(text_two.split("\n")[2:])
                        test_cases.append((text_one, text_two))
                        current += 2
            
            for pos in range(len(test_cases)):
                test_cases[pos] = (test_cases[pos][0].strip(), test_cases[pos][1].strip())
            
            
            if len(test_cases):    
                for case in range(len(test_cases)):
                    data = test_cases[case][0]
                    filename = ("input_%s" % (case + 1))
                    with open(os.path.join(test_case_folder,filename), "w") as file_ptr:
                        file_ptr.write(data)
                    data = test_cases[case][1]
                    filename = ("output_%s" % (case + 1))
                    with open(os.path.join(test_case_folder,filename), "w") as file_ptr:
                        file_ptr.write(data)
            else:
                print("No test cases available for this problem.")        

        except:
            print("Error: Incorrect data received.")
            exit(0)

        print("Parsing of test cases done...")

    def bulk_request(self):
        try:
            contest_url = self.get_contest_url()
            data = self.get_page_data(contest_url)
            soup = bs(data.text, "html.parser")
            problem_rows = soup.find("table", class_= "dataTable").find_all("div", class_="problemname")
            problem_codes = []
            for each_row in problem_rows:
                a_tag = each_row.find('a')
                if a_tag and a_tag['href']:
                    problem_codes.append(a_tag['href'].split('/')[-1])
            
            for each in problem_codes:
                print(Style.BRIGHT + ("*" * 30))
                print(Style.BRIGHT + "Getting test case for the problem : {} - {} ....".format(self.contest_code, each))
                self.get_test_cases(each)
                print(Style.BRIGHT + Fore.GREEN + "Done!")
                print(Style.BRIGHT + ("*" * 30))
            
            print(Style.BRIGHT + Fore.GREEN + "All problem's test cases fetched.")
        except:
            print("Error: Issues encountered while fetching test cases. Please try again later.")
            exit(0)

class ATCODER(SITE):
    """
        Class to support features and methods to support parsing through Atcoder website
    """
    folder = None
    site = "AtCoder"
    MAX_TRIES = 5
    url = 'https://atcoder.jp/contests/'
    def __init__(self, contest_code):
        """
            Description:
                Initialise properties related to the Atcoder class
        """
        self.contest_code = contest_code
        #   Check whether necessary folder structure is in place or not
        #   So that the test files could be saved there
        self.cp_dir = (os.path.join(ATCODER.folder, self.contest_code))
        if(not os.path.exists(self.cp_dir)):
            os.makedirs(self.cp_dir)

    def get_contest_url(self):
        if self.contest_code:
            return self.url + self.contest_code + "/tasks"
        else:
            print("Error: No contest code available. Please provide the contest code.")
            exit(0)

    def get_problem_url(self, problem_code):
        if problem_code:
            return (self.url + self.contest_code + '/tasks/' + problem_code)
        else:
            print("Error: No problem code available. Please provide the problem code.")
            exit(0)
        return None

    
    def get_test_cases(self, problem_code):
        test_case_folder = os.path.join(self.cp_dir, problem_code)
        if(not os.path.exists(test_case_folder)):
            os.makedirs(test_case_folder)
        else:
            print("Test cases for {} problem already present.".format(problem_code))
            return
        page_url = self.get_problem_url(problem_code)
        page_data = self.get_page_data(page_url)
        soup = bs(page_data.text, features = 'html.parser')
        tests = soup.find_all("pre")
        current = 0
        pre_size = len(tests)
        test_cases = []
        while(current < pre_size):
            cur_pre = tests[current].find_all('var')
            if(cur_pre):
                #ignore that pre which is input style
                current += 1
            else:
                #otherwise the current one and the next one acts as input and output
                test_cases.append((tests[current].text.strip(), tests[current + 1].text.strip()))
                current += 2
        
        if len(test_cases):
            #Creating input and output files for each test case and storing them in respective folder
            for case in range(len(test_cases)):
                data = test_cases[case][0]
                filename = ("input_%s" % (case + 1))
                with open(os.path.join(test_case_folder,filename), "w") as file_ptr:
                    file_ptr.write(data)
                data = test_cases[case][1]
                filename = ("output_%s" % (case + 1))
                with open(os.path.join(test_case_folder,filename), "w") as file_ptr:
                    file_ptr.write(data)
        else:
            print("No test cases associated with this problem code.")
        print("Parsing of test cases done...")

    def bulk_request(self):
        try:
            contest_url = self.get_contest_url()
            data = self.get_page_data(contest_url)
            soup = bs(data.text, "html.parser")
            problem_rows = soup.find("table").find_all("tr")
            problem_codes = []
            for each_row in problem_rows:
                a_tags = each_row.find_all('a')
                if len(a_tags) and a_tags[0]['href']:
                    problem_codes.append(a_tags[0]['href'].split('/')[-1])
            
            for each in problem_codes:
                print(Style.BRIGHT + ("*" * 30))
                print(Style.BRIGHT + "Getting test case for the problem : {} - {} ....".format(self.contest_code, each))
                self.get_test_cases(each)
                print(Style.BRIGHT + Fore.GREEN + "Done!")
                print(Style.BRIGHT + ("*" * 30))
            
            print(Style.BRIGHT + Fore.GREEN + "All problem's test cases fetched.")
        except:
            print("Error: Issues encountered while fetching test cases. Please try again later.")
            exit(0) 



class HACKERRANK(SITE):
    """
        Class to provide properties and methods for Hackerrank class
    """
    site = "Hackerrank"
    url = "https://www.hackerrank.com"
    MAX_TRIES = 5
    folder = None
    def __init__(self, contest_code):
        """
            Description:
                Initialise properties related to the Hackerrank class
        """
        self.contest_code = contest_code
        #   Check whether necessary folder structure is in place or not
        #   So that the test files could be saved there
        self.contest_code = (contest_code if contest_code else 'CHALLENGES')
        self.cp_dir = os.path.join(HACKERRANK.folder, self.contest_code)
        if(not os.path.exists(self.cp_dir)):
            os.makedirs(self.cp_dir)

    def get_problem_url(self, problem_code):
        if problem_code:
            if self.contest_code == "CHALLENGES":
                return self.url + '/challenges/' + problem_code 
            else:
                return self.url + "/contests/" + self.contest_code + "/challenges/" + problem_code
        else:
            print("Error: No problem code available. Please provide the problem code.")
            exit(0)
        return None


    def get_contest_url(self):
        if self.contest_code != 'CHALLENGES':
            return self.url + "/contests/" + self.contest_code + "/challenges"
        else:
            print("Error: No contest code available. Please provide the contest code.")
            exit(0)

    def get_test_cases(self, problem_code):
        test_case_folder = os.path.join(self.cp_dir, problem_code)
        if(not os.path.exists(test_case_folder)):
            os.makedirs(test_case_folder)
        else:
            print("Test cases for {} problem already present.".format(problem_code))
            return
        try: 
            page_url = self.get_problem_url(problem_code)
            page_data = self.get_page_data(page_url)
            soup = bs(page_data.text, features = "html.parser")
            input_divs = soup.find_all("div", class_="challenge_sample_input")
            output_divs = soup.find_all("div", class_="challenge_sample_output")
            test_cases = []
            for cur in range(len(input_divs)):
                test_cases.append((input_divs[cur].find("pre").text.strip(), output_divs[cur].find("pre").text.strip()))
            if len(test_cases):
                for case in range(len(test_cases)):
                    data = test_cases[case][0]
                    filename = ("input_%s" % (case + 1))
                    with open(os.path.join(test_case_folder,filename), "w") as file_ptr:
                        file_ptr.write(data)
                    data = test_cases[case][1]
                    filename = ("output_%s" % (case + 1))
                    with open(os.path.join(test_case_folder,filename), "w") as file_ptr:
                        file_ptr.write(data)
            else:
                print("No test cases available for this problem.") 

        except:
            print("Error: Incorrect data received.")
            exit(0)

        print("Parsing of test cases done...")
        

    def bulk_request(self):
        try:
            print("Bulk request for all problems of the contest.")
            contest_url = self.get_contest_url()
            print(contest_url)
            data = self.get_page_data(contest_url)
            soup = bs(data.text, "html.parser")
            print(soup)
            problems = soup.find("div", class_="challenges-list")
            print(problems)
            problems_array = problems.find_all("h4", class_="challengecard-title")
            print("FU")
            print(problems)
            problem_codes = []
            for each in problems_array:
                a_tag = each_row.find('a')
                if a_tag and a_tags['href']:
                    problem_codes.append(a_tag['href'].split('/')[-1])
            
            for each in problem_codes:
                print(Style.BRIGHT + ("*" * 30))
                print(Style.BRIGHT + "Getting test case for the problem : {} - {} ....".format(self.contest_code, each))
                self.get_test_cases(each)
                print(Style.BRIGHT + Fore.GREEN + "Done!")
                print(Style.BRIGHT + ("*" * 30))
            
            print(Style.BRIGHT + Fore.GREEN + "All problem's test cases fetched.")
        except:
            print("Error: Issues encountered while fetching test cases. Please try again later.")
            exit(0)