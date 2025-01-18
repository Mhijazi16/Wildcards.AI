import os
import subprocess
from shell_toolkit import start_terminal, send_to_terminal

def compile_program(pathname: str):
    """
    This Tool is used to Compiles and runs a C/C++ file.
    Args:
        pathname (str): The full path to the C/C++ file.
    Returns:
        str: The output of the compiled program or an error message.
    """

    output = ""
    output_file = os.path.splitext(pathname)[0]
    try:

        compiler = "g++" if pathname.endswith(".cpp") else "gcc"
        command = [compiler, pathname, "-o", output_file]
        start_terminal(" ".join(command))

        if not pathname.endswith(('.c', '.cpp')):
            output = "Error: The file is not a C or C++ source file.\n"
            raise Exception()

        if not os.path.exists(pathname):
            output = f"Error: File '{pathname}' does not exist.\n"
            raise Exception()


        result = subprocess.run(command, capture_output=True, text=True)
        send_to_terminal(result)

        if result.returncode != 0:
            raise Exception()

        output = "✅ Compiled Successfully\n"
    except Exception:
        output += f"🚨 Compilation failed\n"
    finally: 
        send_to_terminal(output)

    final = output
    try:
        final = os.popen(f"{output_file}").read()
        start_terminal(output_file)
        output = f"✅ Successfully Executed program output: \n\n {final}"
    except Exception:
        output = f"🚨 Executing failed output: \n\n{final}"
    finally: 
        send_to_terminal(output)

    return final + output
