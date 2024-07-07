import random
import string
import typer
import typing as t
def get_supported_characters():
    return f"{string.ascii_letters}{string.digits}"
    
    
def generate_password(length: int)-> str: 
    alphabet=get_supported_characters()
    alphabet_len=len(alphabet)
    password=""
    for _ in range(length):
        index=random.randrange(0,alphabet_len)
        password+=alphabet[index]
    return password


def generate_passwords(count: int,length: int) -> list[str]:
    passwords=[]
    for _ in range(count):
            new_password=generate_password(length)
            passwords.append(new_password)
    return passwords



def write_passwords_to_file_descriptor(passwords: t.List[str],f=None) -> None:
    for password in passwords:
        typer.echo(password,f)