"""
Author: Bradley Fernando
Purpose: Sends a file using netmiko_file_transfer plugin. Deletes the file using
         netmiko prompting. 

Usage:
    python exercise4.py

Output:
    nxos1: bf-license.txt
      transferring - Success
      deleting - Success
    --------------------------------------------------------------------------------
    del bootflash:/bf-license.txt
    
    Do you want to delete "/bf-license.txt" ? (yes/no/abort)   [y] y
    
    nxos1#
"""


from nornir import InitNornir
from nornir.plugins.tasks import networking
import colorama


def send_file(task):
    group_name = task.host.platform
    base_file = task.host['file_name']
    source_file = f"{group_name}/{base_file}"
    dest_file = base_file

    results = task.run(
                task=networking.netmiko_file_transfer,
                source_file=source_file,
                dest_file=dest_file,
                overwrite_file=True,
                direction="put"
              )
    if results.result is False:
        print("File transfer failed")
    else:
        colorama.init()
        print(task.host, end='')
        print(": " + base_file)
        print("  transferring - ", end='')
        print(colorama.Fore.GREEN + "Success" +
              colorama.Style.RESET_ALL)


def delete_file(task):
    """
    # Delete sequence:
    nxos1# del bootflash:/testx.txt
    Do you want to delete "/testx.txt" ? (yes/no/abort)   [y] y
    """

    # Manually create Netmiko connection
    net_connect = task.host.get_connection("netmiko", task.nornir.config)

    file_name = task.host['file_name']
    del_cmd = f"del bootflash:/{file_name}"
    cmd_list = [del_cmd, "y"]
    output = ""

    for cmd in cmd_list:
        output += net_connect.send_command_timing(
            cmd, strip_prompt=False, strip_command=False
        )

    # Verify file has been removed
    check_cmd = f"dir bootflash | grep {file_name}"
    result = net_connect.send_command(check_cmd)
    if not result:
        print("  deleting - ", end='')
        print(colorama.Fore.GREEN + "Success" +
              colorama.Style.RESET_ALL)
    print('-' * 80)
    print(output)


def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(name="nxos1")
    nr.run(task=send_file)
    nr.run(task=delete_file)


if __name__ == "__main__":
    main()
