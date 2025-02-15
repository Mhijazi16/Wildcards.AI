from .shell_toolkit import handle_sudo, read_status, send_to_terminal, start_terminal
import pexpect
import os

def command_factory(name, action): 
    command = ""
    status = f"sudo systemctl status {name} | head -30"
    try:
        if "start" in action:
            command = f"sudo systemctl start {name}"
        elif "stop" in action:
            command = f"sudo systemctl stop {name}"
        elif "restart" in action:
            command = f"sudo systemctl restart {name}"
        elif "reload" in action:
            command = f"sudo systemctl reload {name}"
        elif "status" in action:
            command = status
        elif "enable" in action:
            command = f"sudo systemctl enable {name}"
        elif "disable" in action:
            command = f"sudo systemctl disable {name}"
        else:
            raise ValueError(f"Unsupported action: {action}")
    except Exception as e:
        print(f"[ERROR] no suitable action! {e}")
    finally:
        return command

def system_service_control(name:str, action: str): 
    """
        This tool is used to control system service 
        it starts/stops/reloads/enables/disables/shows status
        of the service 
        Args: 
            name: str which is the name of service 
            action: str action performed
        Important Notes: 
            action can only be one of the following values: 
            start 
            stop
            restart
            reload
            status 
            enable
            disable
    """
    try:
        output = ""
        command = command_factory(name, action)
        if command == "": 
            raise ValueError(f"Unsupported action: {action}")

        start_terminal(command)
        process = pexpect.spawn(command)
        process, message = handle_sudo(process)
        message = read_status(process)
        if "Failed" in message or "error" in message: 
            raise Exception

        if "status" not in action: 
            output = f"✅ {name} Service Successfull {action}.\n"
            send_to_terminal(output)
            status = f"systemctl status {name} | head -30"
            send_to_terminal(os.popen(status).read())
        else: 
            status = f"systemctl status {name} | head -30"
            send_to_terminal(os.popen(status).read())

    except: 
        output = f"🚨 faild Starting {name} service.\n"
        send_to_terminal(output)
        print(f"[INFO] {output}")
    finally: 
        return output

def list_process():
    """
        This tool is used to list 
        the process running on the system
        it execute the command ps -aux
    """
    try:
        command = "ps -aux"
        result = os.popen(command).read()
        start_terminal(command)
        send_to_terminal(result)
        return result
    except Exception:
        send_to_terminal("🚨 Failed listing the Processes.")

def kill_process(name: str): 
    """
    this tool is used to kill a 
    process on the linux system 
    it runs pkill <process_name> 
    command 
    """
    try:
        command = f"pkill {name}"
        result = os.popen(command).read()
        start_terminal(command)
        send_to_terminal("✅ Process was killed")
        return result
    except Exception:
        send_to_terminal("🚨 Failed Killing the process.")

def get_service_logs(name: str): 
    """
    this tool is used to display the 
    latest 30 logs of some service 
    Args: 
        name: str
    Returns: 
        logs of the system
    """
    result = ""
    try:
        command = f"journalctl -u {name}.service | tail -30"
        result = os.popen(command).read()
        start_terminal(command)
        send_to_terminal(result)
    except Exception:
        send_to_terminal("🚨 Failed Killing the process.")
    finally: 
        return result

def run_command_in_background(command: str): 
    """
    this tool is used to run 
    command in the background 
    Args: 
        command: str
    """
    result = ""
    try:
        command = f"{command} &; exit;"
        result = os.popen(command).read()
        start_terminal(command)
        result += "✅ The Process is running in the Background."
    except Exception:
        result += "🚨 Failed Running Process in the Background."
    finally: 
        send_to_terminal(result)
        return result

def get_process_toolkit():
    return [
        system_service_control,
        list_process,
        kill_process,
        get_service_logs,
        run_command_in_background,
    ]
