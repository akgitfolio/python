import paramiko


def deploy_updates(host, username, password, update_script_path):

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=host, username=username, password=password)

    stdin, stdout, stderr = ssh_client.exec_command(f"bash {update_script_path}")

    print("".join(stdout.readlines()))
    print("".join(stderr.readlines()))

    ssh_client.close()


if __name__ == "__main__":

    host = "remote_server_ip"
    username = "remote_username"
    password = "remote_password"
    update_script_path = "/path/to/update_script.sh"

    deploy_updates(host, username, password, update_script_path)
