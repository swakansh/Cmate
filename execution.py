from colorama import init, Fore, Style, Back
import subprocess
import argparse
import os

class TEST:
    """
        Description:
            A class to represent the status of each test done.
            status - True/False (Whether the test passed or not)
            input - the input for the test
            output - the output for the test
            expected_output - output expected from the test
            message - an informational message
    """
    def __init__(self, status, inp, e_out, out, msg):
        self.status = status
        self.input = inp
        self.output = out
        self.expected_output = e_out
        self.message = msg

    def __str__(self):
        output = ""
        output += (Style.BRIGHT + "Test :")
        output += ("\nInput: \n" + self.input)
        output += ("\nExpected Output: \n" + self.expected_output)
        output += ("\nOutput from program: \n" + self.output)
        output += ("\n" + ((Fore.GREEN + "TEST PASSED") if self.status else (Fore.RED + "TEST FAILED")))
        output += ("\n" + Style.BRIGHT + Fore.CYAN + self.message)
        return output

class LANGUAGE_EXEC:
    """
        The base class to support solution file execution.
    """
    def __init__(self):
        """
            Base class constructor which defines some basic property
            that will also be available in derived class.
        """
        self.tle = 10
        self.command = None

    def get_output_file_name(self, sol_file):
        """
            Description:
                Get the name of the output file to be generated.
            I/O:
                Name of the solution file.
            O/P:
                Name of the output file.
        """
        try:
            return sol_file.split(".")[0]
        except:
            print("Incorrect file name given")
            exit(0)

    def get_test_file_list(self, tests_location):
        """
            Description:
                The job of this function is to prepare a list of name of all the input files in tests location folder.
            I/O:
                Path to the folder which contains test files
            O/P:
                A list containing the content as described above
        """
        files = os.listdir(tests_location)
        input_files = []
        for current in files:
            if current.startswith("input"):
                input_files.append(current)
        return input_files

    def test_file(self, tests_location, sol_file):
        """
            Description :
                Given the location where the test files are saved this function will
                compile and execute the provided file and produce the output generated
                by executable file. It will then compare the output with the expected output
                to prepare the list. 
                
                This function will be overridden in derived classes depending on the language
                of the solution file. 
            
            I/O :
                tests_location : Path to where the test files are located
                sol_file : name of the solution file to test on

        """
        pass

    def match_output(self, input_files, output, tests_location):
        """
            Description:
                Given the name input_files which contains the input test file names and
                name of the executable file, the job of this function is to match the output
                produced from the program with the expected output.
            I/P:
                input_list : list of names of the input files
                output : name of the executable on which matching is to be done
                test_location : path to input and output test file
            O/P:
                test_list - status of each test done on the sol_file
        """
        tests_list = []
        for current in input_files:
            file_id = current.split("_")[1]
            inp_file_name = "input_%s" % file_id
            inp_file_content = None
            out_file_content = None
            with open(os.path.join(tests_location, inp_file_name), "r") as inp_file:
                inp_file_content = inp_file.read()
            out_file_name = "output_%s" % file_id
            with open(os.path.join(tests_location, out_file_name), "r") as out_file:
                out_file_content = out_file.read()
            temp_file = open("temp", "wb")
            inp_file = open(os.path.join(tests_location, inp_file_name), "r")
            try:
                completed = subprocess.run(
                    [output],
                    check = True,
                    stdin = inp_file,
                    stdout = temp_file,
                    timeout = self.tle,
                    stderr = subprocess.PIPE
                )
            except subprocess.CalledProcessError as err:
                current_test = TEST(False, inp_file_content, out_file_content, "", completed.stderr.decode('utf-8'))
                tests_list.append(current_test)
            except subprocess.TimeoutExpired as err:
                current_test = TEST(False, inp_file_content, out_file_content, "", "TLE")
                tests_list.append(current_test)
            else:
                temp_file.close()
                temp_file_content = None
                with open("temp", "r") as temp_file:
                    temp_file_content = temp_file.read()
                current_test = None
                temp_file_content = temp_file_content.strip()
                #
                # TODO: Below comparison, works for now!
                # Normal string comparisons for two files
                # Make sure this works
                if out_file_content == temp_file_content:
                    current_test = TEST(True, inp_file_content, out_file_content, temp_file_content, "Ok!")
                else:
                    current_test = TEST(False, inp_file_content, out_file_content, temp_file_content, "Not Ok!")
                tests_list.append(current_test)
            inp_file.close()
            temp_file.close()
        return tests_list

    def print_status(self, tests_list):
        """
            Description:
                This function is responsible for showing nice output of each test
                done on the test file.

            I/O :
                A list containing status of the each test done on the file.

        Elaborate more on this later
        """
        success_tests = 0
        total_tests = 0
        for test in tests_list:
            if(test.status):
                success_tests += 1
            total_tests += 1
            print("*" * 30)
            print(test)
            print("*" * 30)
        print(Style.BRIGHT + Fore.GREEN + "PASSED: " + str(success_tests) + "/" + str(total_tests))
        print(Style.BRIGHT + Fore.GREEN + "Success percentage: " + str(success_tests / total_tests * 100))


class LANG_CPLUS(LANGUAGE_EXEC):
    """
        Class to support execution of c++ files
    """
    def __init__(self):
        self.command = "g++"
        self.args = []
        self.tle = 10

    def compile_file(self, sol_file):
        """
            Description:
                Compile the file to check for errors, if there are errors present let the user know.
                Don't continue further.

                If this stage doesn't produce any error, move ahead to stage 2.
            I/P:
                Name of the input file to be compiled
            O/P:
                Name of the executable generated after compiling
        """
        output = self.get_output_file_name(sol_file)
        try:
            completed = subprocess.run(
                [self.command, sol_file, "-o", output],
                timeout = self.tle,
                check = True,
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE
            )
        except subprocess.CalledProcessError as err:
            print(err.stderr.decode('utf-8'))
            exit(0)
        except subprocess.TimeoutExpired as err:
            print("The program took too much time to compile.")
            exit(0)
        return output
        

    def test_file(self, tests_location, sol_file):
        """
            Description:
                The job of this function is to do testing of the solution file on the test cases present in tests_location folder.
                Whole work is divided into three parts:
                1. Compilation
                2. Fetching the test files name
                3. Testing
            I/P:
                sol_file - name of the solution file
                tests_location - location where the test files are stored
            O/P:
                test_list - status of each test done on the sol_file
        """
        """
            Compile file
        """
        output = self.compile_file(sol_file)
        output = "./" + output
        """
            Get a listing of all the test files on which the input program is to be tested.
        """
        input_files = self.get_test_file_list(tests_location)
        """
            For each input files on which the program is to be tested, test the program and make
            note of the output for comparison purposes.
        """
        tests_list = self.match_output(input_files, output, tests_location)
        self.print_status(tests_list)


class LANG_C(LANGUAGE_EXEC):
    """
        Class to support execution of c files
    """
    def __init__(self):
        self.command = "gcc"
        self.args = []
        self.tle = 10

    def compile_file(self, sol_file):
        output = self.get_output_file_name(sol_file)
        try:
            completed = subprocess.run(
                [self.command, sol_file, "-o", output],
                timeout = self.tle,
                check = True,
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE
            )
        except subprocess.CalledProcessError as err:
            print(err.stderr.decode('utf-8'))
            exit(0)
        except subprocess.TimeoutExpired as err:
            print("The program took too much time to compile.")
            exit(0)
        return output
        

    def test_file(self, tests_location, sol_file):
        output = self.compile_file(sol_file)
        output = "./" + output
        input_files = self.get_test_file_list(tests_location)
        tests_list = self.match_output(input_files, output, tests_location)
        self.print_status(tests_list)

class LANG_PYTHON(LANGUAGE_EXEC):
    """
        Class to support interpretation of python source files
    """
    def __init__(self):
        self.command = "python"
        self.args = []
        self.tle = 10
    
    def test_file(self, tests_location, sol_file):
        input_files = self.get_test_file_list(tests_location)
        tests_list = self.interpret_file(input_files, tests_location, sol_file)
        self.print_status(tests_list)


    def interpret_file(self, input_files, tests_location, sol_file):
        """
            Description:
                This is for python, there is no compilation phase in python so the solution will
                directly be interpreted and its output will be matched the expected output.

                Given the name input_files which contains the input test file names and
                name of the solution file, the job of this function is to match the output
                produced from the program with the expected output.
            I/P:
                input_list : list of names of the input files
                output : name of the file on which matching is to be done
                test_location : path to input and output test file
            O/P:
                test_list - status of each test done on the sol_file
        """
        tests_list = []
        for current in input_files:
            file_id = current.split("_")[1]
            inp_file_name = "input_%s" % file_id
            inp_file_content = None
            out_file_content = None
            with open(os.path.join(tests_location, inp_file_name), "r") as inp_file:
                inp_file_content = inp_file.read()
            out_file_name = "output_%s" % file_id
            with open(os.path.join(tests_location, out_file_name), "r") as out_file:
                out_file_content = out_file.read()
            temp_file = open("temp", "wb")
            inp_file = open(os.path.join(tests_location, inp_file_name), "r")
            try:
                completed = subprocess.run(
                    [self.command, sol_file],
                    check = True,
                    stdin = inp_file,
                    stdout = temp_file,
                    timeout = self.tle,
                    stderr = subprocess.PIPE
                )
            except subprocess.CalledProcessError as err:
                current_test = TEST(False, inp_file_content, out_file_content, "", completed.stderr.decode('utf-8'))
                tests_list.append(current_test)
            except subprocess.TimeoutExpired as err:
                current_test = TEST(False, inp_file_content, out_file_content, "", "TLE")
                tests_list.append(current_test)
            else:
                temp_file.close()
                temp_file_content = None
                with open("temp", "r") as temp_file:
                    temp_file_content = temp_file.read()
                current_test = None
                temp_file_content = temp_file_content.strip()
                #
                # TODO: Below comparison, works for now!
                # Normal string comparisons for two files
                # Make sure this works
                if out_file_content == temp_file_content:
                    current_test = TEST(True, inp_file_content, out_file_content, temp_file_content, "Ok!")
                else:
                    current_test = TEST(False, inp_file_content, out_file_content, temp_file_content, "Not Ok!")
                tests_list.append(current_test)
            inp_file.close()
            temp_file.close()
        return tests_list
        
def main():
    init(autoreset=True)
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help = "Solution file to be tested")
    parser.add_argument("tests", help = "Location where the test files are stored")

    args = parser.parse_args()

    lang = LANG_PYTHON()
    lang.test_file(args.tests, args.file)

if __name__ == "__main__":
    main()


    