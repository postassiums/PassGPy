import unittest
import subprocess
import os
import pathlib





class MyTestCase(unittest.TestCase):
    
    def setUp(self) -> None:
        self.maxDiff=None
    
    
    # def assertCLILayoutAlmostEqualToIntended(self,filepath: pathlib.Path,process_output : str):
    #     with open(filepath) as f:
    #         file_contents=f.read()
    #         self.assertEqual(process_output,file_contents,'Command Layout is not showing correctly')
            
    def assertCLIOutputMustHaveWords(self,process_output: str,necessary_texts: list[str]):
        self.assertIsNotNone(process_output,'There was no Output')
        self.assertTrue(all(text in process_output for text in necessary_texts ))
    
    def assertProgramExitCode(self,exit_code : int):
        self.assertEqual(exit_code,0,'Program did not terminate sucessufully')
        
    def assertCLILayout(self,std_out : str,expected_texts : str,file_path : str):
        self.assertCLIOutputMustHaveWords(std_out,expected_texts)
        #self.assertCLILayoutAlmostEqualToIntended(file_path,std_out)
        
        
    
        

class CLITester():
    TEST_PATH=pathlib.Path('tests')
    TMP_PATH=TEST_PATH.joinpath('tmp')
    SCREENS_PATH=TEST_PATH.joinpath('screens')
    
    @classmethod
    def run_command(cls,args : list[str]=[])-> tuple[int,str]:
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
            output=f.read()
            return output
    
    

class TestHelpCommand(MyTestCase):
    
    EXPECTED_WORDS_WHEN_MAIN_HELP_OPTION=['--help','generate','Commands','Options','gui']
    EXPECTED_WORDS_WHEN_HELP_GENERATE_OPTION=['--count','--help','--length','--count','--output-path','generate','Options']
    HELP_SCREEN_PATH=CLITester.SCREENS_PATH.joinpath('help.txt')
    HELP_GENERATE_SCREEN_PATH=CLITester.SCREENS_PATH.joinpath('generate/help.txt')
    
    
    def setUp(self) -> None:
        return super().setUp()
    

    def test_help_menu_is_rendering_when_no_args_are_given(self):
        
        std_out=CLITester.run_command()
        self.assertCLILayout(std_out,self.EXPECTED_WORDS_WHEN_MAIN_HELP_OPTION,self.HELP_SCREEN_PATH)
       
   
            
    def test_help_menu_is_rendering_when_using_arg(self):
        std_out=CLITester.run_command(['--help'])
        self.assertCLILayout(std_out,self.EXPECTED_WORDS_WHEN_MAIN_HELP_OPTION,self.HELP_SCREEN_PATH)
    
    def test_generate_help_menu_is_rendering(self):
        std_out=CLITester.run_command(['generate','--help'])

        self.assertCLILayout(std_out,self.EXPECTED_WORDS_WHEN_HELP_GENERATE_OPTION,self.HELP_GENERATE_SCREEN_PATH)
        

        
class TestGenerateCommand(MyTestCase):
    def test_generate_screen_renders_correctly(self):
        pass
    
    def test_generate_is_generating_passwords(self):
        pass
    def test_length_arg_is_working(self):
        pass
    def test_count_arg_is_working(self):
        pass
    
    def test_generate_can_save_passwords_to_file(self):
        pass
        
        


if __name__.__eq__('__main__'):
    unittest.main()
        