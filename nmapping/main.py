import nmap


def scan_host(target_host):

    nm = nmap.PortScanner()

    try:

        nm.scan(target_host, arguments="-sS -p- -sV -O")
    except Exception as e:
        print("An error occurred:", str(e))

    for host in nm.all_hosts():
        print("Host: %s (%s)" % (host, nm[host].hostname()))
        print("State: %s" % nm[host].state())
        for proto in nm[host].all_protocols():
            print("Protocol: %s" % proto)
            ports = nm[host][proto].keys()
            for port in ports:
                print(
                    "Port: %s\tState: %s\tService: %s"
                    % (
                        port,
                        nm[host][proto][port]["state"],
                        nm[host][proto][port]["name"],
                    )
                )
                if "product" in nm[host][proto][port]:
                    print("\tProduct: %s" % nm[host][proto][port]["product"])
                if "version" in nm[host][proto][port]:
                    print("\tVersion: %s" % nm[host][proto][port]["version"])
        if "osclass" in nm[host]:
            print("OS Details:")
            for osclass in nm[host]["osclass"]:
                print("\t%s" % osclass["description"])


target_hosts = ["192.168.1.1", "192.168.1.2", "192.168.1.3"]
for host in target_hosts:
    print("Scanning host:", host)
    scan_host(host)
    print("=" * 50)
