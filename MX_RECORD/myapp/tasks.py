


# -1 = Domain is not live 
# -2 means that the domain is live but the MX records are not found
# -3 means that the domain is live and MX record are found , Now we don't have to check it again

import socket
import datetime
import requests
from celery import shared_task
from .models import UnverifiedData, Domain, MXRecordcurrent, MXRecordAll, MailServercurrent, MailServerHistorical
from . import API
@shared_task
def fetch_and_store_data():
    ANS=""
    if API.API_KEY =='':
        ANS='API key is empty'

    try:
        data = UnverifiedData.objects.exclude(s_no__in=[-1, -2, -3]).first()
        if data is not None:
            domain_name = data.website
            state = data.state
            country = data.country
            if not Domain.objects.filter(name=domain_name).exists():
                try:
                    socket.gethostbyname(domain_name)
                    domain = domain_name
                    url = f"https://api.securitytrails.com/v1/history/{domain}/dns/mx"
                    headers = {"APIKEY": API.API_KEY}
                    response = requests.get(url, headers=headers)
                    if response.status_code == 429:
                        return "API rate limit exceeded or API credit is expired"
                    if response.status_code == 403:
                        return "API key is invalid" 
                    mx_records = response.json()["records"]
                    if  mx_records :
                        try:
                            first_seen = mx_records[0].get('first_seen')
                            if not first_seen:
                                return "API credit is expired"
                        except:
                                pass
                        domain = Domain.objects.create(name=domain_name)
                        first_seen = mx_records[0]['first_seen']
                        month = datetime.datetime.strptime(first_seen, '%Y-%m-%d').strftime('%b')
                        First_time = True
                        for mx in mx_records:
                            if First_time:
                                mx_record_curr = MXRecordcurrent.objects.create(                
                                    domain=domain,
                                    first_seen=mx['first_seen'],
                                    last_seen=mx['last_seen'],
                                    organizations=', '.join(mx['organizations']),
                                    country=country,
                                    state=state,
                                    selected_month=month
                                )
                            mx_record = MXRecordAll.objects.create(
                                domain=domain,
                                first_seen=mx['first_seen'],
                                last_seen=mx['last_seen'],
                                organizations=', '.join(mx['organizations']),
                                country=country,
                                state=state,
                                selected_month=month
                            )
                            for value in mx['values']:
                                if First_time:
                                    MailServercurrent.objects.create(
                                        current_mx=mx_record_curr,
                                        current_host=value['host']
                                    )
                                MailServerHistorical.objects.create(mx_record=mx_record, host=value['host'])
                            First_time = False
                        ANS="Sucess for {domain_name}, sucessfully stored data to database"
                        data.s_no = -3
                        data.save()
                    else:
                        ANS=f"MX RECORD NOT FOUND FOR {domain_name} as it is live domain"
                        data.s_no = -2
                        data.save()
                except socket.gaierror:
                    ANS=f"Invalid Domain Name{domain_name}"
                    data.s_no = -1
                    data.save()
    except Exception as e:
        ANS=f"Error: {e}"
    return ANS


'''go to tempcsv/MX_RECORD
then start worker first as below  '''
#celery -A MX_RECORD  worker --loglevel=info

'''Then start beat as below '''
#celery -A MX_RECORD  beat --loglevel=info






