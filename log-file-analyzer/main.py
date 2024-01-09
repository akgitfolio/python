import pandas as pd
import re
from datetime import datetime

access_log_path = "access.log"

def parse_log_line(line):
    log_pattern = re.compile(
        r'(?P<ip>\S+) - - \[(?P<timestamp>[^\]]+)\] "(?P<method>\S+) (?P<url>\S+) \S+" (?P<http_status_code>\d+) \S+ "(?P<referer>[^"]*)" "(?P<user_agent>[^"]*)"'
    )
    match = log_pattern.match(line)
    if match:
        return match.groupdict()
    return None

logs = []
with open(access_log_path, 'r') as file:
    for line in file:
        parsed_line = parse_log_line(line)
        if parsed_line:
            parsed_line['timestamp'] = datetime.strptime(parsed_line['timestamp'], '%d/%b/%Y:%H:%M:%S %z')
            logs.append(parsed_line)

logs_df = pd.DataFrame(logs)
grouped_logs = logs_df.groupby('ip')

def analyze_log_group(group):
    threats = []
    if len(group) > 10 and (group['timestamp'].max() - group['timestamp'].min()).total_seconds() < 60:
        threats.append("Potential DoS attack")
    restricted_urls = ["/admin", "/users"]
    for url in restricted_urls:
        if any(group["url"] == url):
            threats.append(f"Unauthorized access attempt to {url}")
    unusual_agents = ["curl", "Python-urllib"]
    if any(user_agent in group["user_agent"].values for user_agent in unusual_agents):
        threats.append("Potential bot activity")
    return threats

results = []
for ip, group in grouped_logs:
    threats = analyze_log_group(group)
    if threats:
        results.append({"IP": ip, "Threats": ", ".join(threats)})

report_df = pd.DataFrame(results)
report_df.to_csv("security_report.csv", index=False)

print("Analysis complete! Report generated: security_report.csv")
