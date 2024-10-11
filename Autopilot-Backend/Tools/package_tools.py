from os import environ
from pexpect import spawn

def handle_sudo(process: spawn): 
    password = environ.get("PASS")
    process.expect('password')
    process.sendline(str(password))
    return process

def install_package(name: str): 
    """
        install_package this tool run the command 
        'sudo pacman -S name' on the shell to install 
        a software package on the system it takes in 
        the name then returns the output of installation
        Args: 
            name: string
        Returns: 
            returns what happened after execution
    """
    process = spawn(f"sudo pacman -S {name}")
    process = handle_sudo(process)
    expectation = process.expect(["[Y/n]","target not found"])
    if expectation == 0:
        process.sendline("y")
        process.expect("")
    return process.read().decode()

