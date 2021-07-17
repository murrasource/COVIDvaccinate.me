from django.shortcuts import render, HttpResponse
from .forms import *
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.contrib.gis.geoip2 import GeoIP2
import requests
from .cloud_tasks import send_task
from itertools import islice
from math import radians, cos, sin, asin, sqrt, ceil
import json
from datetime import datetime as dt

state_options = ['AL','AK','AZ','AR','CA','CO','CT','DE','DC',
                'FL','GA','HI','ID','IL','IN','IA','KS','KY',
                'LA','ME','MD','MA','MI','MN','MS','MO','MT',
                'NE','NV','NH','NJ','NM','NY','NC','ND','OH',
                'OK','OR','PA','RI','SC','SD','TN','TX','UT',
                'VT','VA','WA','WV','WI','WY']

g = GeoIP2('GeoLite2-City.mmdb')

# Calculate circle distance
def haversine(lon1, lat1, lon2, lat2):
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    # Radius of earth in kilometers is 6371
    km = 6371 * c
    mi = km * 0.621371
    return ceil(mi)

# function to get user's IP
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = str(request.META.get('REMOTE_ADDR'))
    return ip

# Function for adding a state's api call to database
def update_database(response, state):
    urls = {'Market 32': 'http://link.statmn.org/Poi',
            'CVS': 'http://link.statmn.org/jpe',
            'Health Mart': 'http://link.statmn.org/oaY',
            'Costco': 'http://link.statmn.org/zsv',
            'Walgreens': 'http://link.statmn.org/Odb',
            "Shaw's": 'http://link.statmn.org/Wf9',
            'Walmart': 'http://link.statmn.org/3gu',
            'Rite Aid': 'http://link.statmn.org/Bhs',
            'Carrs': 'http://link.statmn.org/ujM',
            'Safeway': 'http://link.statmn.org/ukX',
            'Albertsons': 'http://link.statmn.org/zl4',
            'Fred Meyer': 'http://link.statmn.org/nz9',
            'Community (Walgreens)': 'http://link.statmn.org/zx8',
            'Harris Teeter': 'http://link.statmn.org/vcQ',
            'Publix': 'http://link.statmn.org/zvZ',
            'Harveys': 'http://link.statmn.org/UbB',
            'Acme': 'http://link.statmn.org/kn3',
            "Sam's Club": 'http://link.statmn.org/nmF',
            "Smith's": 'http://link.statmn.org/0QI',
            'Hy-Vee': 'http://link.statmn.org/NWw',
            'Market Street': 'http://link.statmn.org/uET',
            'Thrifty White': 'http://link.statmn.org/mRq',
            'Dillons': 'http://link.statmn.org/lT5',
            'The Little Clinic': 'http://link.statmn.org/0YQ',
            'Walgreens Specialty Pharmacy': 'http://link.statmn.org/ZUo',
            'Winn-Dixie': 'http://link.statmn.org/3IS',
            'Jewel-Osco': 'http://link.statmn.org/dOG',
            'Baxter Drug (Walgreens)': 'http://link.statmn.org/hPx',
            'Kroger': 'http://link.statmn.org/bAv',
            'Pay-Less': 'http://link.statmn.org/1SD',
            'Kroger COVID': 'http://link.statmn.org/7DK',
            'Jay C': 'http://link.statmn.org/1FQ',
            'Ellisville Drug (Walgreens)': 'http://link.statmn.org/3GA',
            'Carthage Discount Drug (Walgreens)': 'http://link.statmn.org/8Hm',
            'Linn Drug (Walgreens)': 'http://link.statmn.org/fJM',
            'Vons': 'http://link.statmn.org/5K7',
            'Pharmaca': 'http://link.statmn.org/dLs',
            "Baker's": 'http://link.statmn.org/LZb',
            'Albertsons Market': 'http://link.statmn.org/kX4',
            'Duane Reade': 'http://link.statmn.org/8C6',
            'Murphy Drug (Walgreens)': 'http://link.statmn.org/wVo',
            'Gerbes': 'http://link.statmn.org/dBG',
            'Star Market': 'http://link.statmn.org/5NC',
            'Weis': 'http://link.statmn.org/7Mj',
            'Seymour Pharmacy (Walgreens)': 'http://link.statmn.org/81Q',
            'Ferguson Drug (Walgreens)': 'http://link.statmn.org/T0v',
            'Ava Drug (Walgreens)': 'http://link.statmn.org/n2r',
            'Forbes Pharmacy (Walgreens)': 'http://link.statmn.org/p9n',
            'Mansfield Drug (Walgreens)': 'http://link.statmn.org/n3g',
            'Strauser Drug (Walgreens)': 'http://link.statmn.org/n3g',
            'Cox Drug (Walgreens)': 'http://link.statmn.org/n3g',
            'Wegmans': 'http://link.statmn.org/vwp1',
            "Ken's Discount (Walgreens)": 'http://link.statmn.org/n3g',
            'Broadwater Drugs (Walgreens)': 'http://link.statmn.org/n3g',
            'AllianceRx (Walgreens)': 'http://link.statmn.org/n3g',
            'City Market': 'http://link.statmn.org/kwoM',
            'Rite Aid (Walgreens)': 'http://link.statmn.org/n3g',
            'QFC': 'http://link.statmn.org/ewiE',
            'Fresco y Más':'http://link.statmn.org/UwuT',
            'King Soopers': 'http://link.statmn.org/gwy2',
            'Metro Market': 'http://link.statmn.org/XwtW',
            "Pick 'n Save": 'http://link.statmn.org/XwrF',
            'H-E-B Pharmacy': 'http://link.statmn.org/2weH',
            'Parkway Drugs (Walgreens)': 'http://link.statmn.org/n3g',
            'C&M (Walgreens)': 'http://link.statmn.org/n3g',
            'Waldron Drug (Walgreens)': 'http://link.statmn.org/n3g',
            "Fry's": 'http://link.statmn.org/1wwX',
            'Jim, Myers (Walgreens)': 'http://link.statmn.org/n3g',
            'Centura Health: Drive-Up Event': 'http://link.statmn.org/Bwqc',
            'PrepMod': 'http://link.statmn.org/36o',
            'Haggen': 'http://link.statmn.org/35p',
            'Market Bistro': 'http://link.statmn.org/Poi',
            "Mariano's": 'http://link.statmn.org/47b',
            'Denver Ball Arena': 'http://link.statmn.org/R4H',
            'United Supermarkets': 'http://link.statmn.org/zl4',
            'Tom Thumb': 'http://link.statmn.org/zl4',
            'Amigos': 'http://link.statmn.org/zl4',
            'Randalls': 'http://link.statmn.org/zl4',
            'Pioneer (Walgreens)': 'http://link.statmn.org/n3g',
            'Pavilions': 'http://link.statmn.org/zl4',
            'Ralphs': 'http://link.statmn.org/V8X',
            'Dominguez (Walgreens)': 'http://link.statmn.org/n3g',
            "Pak 'n Save": 'http://link.statmn.org/zl4'}
    all_locations = response.json()['features']
    Location.objects.filter(state=state).delete()
    for location in all_locations:
        lat = location['geometry']['coordinates'][1]
        lng = location['geometry']['coordinates'][0]
        if lat is None and lng is None:
            continue
        else:
            prop = location['properties']
            name = prop['provider_brand_name']
            if name in urls.keys():
                url = urls[name]
            else:
                url = prop['url']
            addr = f"{prop['city']}, {state}"
            post = prop['postal_code']
            if prop['appointments_available'] is None:
                avail = False
            else:
                avail = prop['appointments_available']
            Location.objects.create(name=name, postal=post, address=addr, url=url, availabilities=avail, state=state, latitude=lat, longitude=lng)

# Funciton for sending morning email list
def send_email(user):
    plaintext = get_template('email.txt')
    htmly = get_template('email.html')
    today = dt.today()
    date = f'{str(today.month).zfill(2)}{str(today.day).zfill(2)}{str(today.year)}'
    link = f'https://statmn.org/matomo/matomo/matomo.php?idsite=1&rec=1&bots=1&url=https%3A%2F%2Fstatmn.org%2Femail-opened%2F{user.email}&action_name=Email%20opened&_rcn={date}&_rck=vaccinenotification'
    places = Location.objects.filter(availabilities=True, state=user.state)
    # Judge distances within state
    locations = []
    for place in places:
        distance = haversine(user.longitude, user.latitude, place.longitude, place.latitude)
        locations.append({'model': place, 'distance': distance})
    # Order and pick top 10
    total = len(locations)
    if total > 8:
        end = 9
    else:
        end = total
    locations = sorted(locations, key=lambda k: k['distance'])[0:end]

    subject = 'COVIDvaccinate.me Update'
    text_content = plaintext.render({'locations': locations, 'current': user.zipcode})
    html_content = htmly.render({'locations': locations, 'current': user.zipcode, 'link': link})
    msg = EmailMultiAlternatives(subject=subject, body=text_content, to=[user.email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

# Offline view
def offline(request):
    return render(request, 'offline.html')

# Landing page
def home(request):
    return render(request, 'index.html')

# Registration
def signup(request):
    if request.method == "POST":
        form = SubscribeForm(request.POST)
        if form.is_valid():
            # Only create new object if email does not yet exist in database
            Subscriber.objects.get_or_create(email=form.cleaned_data['email'],
                                            state=form.cleaned_data['state'],
                                            zipcode=form.cleaned_data['zipcode'],
                                            latitude=Geocode.objects.get(zipcode=form.cleaned_data['zipcode']).latitude,
                                            longitude=Geocode.objects.get(zipcode=form.cleaned_data['zipcode']).longitude)
            # Give on-screen success update
            messages.success(request, "Please check your email (including your spam folder), as you should receive a verification email. If you did not receive an email, make sure your email address is correct.")
            # Send a confirmation email
            email = form.cleaned_data['email']
            plaintext = get_template('success.txt')
            htmly = get_template('success.html')
            subject = 'COVIDvaccinate.me Registration'
            text_content = plaintext.render({})
            html_content = htmly.render({})
            msg = EmailMultiAlternatives(subject=subject, body=text_content, to=[email])
            msg.attach_alternative(html_content, "text/html")
            try:
                msg.send()
            except:
                messages.error(request, "Please try again.")
        else:
            messages.error(request, "Please try again.")
    else:
        form = SubscribeForm()
    return render(request, 'signup.html', {'form': form})

# Unsubscribe Email
def unsubscribe(request):
    if request.method == "POST":
        form = UnsubscribeForm(request.POST)
        if form.is_valid():
            subscriber = Subscriber.objects.filter(email=form.cleaned_data['email'])
            # Check to see if email is registered to prevent breaking issues
            if subscriber.exists():
                subscriber.delete()
                messages.success(request, "You've successfully unsubscribed.")
            else:
                messages.error(request, "There is no subscription associated with the given email.")
        else:
            messages.error(request, "Please try again.")
    else:
        form = UnsubscribeForm()
    return render(request, 'unsubscribe.html', {'form': form})

# Dashboard
def dashboard(request):   
    # Get user's ip address and resolve location from that using GeoIP2
    try:
        user_ip = get_client_ip(request)
        zipcode = int(g.city(user_ip)['postal_code'])
        state = g.city(user_ip)['region']
        obj = Geocode.objects.get(zipcode=zipcode)
        coord = [obj.latitude, obj.longitude]
    except:
    # Default location is 55105
        obj = Geocode.objects.get(zipcode=55105)
        state = 'MN'
        coord = [obj.latitude, obj.longitude]
    # Narrow down list first
    places = Location.objects.filter(availabilities=True, state=state)
    # Judge distances within state
    locations = []
    for place in places:
        distance = haversine(coord[1], coord[0], place.longitude, place.latitude)
        locations.append({'model': place, 'distance': distance})
    # Order and pick top 10
    total = len(locations)
    if total > 8:
        end = 9
    else:
        end = total
    locations = sorted(locations, key=lambda k: k['distance'])[0:end]
    return render(request, 'dashboard.html', {'locations': locations, 'current': obj.zipcode})

# Trigger Updating Task
def begin_update(request):
    for state in state_options:
        dictionary = {"state":state}
        payload = json.dumps(dictionary)
        send_task(url='/update9923/', http_method='POST', payload=payload)
    return HttpResponse('Updating has begun!')

# Trigger Emailing Task
def begin_emailing(request):
    for user in Subscriber.objects.all():
        uid = str(user.id)
        dictionary = {"id":uid}
        payload = json.dumps(dictionary)
        send_task(url='/email4497/', http_method='POST', payload=payload)
    return HttpResponse('Emailing has begun!')

# Updating Task
@csrf_exempt
def update(request):
    # Get payload
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    state = body['state']
    # Collect state data
    data = requests.get(f'https://www.vaccinespotter.org/api/v0/states/{state}.json')
    # Update Database
    update_database(data, state)
    # Success message
    return HttpResponse('Update Has Been Completed')

# Emailing Task
@csrf_exempt
def email(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    id_client = int(float(body['id']))
    subscriber = Subscriber.objects.get(id=id_client)
    try:
        send_email(subscriber)
        print(f'Sent to {subscriber.email}')
    except:
        subject = 'Email Failure'
        msg = EmailMultiAlternatives(subject=subject, body=f'Failed to send to {subscriber.email}', to=['austin@statmn.org'])
        msg.send()
        print(f'FAILED - {subscriber.email}')
    return HttpResponse('Email list has been sent.')