import typer

def prompt_to_replace_file()-> str:
    return typer.confirm("File already exists, do you want to replace it?")


def prompt_new_file_name()-> str:
    return typer.prompt("Please enter a new file name")


def prompt_for_high_password_count()-> bool:
    return typer.confirm("Are you sure you want to generate more than 1000 passwords?")



def prompt_to_replace_existing_file() -> bool:
    return typer.confirm("File already exists, do you want to replace it?",default=False)
