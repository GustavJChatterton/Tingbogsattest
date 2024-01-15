# import sqlite3
#
# connection = sqlite3.connect("TingBogsattest")
# cursor = connection.cursor()


import datetime

# Get the current date and time
now = datetime.datetime.now(datetime.timezone.utc)

# Format the date and time in the specified format: "yyyy-mm-ddThh:mm:ssZ"
formatted_date = now.strftime("%Y-%m-%dT%H:%M:%SZ")

print(formatted_date)

