import typer

class Prompt:
    ASK_REPLACE= "File already exists, do you want to replace it?"
    
    @staticmethod
    def prompt_new_file_name()-> str:
        return typer.prompt("Please enter a new file name")

    @staticmethod
    def prompt_for_high_password_count()-> bool:
        return typer.confirm("Are you sure you want to generate more than 1000 passwords?")


    @classmethod
    def prompt_to_replace_existing_file(cls) -> bool:
        return typer.confirm(cls.ASK_REPLACE,default=False)
