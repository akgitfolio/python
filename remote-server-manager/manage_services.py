import paramiko


def manage_service(host, username, password, service_name, action):

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=host, username=username, password=password)

    stdin, stdout, stderr = ssh_client.exec_command(
        f"sudo systemctl {action} {service_name}"
    )

    print("".join(stdout.readlines()))
    print("".join(stderr.readlines()))

    ssh_client.close()


if __name__ == "__main__":

    host = "remote_server_ip"
    username = "remote_username"
    password = "remote_password"
    service_name = "my_service"
    action = "restart"

    manage_service(host, username, password, service_name, action)
