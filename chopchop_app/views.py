# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from chopchop_app.models import *
from chopchop_app.forms import *

from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt

from django.utils import timezone
from datetime import timedelta

from datetime import datetime as dt
from collections import Counter
import datetime

from django.shortcuts import render, redirect, get_object_or_404



# For Navigation - Return HTML file , Refer to urls.py

# Home - redirect to demo-seat-map page
def home(request):
    context = {}
    return render(request, 'demo_seatmap.html', context)

# Dashboard - redirect to dashbord for presentation
def dashboard(request):
    context = {}
    return render(request, 'dashboard.html', context)


# Booking Method
# Please note that we decide to pivot this part, thus this is a working method

def addTable(request):
    context = {}

    if request.method == 'POST':
        form = TableForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/home')
        else:

            context['errors'] = "Invalid input"
            context['all_booking'] = Booking.objects.all()
            context['form1'] = TableForm()
            return render(request, 'booking-home.html', context)
    else:
        return redirect('/booking-home.html')


def bookingPage(request):
    context = {}
    context['table_option'] = Table.objects.all()
    return render(request, 'add_booking.html', context)


def addBooking(request):
    context = {}
    errors = []
    # allbooking = Booking.objects.all()

    user_name = request.POST['user_name']
    phone = request.POST['phone_num']
    table_i = request.POST['table_i']
    date = request.POST['date']
    start_t = request.POST['start_time']
    end_t = request.POST['end_time']

    date_dt = dt.strptime(date, '%m/%d/%Y')
    start_t_dt = dt.strptime(start_t, '%I:%M %p')
    end_t_dt = dt.strptime(end_t, '%I:%M %p')

    start_dt = dt.combine(date_dt, start_t_dt.time())
    end_dt = dt.combine(date_dt, end_t_dt.time())

    table_item = Table.objects.get(table_id=table_i)

    if start_t >= end_t:
        errors.append('Please choose new time.')
    else:
        new_booking = Booking.objects.create(name=user_name, phone_number=phone, table=table_item, start_time=start_dt,
                                             end_time=end_dt)

    context['errors'] = errors

    return render(request, 'add_booking.html', context)


#---------------------------------- SENSOR VISIBILITY DEMO  -----------------------------------
# Functional Prototype submitted on the video


#GetChairStatus Method
#the method support ajax request from web client
# return : JSON object with all chair status data

def getChairStatus(request):
    context = {}
    chair_status = Chair.objects.all()

    now_ = timezone.now() + timedelta(hours=8)
    sum_duration = 0
    duration_list = []

    chair_data = []
    chair_data.append("{\"chair\":[")
    for chair in chair_status:

        delta_min = ""

        if chair.current_session_time is None :
            delta_min = " "
        else:
            delta_min = timezone.now() + timedelta(hours=8) - chair.current_session_time
            delta_min = round(delta_min.total_seconds()/60,2)

        chair_dic = {
            str("chair_code"): str(chair.chair_code),
            str("status"): str(chair.status),
            str("in_time"): str(chair.current_session_time)[11:16],
            str("duration"): str(delta_min)

        }
        chair_data.append(chair_dic)
        if chair != chair_status.last():
            chair_data.append(",")

    chair_data.append("],\"dashboard\":[")

    chair_session_obj = ChairSession.objects.all()
    for session in chair_session_obj:
        if session.end_time and session.start_time is not None:
            duration_session = session.end_time - session.start_time
            duration_session = round(duration_session.total_seconds()/60,1)
            sum_duration = sum_duration + duration_session
            duration_list.append(duration_session)
        else:
            print "none at" + str(session.id)
            duration_list.append(0)

    cnt = Counter(chair_session_obj.values_list('chair_id',flat=True))
    min_pop_id = cnt.most_common()[-1][0]
    max_pop_id = cnt.most_common(1)[0][0]


    dashboard_dic = {
        str("now"): str(now_)[0:16],
        str("total_person"): str(chair_session_obj.count()),
        str("avg_time"): str(round(sum(duration_list)/len(duration_list), 2)),
        str("max_time"): str(max(duration_list)),
        str("min_time"): str(min([n for n in duration_list  if n >= 1])),
        str("most_pop"): str(max_pop_id),
        str("min_pop"): str(min_pop_id),

    }
    chair_data.append(dashboard_dic)
    chair_data.append("]}")


    return HttpResponse(chair_data, content_type="application/json")


def most_common(lst):
    return max(set(lst), key=lst.count)



# PostChairStatus method
# Receive post request from the four sensors
# The method save chair status to two models - chair , chairSession (refer to models.py)
@csrf_exempt
def postChairStatus(request):
    if request.method == 'POST':
        print(request.POST['chair_code'] + " " + request.POST['status_change'])

        chair_code = request.POST['chair_code']
        input_status = request.POST['status_change']

        chair_obj = Chair.objects.get(chair_code=chair_code)
        db_status = chair_obj.status

        if input_status == 'sit':
            if db_status == 'free':
                # change chair status to sit
                chair_obj.status = 'sit'

                chair_obj.current_session_time = timezone.now() + timedelta(hours=8)

                # record new chair session start time

                new_chair_session = ChairSession.objects.create(chair=chair_obj, start_time= chair_obj.current_session_time)

                print('save'+' session id = '+ str(new_chair_session.id) + ' status change to SIT')

                chair_obj.current_session_id = new_chair_session.id

                chair_obj.save()


            return HttpResponse(status=200)

        elif input_status == 'free':
            if db_status == 'sit':
                # change chair status to free
                chair_obj.status = 'free'
                # update chairsession end time
                chair_session_id = chair_obj.current_session_id

                chair_session_obj= ChairSession.objects.get(id=chair_session_id)

                chair_session_obj.end_time = timezone.now()+ timedelta(hours=8)

                chair_obj.save()
                chair_session_obj.save()

                print('save' + ' session id = ' + str(chair_session_id) + ' status change to FREE')

                return HttpResponse(status=200)
        else:
            print ('not write to db')
            return HttpResponse(status=404)

        return HttpResponse(status=404)
    else:
        return HttpResponse(status=404)

