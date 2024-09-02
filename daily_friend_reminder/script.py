import os
import requests
import datetime
import templates

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

google_sheets_content = requests.get(
    "https://api.zerosheets.com/v1/ugz",
    headers={
        "Authorization": "Bearer " + os.environ.get("PERSONAL_ZERO_SHEETS_API_KEY"),
    },
)

google_sheets_data = google_sheets_content.json()
for item in google_sheets_data:
    last_hangout_date = item["Last Hangout"].strip()
    if last_hangout_date:
        try:
            date_obj = datetime.datetime.strptime(last_hangout_date, "%B %d, %Y")
            item["epoch"] = int(date_obj.timestamp())
        except ValueError as e:
            print(e)
            print(f"Invalid date format: {last_hangout_date} for item: {item}")
            item["epoch"] = None

sorted_sheets_data = sorted(google_sheets_data, key=lambda x: x["epoch"], reverse=True)

local_template = str(templates.html_table)
for item in sorted_sheets_data:
    if item["epoch"] is None:
        print(f'Cannot send email for {item["Name"]}')
        continue

    local_template += f"""
    <tr>
      <td>{item['Name']}</td>
      <td>{item['Last Hangout']}</td>
      <td>{item['Location']}</td>
      <td>{item['Notes']}</td>
    </tr>
    """

local_template += """
  </table>
</body>
</html>
"""

message = Mail(
    from_email=os.environ.get("ICLOUD_EMAIL"),
    to_emails=os.environ.get("GMAIL_EMAIL"),
    subject="Daily Friends Reminder",
    html_content=local_template,
)

try:
    sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
    response = sg.send(message)
    print(response.headers)
except Exception as e:
    print(e.to_dict)
    raise e

print("Done")
