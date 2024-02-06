# import datetime
# mx_records=[{'first_seen': '2022-06-16', 'last_seen': '2022-04-28', 'organizations': ['TEKNO company'], 'type': 'mx', 'values': [{'host': 'smtp.teknobyte.com', 'mx_count': 26463, 'priority': 8}, {'host': 'aspmx.l.teknobyte.com', 'mx_count': 15207728, 'priority': 10}, {'host': 'alt1.aspmx.l.teknobyte.com', 'mx_count': 14980461, 'priority': 20}, {'host': 'alt2.aspmx.l.teknobyte.com', 'mx_count': 14907437, 'priority': 30}, {'host': 'alt3.aspmx.l.teknobyte.com', 'mx_count': 10715705, 'priority': 40}, {'host': 'alt4.aspmx.l.teknobyte.com', 'mx_count': 10656814, 'priority': 50}]}, {'first_seen': '2021-08-04', 'last_seen': '2022-04-16', 'organizations': ['TEKNO company'], 'type': 'mx', 'values': [{'host': 'aspmx.l.teknobyte.com', 'mx_count': 15207728, 'priority': 10}, {'host': 'alt1.aspmx.l.teknobyte.com', 'mx_count': 14980461, 'priority': 20}, {'host': 'alt2.aspmx.l.teknobyte.com', 'mx_count': 14907437, 'priority': 30}, {'host': 'alt3.aspmx.l.teknobyte.com', 'mx_count': 10715705, 'priority': 40}, {'host': 'alt4.aspmx.l.teknobyte.com', 'mx_count': 10656814, 'priority': 50}]}, {'first_seen': '2021-07-28', 'last_seen': '2021-08-04', 'organizations': ['TEKNO company'], 'type': 'mx', 'values': [{'host': 'smtp.teknobyte.com', 'mx_count': 26463, 'priority': 0}, {'host': 'aspmx.l.teknobyte.com', 'mx_count': 15207728, 'priority': 10}, {'host': 'alt1.aspmx.l.teknobyte.com', 'mx_count': 14980461, 'priority': 20}, {'host': 'alt2.aspmx.l.teknobyte.com', 'mx_count': 14907437, 'priority': 30}, {'host': 'alt3.aspmx.l.teknobyte.com', 'mx_count': 10715705, 'priority': 40}, {'host': 'alt4.aspmx.l.teknobyte.com', 'mx_count': 10656814, 'priority': 50}]}, {'first_seen': '2018-09-05', 'last_seen': '2021-07-28', 'organizations': ['TEKNO company'], 'type': 'mx', 'values': [{'host': 'aspmx.l.teknobyte.com', 'mx_count': 15207728, 'priority': 10}, {'host': 'alt1.aspmx.l.teknobyte.com', 'mx_count': 14980461, 'priority': 20}, {'host': 'alt2.aspmx.l.teknobyte.com', 'mx_count': 14907437, 'priority': 30}, {'host': 'alt3.aspmx.l.teknobyte.com', 'mx_count': 10715705, 'priority': 40}, {'host': 'alt4.aspmx.l.teknobyte.com', 'mx_count': 10656814, 'priority': 50}]}, {'first_seen': '2013-07-19', 'last_seen': '2013-07-21', 'organizations': ['TEKNO company'], 'type': 'mx', 'values': [{'host': 'aspmx.l.teknobyte.com', 'mx_count': 15207728, 'priority': 10}, {'host': 'alt1.aspmx.l.teknobyte.com', 'mx_count': 14980461, 'priority': 20}, {'host': 'alt2.aspmx.l.teknobyte.com', 'mx_count': 14907437, 'priority': 30}, {'host': 'alt3.aspmx.l.teknobyte.com', 'mx_count': 10715705, 'priority': 40}, {'host': 'alt4.aspmx.l.teknobyte.com', 'mx_count': 10656814, 'priority': 50}]}]

# # Extract the month abbreviation from the first record
# first_seen = mx_records[0]['first_seen']
# month_abbr = datetime.datetime.strptime(first_seen, '%Y-%m-%d').strftime('%b')

# print(month_abbr)



# import requests

# def check_domain_availability(domain):
#     url = "http://" + domain  # Prepend http:// to the domain
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             return True  # Domain is alive
#         else:
#             return False  # Domain is not alive
#     except requests.exceptions.RequestException:
#         return False  # Error occurred, domain is not alive

# # Example usage:
# domain = "google.com"
# is_alive = check_domain_availability(domain)
# print(f"Is {domain} alive? {is_alive}")


import socket

def check_domain_availability(domain):
    # try:
        if socket.gethostbyname(domain):
            return True  # Domain exists
        else:
            return False
    # except socket.gaierror:
    #     return False  # Domain does not exist

# Example usage:
domain = "india.gov.in/"
domain_exists = check_domain_availability(domain)
print(f"Does {domain} exist? {domain_exists}")
