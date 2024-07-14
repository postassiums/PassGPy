import unittest
import subprocess
import os
import pathlib
import re
import random
import shutil
class CLI():
    from sources.commands import DEFAULT_COUNT,DEFAULT_LENGTH
    TEST_PATH=pathlib.Path('tests')
    TMP_PATH=TEST_PATH.joinpath('tmp')
    SCREENS_PATH=TEST_PATH.joinpath('screens')
    PASSWORD_PATTERN=r'^[A-z0-9]+$'

    
    @classmethod
    def generate(cls,count : int=DEFAULT_COUNT,length : int=DEFAULT_LENGTH,output : str=None,strip_stdout : bool=True):
        arguments=['generate']
        argument_map={
            '--count':count,
            '--length':length,
            '--output-path':output
        }
        for arg,value in argument_map.items():
            if value:
                arguments.append(arg)
                arguments.append(str(value))

        std_out=cls.run_command(arguments)
        if strip_stdout:
            std_out=list(map(lambda x: x.strip(),std_out))
        
        return std_out
    
    @classmethod
    def run_command(cls,args : list[str]=[])-> list[str]:
        with open(cls.TMP_PATH.joinpath('help.txt'),'w+',encoding='utf-8') as f:
            process_args=['python3','.']
            process_args.extend(args)
            process : subprocess.CompletedProcess =subprocess.run(process_args,stdout=f,stderr=subprocess.DEVNULL,stdin=subprocess.DEVNULL)
            try:
                process.check_returncode()
            except subprocess.CalledProcessError as e:
                print('Process did not complete sucesufully')
                print(e)
                exit(1)
            f.seek(0)
            output=f.readlines()
            return output

class MyTestCase(unittest.TestCase):
    
    def setUp(self) -> None:
        self.maxDiff=None


    
    
    @staticmethod
    def filter_cli_decorations(line: str):
        return re.sub(r'[╭─╮╰╯\s]+','',line.strip())
    

    
    def assertScreenAndStdOutLinesMatch(self,lines_of_stdout : list[str],lines_of_screen_file : list[str]):
        lines_of_stdout=list(map(self.filter_cli_decorations,lines_of_stdout))
        lines_of_screen_file=list(map(self.filter_cli_decorations,lines_of_screen_file))
        self.assertListEqual(lines_of_stdout,lines_of_screen_file,'Screen Layout does not match expected')
        
        
    def assertPasswordsCount(self,lines_of_stdout : list[str],expected_count : int):
        self.assertEqual(len(lines_of_stdout),expected_count,'Password count is different from expected')

    def assertPasswordsArePasswords(self,lines_of_stdout : list[str],password_regex : re.Pattern):
        for password in lines_of_stdout:
            self.assertPasswordIsPassword(password,password_regex)
            
    def assertPasswordsAreGivenLength(self,lines_of_stdout : list[str],expected_length : int):
        for password in lines_of_stdout:
            self.assertPasswordIsTheGivenLength(password,expected_length)
    
    def assertPasswordIsPassword(self,password : str,password_regex : re.Pattern):
        self.assertRegex(password,password_regex,'Password pattern is different from expected')
    
    def assertPasswordIsTheGivenLength(self,password: str,expected_length):
        self.assertEqual(len(password),expected_length,'Password length is different from expected')
    
    def assertProgramExitCode(self,exit_code : int):
        self.assertEqual(exit_code,0,'Program did not terminate sucessufully')
        
    def assertPasswordsWereGeneratedCorrectly(self,lines_of_stdout : list[str],password_regex : re.Pattern=CLI.PASSWORD_PATTERN,
                                              expected_length : int=CLI.DEFAULT_LENGTH,expected_count: int=CLI.DEFAULT_COUNT):
        self.assertPasswordsCount(lines_of_stdout,expected_count)

        self.assertPasswordsArePasswords(lines_of_stdout,password_regex)
        self.assertPasswordsAreGivenLength(lines_of_stdout,expected_length)
        
        
    def assertCLILayout(self,filepath: pathlib.Path,lines_of_stdout : list[str]):
        with open(filepath) as f:
            file_contents=f.readlines()
            
            self.assertScreenAndStdOutLinesMatch(lines_of_stdout,file_contents)
        
        
    
        


    
    

class TestHelpCommand(MyTestCase):
    HELP_SCREEN_PATH=CLI.SCREENS_PATH.joinpath('help.txt')
    HELP_GENERATE_SCREEN_PATH=CLI.SCREENS_PATH.joinpath('generate/help.txt')
    
    
    def setUp(self) -> None:
        return super().setUp()
    

    def test_menu_is_rendering_when_no_args_are_given(self):
        
        std_out=CLI.run_command()
        self.assertCLILayout(self.HELP_SCREEN_PATH,std_out)
       
   
            
    def test_help_menu_is_rendering_when_using_arg(self):
        std_out=CLI.run_command(['--help'])
        self.assertCLILayout(self.HELP_SCREEN_PATH,std_out)
    
    def test_generate_help_menu_is_rendering(self):
        std_out=CLI.run_command(['generate','--help'])

        self.assertCLILayout(self.HELP_GENERATE_SCREEN_PATH,std_out)
        

        
class TestGenerateCommand(MyTestCase):


    def setUp(self) -> None:
        self.SUBSTEST_COUNT=10


    
    def test_is_generating_passwords_using_default_args(self):
        lines_of_stdout=CLI.generate()
        self.assertPasswordsWereGeneratedCorrectly(lines_of_stdout)

    


        
    def test__only_length_is_random(self):
        for i in range(0,self.SUBSTEST_COUNT):
            random_length=random.randrange(1,self.SUBSTEST_COUNT)
            with self.subTest(f'Length: {random_length}'):
                lines_of_stdout=CLI.generate(length=random_length)
                self.assertPasswordsWereGeneratedCorrectly(lines_of_stdout,expected_length=random_length)
                
    
    
    
        
    def test_only_count_is_random(self):
        for i in range(0,self.SUBSTEST_COUNT):
            random_count=random.randrange(1,self.SUBSTEST_COUNT)
            with self.subTest(f'Count: {random_count}'):
                lines_of_stdout=CLI.generate(count=random_count)
                self.assertPasswordsWereGeneratedCorrectly(lines_of_stdout,expected_length=CLI.DEFAULT_LENGTH,expected_count=random_count)
                

        
    def test_using_random_arguments_for_count_and_length(self):
        
        for i in range(0,self.SUBSTEST_COUNT):
            random_count=random.randrange(1,self.SUBSTEST_COUNT)
            random_length=random.randrange(1,self.SUBSTEST_COUNT)
            with self.subTest(f'Count:  {random_count}, Length: {random_length}'):
                lines_of_stdout=CLI.generate(count=random_count,length=random_length)
                self.assertPasswordsWereGeneratedCorrectly(lines_of_stdout,expected_length=random_length,expected_count=random_count)

            
    
    def test_can_save_passwords_to_new_file(self):
        output_path=CLI.TMP_PATH.joinpath('passwords.txt')
        os.remove(output_path)
        CLI.generate(output=str(output_path))
        with open(output_path,'r',encoding='utf-8') as f:
            passwords=list(map(lambda x: x.strip(),f.readlines()))
            
            self.assertIsNotNone(passwords,'Passwords are not being saved into a file')
            self.assertPasswordsWereGeneratedCorrectly(passwords)
            
    def test_can_replace_file_when_confirming(self):
        output_path=CLI.TMP_PATH.joinpath('passwords.txt')
        with open(output_path,'w',encoding='utf-8') as f:
            f.write('This is a file')
        
        with open(CLI.SCREENS_PATH.joinpath('generate/replace.txt'),'r',encoding='utf-8') as f:
            question=CLI.generate(output=str(output_path))
            expected_question=f.readline().strip()
            self.assertEqual(question[0],expected_question,'Question is different from expected')

        
        
        


if __name__.__eq__('__main__'):
    unittest.main()
        