import paramiko


def monitor_logs(host, username, password, log_file_path):

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=host, username=username, password=password)

    stdin, stdout, stderr = ssh_client.exec_command(f"tail -f {log_file_path}")

    print("".join(stdout.readlines()))

    ssh_client.close()


if __name__ == "__main__":

    host = "remote_server_ip"
    username = "remote_username"
    password = "remote_password"
    log_file_path = "/path/to/log_file.log"

    monitor_logs(host, username, password, log_file_path)
