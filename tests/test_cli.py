import unittest
import subprocess
import os
import pathlib
import re
import random



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
        
    def assertCLILayout(self,filepath: pathlib.Path,lines_of_stdout : list[str]):
        with open(filepath) as f:
            file_contents=f.readlines()
            
            self.assertScreenAndStdOutLinesMatch(lines_of_stdout,file_contents)
        
        
    
        

class CLI():
    TEST_PATH=pathlib.Path('tests')
    TMP_PATH=TEST_PATH.joinpath('tmp')
    SCREENS_PATH=TEST_PATH.joinpath('screens')
    

    
    @classmethod
    def generate(cls,args=[]):
        arguments=['generate']
        arguments.extend(args)
        return cls.run_command(arguments)
    
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
    
    

class TestHelpCommand(MyTestCase):
    HELP_SCREEN_PATH=CLI.SCREENS_PATH.joinpath('help.txt')
    HELP_GENERATE_SCREEN_PATH=CLI.SCREENS_PATH.joinpath('generate/help.txt')
    
    
    def setUp(self) -> None:
        return super().setUp()
    

    def test_help_menu_is_rendering_when_no_args_are_given(self):
        
        std_out=CLI.run_command()
        self.assertCLILayout(self.HELP_SCREEN_PATH,std_out)
       
   
            
    def test_help_menu_is_rendering_when_using_arg(self):
        std_out=CLI.run_command(['--help'])
        self.assertCLILayout(self.HELP_SCREEN_PATH,std_out)
    
    def test_generate_help_menu_is_rendering(self):
        std_out=CLI.run_command(['generate','--help'])

        self.assertCLILayout(self.HELP_GENERATE_SCREEN_PATH,std_out)
        

        
class TestGenerateCommand(MyTestCase):
    from sources.commands import DEFAULT_COUNT,DEFAULT_LENGTH

    def setUp(self) -> None:
        self.PASSWORD_PATTERN=r'^[A-z1-9]+$'
    
    def test_generate_is_generating_passwords(self):
        lines_of_stdout=CLI.generate()
        
        self.assertPasswordsCount(lines_of_stdout,len(lines_of_stdout))

        self.assertPasswordsArePasswords(lines_of_stdout,self.PASSWORD_PATTERN)
        self.assertPasswordsAreGivenLength(lines_of_stdout,self.DEFAULT_LENGTH)
        
        
    def test_length_arg_is_working(self):
        for i in range(0,10):
            with self.subTest(f'Generating random arguments, iteration: {i}'):
                random_length=str(random.randrange(1,100))
                lines_of_stdout=CLI.generate(['--length',random_length])
                
                self.assertPasswordsCount(lines_of_stdout,len(lines_of_stdout))

                self.assertPasswordsArePasswords(lines_of_stdout,self.PASSWORD_PATTERN)
                self.assertPasswordsAreGivenLength(lines_of_stdout,random_length)
        
        
    def test_count_arg_is_working(self):
        for i in range(0,10):
            with self.subTest(f'Generating random arguments, iteration: {i}'):
                random_count=str(random.randrange(1,100))
                lines_of_stdout=CLI.generate(['--count',random_count])
                
                self.assertPasswordsCount(lines_of_stdout,len(lines_of_stdout))
                self.assertPasswordsAreGivenLength(lines_of_stdout,self.DEFAULT_LENGTH)
        
    def test_generate_with_random_arguments(self):
        
        for i in range(0,10):
            with self.subTest(f'Generating random arguments, iteration: {i}'):
                random_length=str(random.randrange(1,100))
                random_count=str(random.randrange(1,100))
                lines_of_stdout=CLI.generate(['--length',random_length,'--count',random_count])
                
                self.assertPasswordsCount(lines_of_stdout,len(lines_of_stdout))

                self.assertPasswordsArePasswords(lines_of_stdout,self.PASSWORD_PATTERN)
                self.assertPasswordIsTheGivenLength(lines_of_stdout,random_length)
            
    
    def test_generate_can_save_passwords_to_file(self):
        output_path=CLI.TMP_PATH.joinpath('passwords.txt')
        CLI.generate(['--output',output_path.__str__()])
        with open(output_path,'r',encoding='utf-8') as f:
            passwords=f.readlines()
            self.assertIsNotNone(passwords,'Passwords are not being saved into a file')
        
        
        


if __name__.__eq__('__main__'):
    unittest.main()
        