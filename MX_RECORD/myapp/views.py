
# Create your views here.
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
import pandas as pd
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import UnverifiedData
from django.shortcuts import redirect
import time,csv,re,datetime,requests,socket
from .models import  Domain, MXRecordAll, MailServerHistorical ,MailServercurrent,MXRecordcurrent,Country,State
# from .tasks import test_func
def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('login')

@login_required(login_url='login')
def import_file(request):
    total_number_of_data_tried_to_input = 0
    total_duplicate_found = 0
    total_updated = 0
    dropped  = 0
    
    if request.method == 'POST':
        if 'file' not in request.FILES:
            return render(request, 'import_file.html', {'error': 'No file selected'})
        file = request.FILES['file']
        file_ext = file.name.split('.')[-1]
        if file_ext == 'csv':
            df = pd.read_csv(file)
        elif file_ext == 'xlsx':
            df = pd.read_excel(file)
        else:
            return render(request, 'import_file.html', { 'Invalid file type':' Please upload a CSV or XLSX file.'})
        required_cols = ['S. NO.', 'COMPANY NAME', 'CONTACT PERSON', 'ADD.', 'CITY', 'PIN','COUNTRY', 'STATE','LANDLINE NO.', 'MOBILE NO.', 'EMAIL ID', 'WEBSITE']
        if not all(elem in df.columns.tolist() for elem in required_cols):
            return render(request, 'import_file.html', {'error': 'Invalid file format. The file should have the following row at top: S. NO., COMPANY NAME, CONTACT PERSON, ADD., CITY, PIN, COUNTRY, STATE, LANDLINE NO., MOBILE NO., EMAIL ID, WEBSITE'})
# Create a list of UnverifiedData objects from the rows of the CSV/XLSX file
        total_number_of_data_tried_to_input = len(df)
        df = df.dropna(subset=['WEBSITE'])
        df['WEBSITE'] = df['WEBSITE'].str.strip()

        df.drop_duplicates(subset='WEBSITE', keep='first', inplace=True)
        print("Duplicates removed successfully-------------------")
        print(df['WEBSITE'])

        companies = []
        for index, row in df.iterrows():
            website = row['WEBSITE'] # row['website'] is the website column in the CSV/XLSX file
            website=(re.search(r"(?:https?://)?(?:www\.)?([\w-]+\.[\w.-]+)", str(website)[:254]).group(1)) if re.search(r"(?:https?://)?(?:www\.)?([\w-]+\.[\w.-]+)", str(website)[:254]) else None
            if UnverifiedData.objects.filter(website=website).exists():
                continue
            company = UnverifiedData(
                s_no=row['S. NO.'],
                company_name=str(row['COMPANY NAME'])[:200],
                contact_person=str(row['CONTACT PERSON'])[:100],
                address=str(row['ADD.'])[:254],
                city=str(row['CITY'])[:70],
                pin=str(row['PIN'])[:16],
                country=str(row['COUNTRY'])[:70],
                state=str(row['STATE'])[:70],
                landline_no=str(row['LANDLINE NO.'])[:100],
                mobile_no=str(row['MOBILE NO.'])[:180],
                email_id=str(row['EMAIL ID'])[:254],
                website = (re.search(r"(?:https?://)?(?:www\.)?([\w-]+\.[\w.-]+)", str(website)[:254]).group(1)) if re.search(r"(?:https?://)?(?:www\.)?([\w-]+\.[\w.-]+)", str(website)[:254]) else None
            )
            companies.append(company)
        # print(companies)
        # time.sleep(2334)
        print("INSERTING INTO DATABASE------------------------------------------------")
        # Bulk create the list of UnverifiedData objects in a single query
        dropped = total_number_of_data_tried_to_input -len(df)
        total_duplicate_found = len(df) - len(companies)
        if companies:
            try:
                UnverifiedData.objects.bulk_create(companies)
            except:
                return render(request, 'import_file.html', {'error': 'Another user just updated similar type of data in database. Please  reload the page after some time.'})
            total_updated = len(companies)
            html_table = 'Data imported successfully'
        else:
            total_updated = 0
            html_table = 'All data are duplicates'
        return render(request, 'import_file.html', {
            'success': True,
            'total_number_of_data_tried_to_input': total_number_of_data_tried_to_input,
            'total_duplicate_found': total_duplicate_found,
            'total_updated': total_updated,
            'html_table': html_table,
            'dropped': dropped,
        })
    return render(request, 'import_file.html')

def is_superuser_(user):
    return user.is_superuser
# in home base only superuser and staff can accessso we have to use decorator
def is_superuser_or_staff(user):
    return user.is_superuser or user.is_staff





def LoginPage(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST) 
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_staff or user.is_superuser:
                return redirect('search_results')
            return redirect('import-file')
        else:
            return render(request, 'login.html',{'form': form}) # html file ma jada form pass karna hai toh dictionary mei pass karo
    else:
        # If this is a GET request, render the login.html template
        form = AuthenticationForm(request) 
        return render(request, 'login.html', {'form': form})





def get_states(request, country_name):
    # Get the selected country object
    country = Country.objects.get(country_name=country_name)
    # Get the states of the selected country
    states = State.objects.filter(country=country)
    # Return the states as a JSON response
    return JsonResponse(list(states.values()), safe=False)




from django.http import JsonResponse

def get_dashboard(request):
    total_domain_not_live = UnverifiedData.objects.filter(s_no=-1).count()
    total_domain_live_with_no_MX = UnverifiedData.objects.filter(s_no=-2).count()
    total_amount_of_mx_data = Domain.objects.all().count()
    total_amount_of_new_unverified_data = UnverifiedData.objects.exclude(s_no__in=[-1, -2, -3]).count()

    dashboard_data = {
        'total_domain_not_live': total_domain_not_live,
        'total_domain_live_with_no_MX': total_domain_live_with_no_MX,
        'total_amount_of_mx_data': total_amount_of_mx_data,
        'total_amount_of_new_unverified_data': total_amount_of_new_unverified_data
    }

    return JsonResponse({'dashboard_data': dashboard_data})


def export_dashboard(request):
    print("aayo",request.method,request.GET.get('export'),request.GET.get('selected_query'))
    if request.method == 'GET' and request.GET.get('export') == 'csv' and request.GET.get('selected_query') is not None :
        selected_query = request.GET.get('selected_query')
        if selected_query=="total_amount_of_mx_data":
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{selected_query}.csv"'
            
            writer = csv.writer(response)
            writer.writerow(["Domains Whose MX records was Found"])
            total_amount_of_mx_data=Domain.objects.all()
            for record in total_amount_of_mx_data:
                writer.writerow([record.name])
        else:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{selected_query}.csv"'
            
            writer = csv.writer(response)
            writer.writerow(['Company Name' , 'Contact Person' , 'Address ', 'City ' , 'Pin' ,'Country' ,'State', 'LandLine No','Mobile No','Email Id','Website'])
            records=None

            if selected_query=='total_amount_of_new_unverified_data':
                records=UnverifiedData.objects.exclude(s_no__in=[-1, -2,-3])

            if selected_query=='total_domain_not_live':
                records =UnverifiedData.objects.filter(s_no=-1)


            if selected_query=='total_domain_live_with_no_MX':
                records =UnverifiedData.objects.filter(s_no=-2)

            if records:
                for record in records:
                        writer.writerow([
                        record.company_name,
                        record.contact_person,
                        record.address,
                        record.city,
                        record.pin,
                        record.country,
                        record.state,
                        record.landline_no,
                        record.mobile_no,
                        record.email_id,
                        record.website
                        ])

        return response


# -1 = Domain is not live 
# -2 means that the domain is live but the MX records are not found
# -3 means that the domain is live and MX record are found , Now we don't have to check it again

@user_passes_test(is_superuser_or_staff, login_url='login')
def search_results(request):
    countries = Country.objects.all()
    states = State.objects.all()
    total_domain_not_live = UnverifiedData.objects.filter(s_no=-1).count()
    total_domain_live_with_no_MX= UnverifiedData.objects.filter(s_no=-2).count()
    total_amount_of_mx_data=Domain.objects.all().count()
    total_amount_of_new_unverified_data= UnverifiedData.objects.exclude(s_no__in=[-1, -2,-3]).count()
    dashboard_data={
        'total_domain_not_live':total_domain_not_live,
        'total_domain_live_with_no_MX':total_domain_live_with_no_MX,
        'total_amount_of_mx_data':total_amount_of_mx_data,
        'total_amount_of_new_unverified_data':total_amount_of_new_unverified_data

    }
    # By domain search 
    if request.method=='POST' and request.POST.get('domain') is not None:
        selected_domain=request.POST.get('domain')
        mx_records = MXRecordAll.objects.filter(
            domain__name__iexact=selected_domain, 
        ) 
        
        mail_servers = MailServerHistorical.objects.filter(mx_record__in=mx_records).prefetch_related('mx_record__domain')
        context = {
            'mx_records': mx_records,
            'historical_mail_servers': mail_servers,
        }
        if not mx_records:
            print("no mx records ")
            context = {
                'error_message_domain': f'No data found for Domain: {selected_domain} '
            }
        return render(request, 'search_results.html', {'countries': countries, 'states': states,'context':context,'dashboard_data':dashboard_data})



    # By month search , state and country search 
    if request.method == 'POST' and request.POST.get('month')is not None and request.POST.get('country')is not None and request.POST.get('state')is not None:
        selected_month = request.POST.get('month')
        selected_country = request.POST.get('country')
        selected_state = request.POST.get('state')
        mx_records = MXRecordcurrent.objects.filter(
            selected_month__iexact=selected_month, 
            country__iexact=selected_country, 
            state__iexact=selected_state
        )[:10] 
        mail_servers = MailServercurrent.objects.filter(current_mx__in=mx_records).prefetch_related('current_mx__domain')
        context = { 
            'mx_records': mx_records,
            'mail_servers': mail_servers,
            'selected_month': selected_month,
            'selected_country': selected_country,
            'selected_state': selected_state,
        }
        if not mx_records:
            context = {
                'error_message': f'No data found for COUNTRY: {selected_country} - STATE: {selected_state}- MONTH:{selected_month}'
            }
        return render(request, 'export_file.html', {'context':context})
    

    if request.method == 'GET' and request.GET.get('export') == 'csv' and request.GET.get('selected_month') is not None and request.GET.get('selected_country') is not None and request.GET.get("selected_state") is not None:
        selected_month = request.GET.get('selected_month')
        selected_country= request.GET.get('selected_country')
        selected_state= request.GET.get('selected_state')
        print(selected_country,selected_month,selected_state)
        mx_records = MXRecordcurrent.objects.filter(
            selected_month=selected_month, 
            country=selected_country, 
            state=selected_state
        ) .prefetch_related('current_mail_servers')
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="mx_records_{selected_country}_{selected_state}_{selected_month}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Domain Name' , 'Country' , 'State', 'Month' , 'Mail Server' ,'Organization' ,'First Seen', 'Last Seen'])
        
        for mx_record in mx_records:
            for mail_server in mx_record.current_mail_servers.all():
                writer.writerow([
                    mx_record.domain.name,
                    mx_record.country,
                    mx_record.state,
                    mx_record.selected_month,
                    mail_server.current_host,
                    mx_record.organizations,
                    mx_record.first_seen,
                    mx_record.last_seen,
                ])
        
        return response

    return render(request, 'search_results.html', {'countries': countries, 'states': states,'dashboard_data':dashboard_data})






# try section :::____________________________________


@user_passes_test(is_superuser_, login_url='login')
def delete(request):
    total_domain_not_live = UnverifiedData.objects.filter(s_no=-1).count()
    total_domain_live_with_no_MX= UnverifiedData.objects.filter(s_no=-2).count()
    total_amount_of_mx_data=Domain.objects.all().count()
    total_amount_of_new_unverified_data= UnverifiedData.objects.exclude(s_no__in=[-1, -2,-3]).count()
    dashboard_data={
        'total_domain_not_live':total_domain_not_live,
        'total_domain_live_with_no_MX':total_domain_live_with_no_MX,
        'total_amount_of_mx_data':total_amount_of_mx_data,
        'total_amount_of_new_unverified_data':total_amount_of_new_unverified_data

    }
    return render(request, 'delete.html',{'dashboard_data':dashboard_data})

@user_passes_test(is_superuser_, login_url='login')
def delete_all_unverified_data(request):
    if request.method == 'POST':
        UnverifiedData.objects.all().delete()

        total_domain_not_live = UnverifiedData.objects.filter(s_no=-1).count()
        total_domain_live_with_no_MX= UnverifiedData.objects.filter(s_no=-2).count()
        total_amount_of_mx_data=Domain.objects.all().count()
        total_amount_of_new_unverified_data= UnverifiedData.objects.exclude(s_no__in=[-1, -2,-3]).count()
        dashboard_data={
            'total_domain_not_live':total_domain_not_live,
            'total_domain_live_with_no_MX':total_domain_live_with_no_MX,
            'total_amount_of_mx_data':total_amount_of_mx_data,
            'total_amount_of_new_unverified_data':total_amount_of_new_unverified_data

    }


        return render(request, 'delete.html', {'message': 'All unverified data deleted successfully.','dashboard_data':dashboard_data})

    return render(request, 'delete.html')

@user_passes_test(is_superuser_, login_url='login')
def delete_all_domain_not_live_data(request):
    if request.method == 'POST':
        UnverifiedData.objects.filter(s_no=-1).delete()

        total_domain_not_live = UnverifiedData.objects.filter(s_no=-1).count()
        total_domain_live_with_no_MX= UnverifiedData.objects.filter(s_no=-2).count()
        total_amount_of_mx_data=Domain.objects.all().count()
        total_amount_of_new_unverified_data= UnverifiedData.objects.exclude(s_no__in=[-1, -2,-3]).count()
        dashboard_data={
            'total_domain_not_live':total_domain_not_live,
            'total_domain_live_with_no_MX':total_domain_live_with_no_MX,
            'total_amount_of_mx_data':total_amount_of_mx_data,
            'total_amount_of_new_unverified_data':total_amount_of_new_unverified_data

    }


        return render(request, 'delete.html', {'message': 'All domain not live data deleted successfully from unverified database.','dashboard_data':dashboard_data})

    return render(request, 'delete.html')


@user_passes_test(is_superuser_, login_url='login')
def delete_all_domain_live_no_mx_data(request):
    if request.method == 'POST':
        UnverifiedData.objects.filter(s_no=-2).delete()

        total_domain_not_live = UnverifiedData.objects.filter(s_no=-1).count()
        total_domain_live_with_no_MX= UnverifiedData.objects.filter(s_no=-2).count()
        total_amount_of_mx_data=Domain.objects.all().count()
        total_amount_of_new_unverified_data= UnverifiedData.objects.exclude(s_no__in=[-1, -2,-3]).count()
        dashboard_data={
            'total_domain_not_live':total_domain_not_live,
            'total_domain_live_with_no_MX':total_domain_live_with_no_MX,
            'total_amount_of_mx_data':total_amount_of_mx_data,
            'total_amount_of_new_unverified_data':total_amount_of_new_unverified_data

    }
        return render(request, 'delete.html', {'message': 'All domain live but MX record not found data deleted successfully from unverified database.','dashboard_data':dashboard_data})


    return render(request, 'delete.html')


@user_passes_test(is_superuser_, login_url='login')
def delete_all_verified_data(request):
    if request.method == 'POST':
        # Prompt user confirmation
        confirm = request.POST.get('confirm', False)

        if confirm == 'yes':
            Domain.objects.all().delete()

            total_domain_not_live = UnverifiedData.objects.filter(s_no=-1).count()
            total_domain_live_with_no_MX= UnverifiedData.objects.filter(s_no=-2).count()
            total_amount_of_mx_data=Domain.objects.all().count()
            total_amount_of_new_unverified_data= UnverifiedData.objects.exclude(s_no__in=[-1, -2,-3]).count()
            dashboard_data={
            'total_domain_not_live':total_domain_not_live,
            'total_domain_live_with_no_MX':total_domain_live_with_no_MX,
            'total_amount_of_mx_data':total_amount_of_mx_data,
            'total_amount_of_new_unverified_data':total_amount_of_new_unverified_data

    }


            return render(request, 'delete.html', {'message': 'All verified data deleted successfully from domain database.','dashboard_data':dashboard_data})
        else:
            return render(request, 'delete.html', {'message': 'Deletion of verified data canceled.','dashboard_data':dashboard_data})

    return render(request, 'delete.html')


# _____________________remake form section _____________________________________________

