# --- Student Starter File: The Log File Forensic Challenge ---

input_file = "raw_logs.txt"
output_file = "audit_report.txt"

file = open(input_file, "r")
lines = file.readlines()
file.close()
security_alerts = []
processed_lines = []

for line in lines:
    parts = line.split("|")

    if len(parts) == 4:
        timestamp = parts[0].strip()
        ip_address = parts[1].strip()
        status_code = parts[2].strip()
        username = parts[3].strip()

    if status_code == "403":
        security_alerts.append((username.upper))

    report_entry = f"User {username} accessed the system from {ip_address}"
    processed_lines.append(report_entry)

    out = open(output_file, "w")
total_alerts = len(security_alerts)
out.write("Total Suspicious Attempts Found: " + str(total_alerts) + "\n")
out.write("-" * 30 + "\n")
out.write("Access Log Summary:\n")
for entry in processed_lines:
    out.write(entry + "\n")
out.write("\nFlagged Usernames (403 Forbidden):\n")

for user in security_alerts:
    out.write(f"- {user}\n") 
out.close()

out.close()

print("Task complete! Check your audit_report.txt file.")

