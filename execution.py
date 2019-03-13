from colorama import init, Fore, Style, Back
import subprocess
import argparse
import os

class TEST:
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
        self.tle = 5
        self.command = ""

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


class CPLUS(LANGUAGE_EXEC):
    """
        Class to support execution of c++ files
    """
    def __init__(self):
        self.command = "g++"
        self.args = []
        self.tle = 10

    def test_file(self, tests_location, sol_file):
        """
            Stage 1:
                Compile the file to check for errors, if there are erros present let the user know.
                Don't continue further.

                If this stage doesn't produce any error, move ahead to stage 2.
        """
        try:
            completed = subprocess.run(
                [self.command, sol_file],
                timeout = self.tle,
                check = True,
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE
            )
        except subprocess.CalledProcessError as err:
            print(err.stderr.decode('utf-8'))
            return
        except subprocess.TimeoutExpired as err:
            print("The program took too much time to compile.")
            return
        
        """
            Stage 2:
                Get a listing of all the test files on which the input program is to be tested.
        """
        files = os.listdir(tests_location)
        input_files = []
        for current in files:
            if current.startswith("input"):
                input_files.append(current)

        """
            Stage 3:
                For each input files on which the program is to be tested, test the program and make
                note of the output for comparison purposes.
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
                    ["./a.out"],
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
        self.print_status(tests_list)
        return


def main():
    init(autoreset=True)
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help = "Solution file to be tested")
    parser.add_argument("tests", help = "Location where the test files are stored")

    args = parser.parse_args()

    lang = CPLUS()
    lang.test_file(args.tests, args.file)

if __name__ == "__main__":
    main()


    