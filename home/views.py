from django.shortcuts import render,redirect
from home.custom_decorator import role_required_decorator
# from django.contrib.auth.models import User,auth

from home.models import *

# importing password encryptor
from django.contrib.auth.hashers import make_password, check_password

# importing django login athentications
from django.contrib.auth import authenticate, login, logout

# /////// for login purpose //////////////
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator # pagination purpose

from django.db.models import Q # this is for multiple queryset conditions

# Create your views here.


def index(request):
    # user already logged in area (case 1)
    if request.user.is_authenticated: 
        print(request.user,'User already logged in')

        if(request.user.role =='admin'):
            print('admin is already logged in')
            return redirect('dashboard')

        elif(request.user.role =='driver'):
            print('driver is already logged in')
            return redirect('add_trip')

    else:        
        return render(request,'home/index.html')


def signup(request):

    # user already logged in area (case 1)
    if request.user.is_authenticated: 
        print(request.user,'User already logged in')

        if(request.user.role =='admin'):
            print('admin is already logged in')
            return redirect('dashboard')

        elif(request.user.role =='driver'):
            print('driver is already logged in')
            return redirect('add_trip') 

    else:

        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            pswd1 = request.POST.get('pswd1')
            pswd2 = request.POST.get('pswd2')
            role = request.POST.get('role')
            # address = request.POST.get('address')
            # phone = request.POST.get('phone')
            # license_no = request.POST.get('license_no')
            # age = request.POST.get('age')

            print(name)
            print(email)
            print(pswd1)
            print(pswd2)
            print(role)


            if(name=='' or email== '' or pswd1=='' or pswd2==''):
                print('No value')
                context={'static_name':name,'static_mail':email,'user_error':'Please enter valid info...'}
                return render(request,'home/index.html',context)

            elif(len(pswd1)<6):
                print('Password length too short.')
                context={'static_name':name,'static_mail':email,'user_error':'Password length is too short. Require a minimum password length of 6–10 characters.'}
                return render(request,'home/index.html',context)

            elif(not pswd1==pswd2):
                print('Password Missmatch')
                context={'static_name':name,'static_mail':email,'user_error':'password Missmatch'}
                return render(request,'home/index.html',context)

            elif User.objects.filter(username=email).exists():
                print('User already exist View')
                context={'static_name':name,'static_mail':email,'user_error':'Email already exist...'}
                return render(request,'home/index.html',context)

            else:

                #making password encryption for login purpose
                passEncrypted = make_password(pswd1)

                User_db=User.objects.create(
                    username=email,
                    password=passEncrypted,
                    role=role,
                )

                Driver.objects.create(
                    user_id=User_db,
                    email=email,
                    name=name,
                )
                print('User_db and Driver_db Created')

                return render(request,'home/index.html',{'reg_success': 'Successfully registered, Please login'})
            


        return render(request,'home/index.html')



def loginpage(request):

    # user already logged in area (case 1)
    if request.user.is_authenticated: 
        print(request.user,'User already logged in')

        if(request.user.role =='admin'):
            print('admin is already logged in')
            return redirect('dashboard')

        elif(request.user.role =='driver'):
            print('driver is already logged in')
            return redirect('add_trip') 

    else:
        if request.method == 'POST':
            email = request.POST.get('email')
            pswd = request.POST.get('pswd')

            print(email)
            print(pswd)


            if(email== '' or pswd==''):
                print('No value')
                context={'static_mail':email,'user_error':'Please enter valid info...'}
                return render(request,'home/index.html',context)

            else:

                user =authenticate(request, username=email, password=pswd) # check the user is valid
                print(user)

                if user is not None:
                    login(request, user) #login is hold uservalue(request&user), and added to django_section database
                    print(type(user),user)
                    print('User Login succesfull')

                    # admin login condition
                    if(request.user.role == 'admin'):
                        print('admin is logged in')
                        return redirect('dashboard') 

                    # driver login condition
                    elif(request.user.role =='driver'):
                        print('driver is logged in')
                        return redirect('add_trip')   

                else:
                    print(user,'user')
                    print('login failed')
                    context={'static_mail':email,'user_error':'Invalid Email & Password'}
                    return render(request,'home/index.html',context)

        
        return render(request,'home/index.html')




def logoutpage(request):
    logout(request)
    return redirect('/')



# /////////////////////////////////////////////////////////////////////////////////////////////////////
# driver area
import base64
import random
from django.core.files.base import ContentFile

@login_required(login_url="signup")
@role_required_decorator(allowed_roles=['driver'])
def add_trip(request):

    already_tripExist=Trip_details.objects.filter(driver_id=request.user.id,status='pending').count()
    print(already_tripExist)

    if Trip_details.objects.filter(driver_id=request.user.id,status='pending').exists():
        trip_details_db=Trip_details.objects.get(driver_id=request.user.id,status='pending')

        print('Trip_exist')

        context={'already_tripExist':already_tripExist,'trip_details_db':trip_details_db}
        return render(request,'driver/add_trip.html',context)
    
    elif request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        driver_name = request.POST.get('driver_name')
        guest_name = request.POST.get('guest_name')
        # guest_address = request.POST.get('guest_address')
        start_date = request.POST.get('start_date')
        start_time = request.POST.get('start_time')
        start_km = request.POST.get('start_km')
        vehicle = request.POST.get('vehicle')
        vehicle_number = request.POST.get('vehicle_number')
        reporting_address = request.POST.get('reporting_address')
        driver_signature = request.POST.get('driver_signature')

        # base64-url converted into png file format- start 
        format, imgstr = driver_signature.split(';base64,')
        ext = format.split('/')[-1]

        number = random.randint(1000,9999)
        saver_name=str(request.user.id)+'_signature_'+str(number)

        print(saver_name)
        base64P_png = ContentFile(base64.b64decode(imgstr), name=saver_name + '.' + ext)
        # base64-url converted into png file format- end

        Trip_details.objects.create(

            driver_id=Driver.objects.get(user_id=request.user.id),
            booking_id=booking_id,
            driver_name=driver_name,
            guest_name=guest_name,
            # address=guest_address,
            start_date=start_date,
            start_time=start_time,
            start_km=start_km,
            vehicle=vehicle,
            vehicle_number=vehicle_number,
            reporting_address=reporting_address,
            driver_signature=base64P_png

        )
        print('New trip created')

    context={'already_tripExist':already_tripExist}
    return render(request,'driver/add_trip.html',context)

# add_trip sub view
@login_required(login_url="signup")
@role_required_decorator(allowed_roles=['driver'])
def add_route(request,pk):

    route_db=route.objects.filter(driver_id=request.user.id,trip_id=pk)

    if request.method == 'POST':
        route_address = request.POST.get('route_address')

        print(route_address)

        if route.objects.filter(driver_id=request.user.id,trip_id=pk,route__contains=route_address).exists():
            print('Route location already exist')
            context={'route_db':route_db,'pk':pk,'alreadyExist':'Route location already exist'}
            return render(request,'driver/add_route.html',context)

        else:
            route.objects.create(
                driver_id=request.user.driver,
                trip_id=Trip_details.objects.get(id=pk),
                route=route_address
            )
            print('route saved')

    
   

    context={'route_db':route_db,'pk':pk}
    return render(request,'driver/add_route.html',context)


# @login_required(login_url="signup")
# @role_required_decorator(allowed_roles=['driver'])
# def recent_triplist(request):
#     trip_details_db=Trip_details.objects.filter(status='pending',driver_id=request.user.id)

#     context={'trip_details_db':trip_details_db}
#     return render(request,'driver/recent_triplist.html',context)




# add_trip sub view
# from datetime import datetime
# import datetime as dt

from datetime import date, time

from datetime import datetime, timedelta
import datetime as dt

@login_required(login_url="signup")
@role_required_decorator(allowed_roles=['driver'])
def recent_trip(request,pk):

    if Trip_details.objects.filter(id=pk,status='pending').exists():
        print('exist')
        trip_details_db=Trip_details.objects.get(id=pk,status='pending')
        # first_date= datetime.strftime(trip_details_db.start_date, '%d-%m-%Y')

        # passing time-object to string - for total time calculation purpose(calculated with javascript)
        stime=time.strftime(trip_details_db.start_time,'%H:%M') #converting time-object to string
        print(stime,type(stime),'stime')

        sdate=datetime.strftime(trip_details_db.start_date, '%Y-%m-%d') # converting date-object to string

        # sdate=datetime.strftime(trip_details_db.start_date, '%Y-%m-%d')
        # print(sdate)
        # slist=[]
        # for x in sdate.split('-'):
        #     slist.append(int(x))
        # print(slist)

        if request.method == 'POST':
            # start_date = request.POST.get('start_date')
            # start_time = request.POST.get('start_time')
            # start_km = request.POST.get('start_km')

            end_date = request.POST.get('end_date')
            end_time = request.POST.get('end_time')
            total_time = request.POST.get('total_time')# total_time is calculated by javascript from 'html form'
            end_km = request.POST.get('end_km')
            releasing_address = request.POST.get('releasing_address')
            remark = request.POST.get('remark')
            guest_signature = request.POST.get('guest_signature')

            print(total_time,'???????????????????????? total_time ??????????????????????')

            # total_days = request.POST.get('total_days')
            # total_time = request.POST.get('total_time')
            # total_km = request.POST.get('total_km')

            # print(start_date)
            print(trip_details_db.start_date,'start_date')
            print(trip_details_db.start_time,'start_time')
            print(trip_details_db.start_km,'start_km')

            print(end_date,'end_date',type(end_date))
            # print(end_time,'end_time')
            print(end_km,'end_km')
            print(type(trip_details_db.start_date),trip_details_db.start_date,'date---------------')
            print(type(trip_details_db.start_time),trip_details_db.start_time,'time-----------------')



            # Total_date calculation area using python ///////////////////////////////////////
            sdate=datetime.strftime(trip_details_db.start_date, '%Y-%m-%d') # converting date-object to string
            print(sdate,type(sdate))
            slist=[]
            for x in sdate.split('-'):
                slist.append(int(x))
            print(slist,'slist')
            
            elist=[]
            for y in end_date.split('-'):
                elist.append(int(y))
            print(elist,'elist')


            start_date = date(slist[0],slist[1],slist[2])
            end_date = date(elist[0],elist[1],elist[2])

            # start_date = date(2022, 6, 17)
            # end_date = date(2022, 6, 19)

            total_days = end_date - start_date
            print(total_days.days,'total_daysssssssssssssssssssss')
            # /////////////////////////////////////////////////////////////////////////////

            # Total_km calculation area using python ///////////////////////////////////////
            total_km = int(end_km) - int(trip_details_db.start_km)
            print(total_km,'km')
            # //////////////////////////////////////////////////////////////////////////////

            # base64-url converted into png file format- start 
            format, imgstr = guest_signature.split(';base64,')
            ext = format.split('/')[-1]

            number = random.randint(1000,9999)
            saver_name='guest_signature_'+str(number)

            print(saver_name)
            base64P_png = ContentFile(base64.b64decode(imgstr), name=saver_name + '.' + ext)
            # base64-url converted into png file format- end

            trip_details_db.end_date=end_date
            trip_details_db.end_time=end_time
            trip_details_db.end_km=end_km
            trip_details_db.remark=remark
            trip_details_db.releasing_address=releasing_address
            trip_details_db.guest_signature=base64P_png
            trip_details_db.total_time=total_time
            trip_details_db.total_days=total_days
            trip_details_db.total_km=total_km
            trip_details_db.status='completed'
            trip_details_db.save()
            print('trip_details_db updated')
            return redirect('/')
            
        context={'trip_details_db':trip_details_db,'pk':pk,'sdate':sdate,'stime':stime}
        return render(request,'driver/recent_trip.html',context)

    else:
        print('not exist')
        return redirect('/')
    

# //////////////////////////////////////////////////////////////////////////////////////

# ///////////////////////////////////////////////////////////////////////////////////////
# admin area
@login_required(login_url="signup")
@role_required_decorator(allowed_roles=['admin'])
def dashboard(request):
    driver_count=Driver.objects.count()
    trip_count=Trip_details.objects.all()

    context={'driver_count':driver_count,
    'pending':trip_count.filter(status="pending").count(),
    'completed':trip_count.filter(status="completed").count()
    }
    return render(request,'admin/dashboard.html',context)

    
@login_required(login_url="signup")
@role_required_decorator(allowed_roles=['admin'])
def driver_list(request):
    driver_db=Driver.objects.all()

    context={'driver_db':driver_db}
    return render(request,'admin/driver_list.html',context)

@login_required(login_url="signup")
@role_required_decorator(allowed_roles=['admin'])
def trip_list(request):


    # pagination search purpose for pending-trips 
    if 'search_key_pending' in request.GET:
            
        search_key_pending = request.GET['search_key_pending']
        print(search_key_pending)

        # search key null
        if search_key_pending == '':
            print('search_key_pending empty')
            trip_details_pending=Trip_details.objects.filter(status='pending')

            # Trip_pending pagination-1
            page_pending=Paginator(trip_details_pending, 5)
            page_list_pending=request.GET.get('page_pending')
            page_pending=page_pending.get_page(page_list_pending)

            context={'pending':page_pending,'required_pending':'required_pending'}
            return render(request,'admin/trip_list.html',context)

        # search key not found
        elif Trip_details.objects.filter(
                Q(status='pending',booking_id__icontains=search_key_pending)|
                Q(status='pending',driver_name__icontains=search_key_pending)|
                Q(status='pending',guest_name__icontains=search_key_pending)|
                Q(status='pending',address__icontains=search_key_pending)|
                Q(status='pending',vehicle__icontains=search_key_pending)|
                Q(status='pending',vehicle_number__icontains=search_key_pending)|
                Q(status='pending',reporting_address__icontains=search_key_pending)|
                Q(status='pending',releasing_address__icontains=search_key_pending)|
                Q(status='pending',start_date__icontains=search_key_pending)|
                Q(status='pending',end_date__icontains=search_key_pending)
               
            ).count() == 0:

            print('not found- pending ')
            context={'not_found_pending':'not_found_pending','search_key_pending':search_key_pending}
            return render(request,'admin/trip_list.html',context)

        # search key avalilable
        else:
            print('search key avalilable- pending')
            trip_details_pending=Trip_details.objects.filter(
                Q(status='pending',booking_id__icontains=search_key_pending)|
                Q(status='pending',driver_name__icontains=search_key_pending)|
                Q(status='pending',guest_name__icontains=search_key_pending)|
                Q(status='pending',address__icontains=search_key_pending)|
                Q(status='pending',vehicle__icontains=search_key_pending)|
                Q(status='pending',vehicle_number__icontains=search_key_pending)|
                Q(status='pending',reporting_address__icontains=search_key_pending)|
                Q(status='pending',releasing_address__icontains=search_key_pending)|
                Q(status='pending',start_date__icontains=search_key_pending)|
                Q(status='pending',end_date__icontains=search_key_pending)
               
            )

            # Trip_pending pagination-1
            page_pending=Paginator(trip_details_pending, 5)
            page_list_pending=request.GET.get('page_pending')
            page_pending=page_pending.get_page(page_list_pending)

            

            context={'pending':page_pending,'search_key_pending':search_key_pending}
            return render(request,'admin/trip_list.html',context)

    elif 'search_key_completed' in request.GET:
            
        search_key_completed = request.GET['search_key_completed']
        print(search_key_completed)

        # search key null
        if search_key_completed == '':
            print('search_key_completed empty')
            trip_details_ended=Trip_details.objects.filter(status='completed')

            # Trip_completed pagination-2
            page_completed=Paginator(trip_details_ended, 1)
            page_list_completed=request.GET.get('page_completed')
            page_completed=page_completed.get_page(page_list_completed)

            context={'completed':page_completed,'required_completed':'required_completed'}
            return render(request,'admin/trip_list.html',context)

        # search key not found
        elif Trip_details.objects.filter(
                Q(status='completed',booking_id__icontains=search_key_completed)|
                Q(status='completed',driver_name__icontains=search_key_completed)|
                Q(status='completed',guest_name__icontains=search_key_completed)|
                Q(status='completed',address__icontains=search_key_completed)|
                Q(status='completed',vehicle__icontains=search_key_completed)|
                Q(status='completed',vehicle_number__icontains=search_key_completed)|
                Q(status='completed',reporting_address__icontains=search_key_completed)|
                Q(status='completed',releasing_address__icontains=search_key_completed)|
                Q(status='completed',start_date__icontains=search_key_completed)|
                Q(status='completed',end_date__icontains=search_key_completed)
               
            ).count() == 0:

            print('not found- completed ')
            context={'not_found_completed':'not_found_completed','search_key_completed':search_key_completed}
            return render(request,'admin/trip_list.html',context)

        # search key avalilable
        else:
            print('search key avalilable')
            trip_details_ended=Trip_details.objects.filter(
                Q(status='completed',booking_id__icontains=search_key_completed)|
                Q(status='completed',driver_name__icontains=search_key_completed)|
                Q(status='completed',guest_name__icontains=search_key_completed)|
                Q(status='completed',address__icontains=search_key_completed)|
                Q(status='completed',vehicle__icontains=search_key_completed)|
                Q(status='completed',vehicle_number__icontains=search_key_completed)|
                Q(status='completed',reporting_address__icontains=search_key_completed)|
                Q(status='completed',releasing_address__icontains=search_key_completed)|
                Q(status='completed',start_date__icontains=search_key_completed)|
                Q(status='completed',end_date__icontains=search_key_completed)
            )

             # Trip_completed pagination-2
            page_completed=Paginator(trip_details_ended, 1)
            page_list_completed=request.GET.get('page_completed')
            page_completed=page_completed.get_page(page_list_completed)

            

            context={'completed':page_completed,'search_key_completed':search_key_completed}
            return render(request,'admin/trip_list.html',context)

    else:



        trip_details_pending=Trip_details.objects.filter(status='pending')
        trip_details_ended=Trip_details.objects.filter(status='completed')

        # Trip_pending pagination-1
        page_pending=Paginator(trip_details_pending, 5)
        page_list_pending=request.GET.get('page_pending')
        page_pending=page_pending.get_page(page_list_pending)

        # Trip_completed pagination-2
        page_completed=Paginator(trip_details_ended, 1)
        page_list_completed=request.GET.get('page_completed')
        page_completed=page_completed.get_page(page_list_completed)
        
        context={'pending':page_pending,'completed':page_completed}
        return render(request,'admin/trip_list.html',context)



@login_required(login_url="signup")
@role_required_decorator(allowed_roles=['admin'])
def dutyslip(request,pk):
    if Trip_details.objects.filter(id=pk,status='completed').exists():
        trip_details_db=Trip_details.objects.get(id=pk,status='completed')

        route_db=route.objects.filter(trip_id=pk)

        context={'trip_details_db':trip_details_db,'route_db':route_db}
        return render(request,'admin/dutyslip.html',context)

    else:
        return redirect('/')

# ///////////////////////////////////////////////////////////////////////////////////////