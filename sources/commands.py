import rich.errors
import typer
import random
import string
import rich
import typing as t
import os
import uuid
import sys
from sources.prompts import Prompt as p
import sources.core as core


app=typer.Typer(no_args_is_help=True)
DEFAULT_COUNT=10
DEFAULT_LENGTH=20

@app.command()
def generate(length: int=DEFAULT_LENGTH,count: int=DEFAULT_COUNT,output_path : t.Union[str,None]=None):
    
    high_password_count=1000
    
    if(count>high_password_count and not(p.prompt_for_high_password_count())):
        exit(0)
        
    use_pager=False
        
    if os.isatty(sys.stdout.fileno()) and output_path is None:
        columns,_,=os.get_terminal_size()
        use_pager=length>columns

    
        
    
    if(length<=0 or count<=0):
        raise ValueError("Length and Count should be greater than 0")
    
    passwords=core.generate_passwords(count,length)
    if output_path is None and not(use_pager):
        core.write_passwords_to_file_descriptor(passwords,sys.stdout)
        exit(0)
    
    if output_path is None:
        typer.echo_via_pager("\n".join(passwords))
        exit(0)
    
    mode="x"
    if os.path.exists(output_path) and os.path.isfile(output_path) and p.prompt_to_replace_existing_file():
        mode="w"
        

    try:
        with open(output_path,mode) as f:
            core.write_passwords_to_file_descriptor(passwords,f)
    except FileExistsError:
        rich.print("[red] Please choose another file name [/red]")
    except Exception as e:
        rich.print(f"[red] {e} [/red]")
        exit(1)


@app.command()
def gui():
    pass