from .models import UserProfile, DriverProfile, SponsorList, SponsorUserProfile, PointReason
from .forms import RegisterUserForm, UserProfileForm, DriverProfileForm, AssignSponsorForm, PointReasonForm, EmailForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from report.models import login_log
from django.core.mail import send_mail
from django.conf import settings

def login_user(request):
    if request.user.is_authenticated:
        return redirect('/about')
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            login_attempt = login_log(username=username, login_success="True")
            login_attempt.save()
            return redirect('about/')
        else:
            messages.success(request, ("There was an error logging in, please try again."))
            login_attempt = login_log(username=username, login_success="False")
            login_attempt.save()
            return redirect('/')
    else:
        return render(request, 'registration/login.html', {})

def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, ("You were successfully logged out."))       
    else:
        messages.success(request, ("You are not currently logged in to an account."))   
    return redirect('/')

def register_user(request):
    if request.user.is_authenticated:
        return redirect('/about')
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            try:
                driver, created = DriverProfile.objects.get_or_create(user=request.user)
            except DriverProfile.DoesNotExist:
                driver = None
            driver.first_name = form.cleaned_data['first_name']
            driver.last_name = form.cleaned_data['last_name']
            driver.email = form.cleaned_data['email']
            driver.is_driver = True
            driver.user = request.user
            driver.save()
            login_attempt = login_log(username=username, login_success="True")
            login_attempt.save()
            messages.success(request, ("You were successfully registered."))
            return redirect('/')
    else:
        form = RegisterUserForm()

    return render(request, 'registration/register_user.html', {'form':form,})

def view_profile(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in or register to view your profile")
        return redirect('/')
    try:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None
    if not request.user.is_superuser and not profile.is_sponsor and not profile.is_driver:
        messages.error(request, "There is an error with your account, please contact Team06 at team06.onlydrivers@gmail.com for support.")
        return redirect('/about')
    if profile.is_driver:
        try:
            driver = DriverProfile.objects.get(user=request.user)
        except DriverProfile.DoesNotExist:
            driver = None

        sponsors = driver.sponsors.all()

        return render(request, 'registration/profile.html', {'profile': profile, 'driver': driver, 'sponsors': sponsors})
    elif profile.is_sponsor:
        try:
            sponsor_user, created = SponsorUserProfile.objects.get_or_create(user=request.user)
        except DriverProfile.DoesNotExist:
            sponsor_user = None

        return render(request, 'registration/profile.html', {'profile': profile, 'sponsor_user': sponsor_user})
    else:
        return render(request, 'registration/profile.html', {'profile': profile})

def edit_profile(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to edit your profile.")
        return redirect('/')
    
    try:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None
    if not request.user.is_superuser and not profile.is_sponsor and not profile.is_driver:
        messages.error(request, "There is an error with your account, please contact Team06 at team06.onlydrivers@gmail.com for support.")
        return redirect('/about')

    if profile.is_driver:
        try:
            driver = DriverProfile.objects.get(user=request.user)
        except DriverProfile.DoesNotExist:
            driver = None

        if request.method == 'POST':
            driver_form = DriverProfileForm(request.POST, instance=driver)

            if driver_form.is_valid():
                driver = driver_form.save(commit=False)
                driver.user = request.user
                driver.save()

                messages.success(request, "Profile updated successfully!")
                return redirect('view_profile')
        else:
            driver_form = DriverProfileForm(instance=driver)

        return render(request, 'registration/edit_profile.html', {'driver_form': driver_form, 'driver': driver, 'profile': profile})
    elif profile.is_sponsor:
        try:
            sponsor_user = SponsorUserProfile.objects.get(user=request.user)
        except DriverProfile.DoesNotExist:
            sponsor_user = None

        if request.method == 'POST':
            form = UserProfileForm(request.POST, instance=sponsor_user)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile updated successfully!")
                return redirect('view_profile')
        else:
            form = UserProfileForm(instance=sponsor_user)
        return render(request, 'registration/edit_profile.html', {'profile': profile,'sponsor_user': sponsor_user, 'form': form})
    
    else:
        if request.method == 'POST':
            form = UserProfileForm(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile updated successfully!")
                return redirect('view_profile')
        else:
            form = UserProfileForm(instance=profile)
        return render(request, 'registration/edit_profile.html', {'profile': profile, 'form': form})
    
def driver_list(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to an authorized account to view this page.")
        return redirect('/')
    try:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None
    if not request.user.is_superuser and not profile.is_sponsor and not profile.is_driver:
        messages.error(request, "There is an error with your account, please contact Team06 at team06.onlydrivers@gmail.com for support.")
        return redirect('/about')
    
    if profile.is_sponsor:
        sponsor = SponsorUserProfile.objects.get(user=request.user)
        results = DriverProfile.objects.filter(sponsors__sponsor_name=sponsor.sponsor_name)
        return render(request, 'sponsor_organization/driver_list.html', {'results': results, 'sponsor': sponsor})
    elif request.user.is_superuser:
        results = DriverProfile.objects.all()
        return render(request, 'sponsor_organization/driver_list.html', {'results': results})    
    else:
        messages.error(request, "You do not have the proper permissions to access this page.")
        return redirect('/about')

def view_driver(request, id):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to an authorized account to view this page.")
        return redirect('/')
    try:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None
    if not request.user.is_superuser and not profile.is_sponsor and not profile.is_driver:
        messages.error(request, "There is an error with your account, please contact Team06 at team06.onlydrivers@gmail.com for support.")
        return redirect('/about')
    
    if profile.is_sponsor:
        driver = DriverProfile.objects.get(userprofile_ptr_id=id)
        sponsor = SponsorUserProfile.objects.get(user=request.user)
        s_name = sponsor
        driver_sponsors = driver.sponsors.all()
        for driver_sponsor in driver_sponsors:
            if s_name.sponsor_name == driver_sponsor.sponsor_name:
                return render(request, 'sponsor_organization/view_driver.html', {'driver': driver, 'profile': profile,})
        else:
            messages.error(request, "You do not have the proper permissions to access this page.")
            return redirect('/about')
        
    elif request.user.is_superuser:
        driver = DriverProfile.objects.get(userprofile_ptr_id=id)
        return render(request, 'sponsor_organization/view_driver.html', {'driver': driver,})
    else:
        messages.error(request, "You do not have the proper permissions to access this page.")
        return redirect('/about')
    
def edit_driver(request, id):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to an authorized account to view this page.")
        return redirect('/')
    try:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None
    if not request.user.is_superuser and not profile.is_sponsor and not profile.is_driver:
        messages.error(request, "There is an error with your account, please contact Team06 at team06.onlydrivers@gmail.com for support.")
        return redirect('/about')
    if profile.is_sponsor or request.user.is_superuser:
        try:
            driver = DriverProfile.objects.get(id=id)
        except DriverProfile.DoesNotExist:
            driver = None
        if profile.is_sponsor:
            sponsor = SponsorUserProfile.objects.get(user=request.user)
            s_name = sponsor
            driver_sponsors = driver.sponsors.all()
            for driver_sponsor in driver_sponsors:
                if s_name.sponsor_name == driver_sponsor.sponsor_name:
                    if request.method == 'POST':
                        driver_form = DriverProfileForm(request.POST, instance=driver)

                        if driver_form.is_valid():
                            driver = driver_form.save(commit=False)
                            driver.save()

                            messages.success(request, "Profile updated successfully!")
                            return redirect('/organization/view/driver/'+str(id))
                    else:
                        driver_form = DriverProfileForm(instance=driver)

                    return render(request, 'sponsor_organization/edit_driver.html', {'driver_form': driver_form, 'driver': driver, 'profile': profile})
        else:
            if request.method == 'POST':
                driver_form = DriverProfileForm(request.POST, instance=driver)

                if driver_form.is_valid():
                    driver = driver_form.save(commit=False)
                    driver.save()

                    messages.success(request, "Profile updated successfully!")
                    return redirect('/organization/view/driver/'+str(id))
            else:
                driver_form = DriverProfileForm(instance=driver)

            return render(request, 'sponsor_organization/edit_driver.html', {'driver_form': driver_form, 'driver': driver, 'profile': profile})    
    else:
        messages.error(request, "You do not have the proper permissions to access this page.")
        return redirect('/about')

def add_points(request, id):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to an authorized account to view this page.")
        return redirect('/')
    try:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None
    if not request.user.is_superuser and not profile.is_sponsor and not profile.is_driver:
        messages.error(request, "There is an error with your account, please contact Team06 at team06.onlydrivers@gmail.com for support.")
        return redirect('/about')
    if profile.is_sponsor:
        try:
            driver = DriverProfile.objects.get(id=id)
        except DriverProfile.DoesNotExist:
            driver = None
        try:
            sponsor = SponsorUserProfile.objects.get(user=request.user)
        except SponsorUserProfile.DoesNotExist:
            sponsor = None
        s_name = sponsor
        driver_sponsors = driver.sponsors.all()
        for driver_sponsor in driver_sponsors:
            if s_name.sponsor_name == driver_sponsor.sponsor_name:
                if request.method == 'POST':
                    point_form = PointReasonForm(request.POST)

                    if point_form.is_valid():
                        instance = point_form.save()
                        point_reason, created = PointReason.objects.get_or_create(id=instance.id)
                        point_reason.point_amt = point_form.cleaned_data['point_amt']
                        point_reason.point_reason = point_form.cleaned_data['point_reason']
                        point_reason.sponsor = sponsor
                        point_reason.driver = driver
                        point_reason.save()
                        temp = driver.points
                        if point_reason.is_add:
                            add = point_reason.point_amt
                            temp = temp + add
                            driver.points = temp
                            driver.save()
                            messages.success(request, "Points added to " + str(driver.user.username) + " successfully.")
                        else:
                            subtract = point_form.cleaned_data['point_amt']

                            if temp <= 0:
                                temp = 0
                                driver.points = temp
                            else:
                                temp = temp - subtract
                                if temp <= 0:
                                    temp = 0
                                else:
                                    driver.points = temp
                            driver.save()
                            messages.success(request, "Points removed from " + str(driver.user.username) + " successfully.")

                        
                        return redirect('/organization/view/driver/'+str(id))
                else:
                    point_form = PointReasonForm()
                return render(request, 'sponsor_organization/add_points.html', {'point_form': point_form, 'driver': driver, 'sponsor': sponsor, 'profile': profile})
    elif request.user.is_superuser:
        try:
            driver = DriverProfile.objects.get(id=id)
        except DriverProfile.DoesNotExist:
            driver = None
        if request.method == 'POST':
            point_form = PointReasonForm(request.POST)

            if point_form.is_valid():
                instance = point_form.save()
                point_reason, created = PointReason.objects.get_or_create(id=instance.id)
                point_reason.point_amt = point_form.cleaned_data['point_amt']
                point_reason.point_reason = point_form.cleaned_data['point_reason']
                point_reason.driver = driver
                point_reason.save()
                temp = driver.points
                if point_reason.is_add:
                    add = point_reason.point_amt
                    temp = temp + add
                    driver.points = temp
                    driver.save()
                    messages.success(request, "Points added to " + str(driver.user.username) + " successfully.")
                else:
                    subtract = point_form.cleaned_data['point_amt']

                    if temp <= 0:
                        temp = 0
                        driver.points = temp
                    else:
                        temp = temp - subtract
                        driver.points = temp
                    driver.save()
                    messages.success(request, "Points removed from " + str(driver.user.username) + " successfully.")

                return redirect('/organization/view/driver/'+str(id))
        else:
            point_form = PointReasonForm()
        return render(request, 'sponsor_organization/add_points.html', {'point_form': point_form, 'driver': driver, 'profile': profile})

def add_sponsor_user(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to an authorized account to view this page.")
        return redirect('/')
    try:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None
    if not request.user.is_superuser and not profile.is_sponsor and not profile.is_driver:
        messages.error(request, "There is an error with your account, please contact Team06 at team06.onlydrivers@gmail.com for support.")
        return redirect('/about')
    if profile.is_sponsor:
        sponsor_user = SponsorUserProfile.objects.get(user=request.user)
        if request.method == "POST":
            form = RegisterUserForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                user = authenticate(username=username, password=password)
                try:
                    sponsor, created = SponsorUserProfile.objects.get_or_create(user=user)
                except SponsorUserProfile.DoesNotExist:
                    sponsor = None
                sponsor.first_name = form.cleaned_data['first_name']
                sponsor.last_name = form.cleaned_data['last_name']
                sponsor.email = form.cleaned_data['email']
                sponsor.is_sponsor = True
                sponsor.user.is_staff = True
                sponsor.user.is_active = True
                sponsor.sponsor_name = sponsor_user.sponsor_name
                sponsor.user = user
                sponsor.save()
                my_group = Group.objects.get(name='Sponsor User') 
                my_group.user_set.add(sponsor.user)
                messages.success(request, ("You successfully added a new sponsor user to " + sponsor_user.sponsor_name +"."))
                return redirect('/dashboard')
        else:
            form = RegisterUserForm()

        return render(request, 'sponsor_organization/add_sponsor_user.html', {'form':form, 'sponsor_user': sponsor_user,})
    elif request.user.is_superuser:
        if request.method == "POST":
            form = RegisterUserForm(request.POST)
            assign_form = AssignSponsorForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                user = authenticate(username=username, password=password)
                try:
                    sponsor, created = SponsorUserProfile.objects.get_or_create(user=user)
                except SponsorUserProfile.DoesNotExist:
                    sponsor = None
                sponsor.first_name = form.cleaned_data['first_name']
                sponsor.last_name = form.cleaned_data['last_name']
                sponsor.email = form.cleaned_data['email']
                sponsor.is_sponsor = True
                sponsor.user.is_staff = True
                sponsor.user.is_active = True
                assign_form.save(commit=False)
                sponsor.sponsor_name = assign_form.cleaned_data['sponsor_name']
                sponsor.user = user
                sponsor.save()
                my_group = Group.objects.get(name='Sponsor User') 
                my_group.user_set.add(sponsor.user)
                messages.success(request, ("You successfully added a new sponsor user to " + sponsor.sponsor_name +"."))
                return redirect('/dashboard')
        else:
            form = RegisterUserForm()
            assign_form = AssignSponsorForm()

        return render(request, 'sponsor_organization/add_sponsor_user.html', {'form':form, 'assign_form': assign_form,})
    
    else:
        messages.error(request, "You do not have the proper permissions to access this page.")
        return redirect('/about')
    
def sponsor_list(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to an authorized account to view this page.")
        return redirect('/')
    try:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None
    if not request.user.is_superuser and not profile.is_sponsor and not profile.is_driver:
        messages.error(request, "There is an error with your account, please contact Team06 at team06.onlydrivers@gmail.com for support.")
        return redirect('/about')
    if profile.is_driver:
        driver = DriverProfile.objects.get(user=request.user)
        sponsors = driver.sponsors.all()
        sponsor_ids = sponsors.values_list('id', flat=True)
        sponsors_and_sponsor_ids = list(zip(sponsors, sponsor_ids))

        return render(request, 'driver_functions/sponsors_list.html', {'sponsors_and_sponsor_ids': sponsors_and_sponsor_ids, 'profile': profile,})
    else:
        messages.error(request, "You do not have the proper permissions to access this page.")
        return redirect('/about')

def leave_sponsor_confirm(request, id):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to an authorized account to view this page.")
        return redirect('/')
    try:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None
    if not request.user.is_superuser and not profile.is_sponsor and not profile.is_driver:
        messages.error(request, "There is an error with your account, please contact Team06 at team06.onlydrivers@gmail.com for support.")
        return redirect('/about')
    if profile.is_driver:
        sponsor = SponsorList.objects.get(id=id)
        sponsor_id = id
        return render(request, 'driver_functions/leave_sponsor.html', {'profile': profile, 'sponsor': sponsor, 'sponsor_id': sponsor_id,})
        
def leave_sponsor(request, id):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to an authorized account to view this page.")
        return redirect('/')
    try:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None
    if not request.user.is_superuser and not profile.is_sponsor and not profile.is_driver:
        messages.error(request, "There is an error with your account, please contact Team06 at team06.onlydrivers@gmail.com for support.")
        return redirect('/about')
    driver = DriverProfile.objects.get(user=request.user)
    sponsor = SponsorList.objects.get(id=id)
    driver.sponsors.remove(sponsor)
    driver.save()
    messages.success(request, ("You successfully left the " + sponsor.sponsor_name +" sponsor organization."))
    return redirect('/dashboard')

def enter_email(request):
    form = EmailForm(request.POST)
    if form.is_valid():
        email_address = form.cleaned_data['email']
        messages.success(request, f"An email has been sent to {email_address}. \nPlease check your inbox.")

        send_mail("OnlyDrivers: Reset Your Password",
                  "Forgot your password?\n" \
                  "No worries, it happens! Click the link below to log in to your OnlyDrivers account." \
                  "This link expires in 10 minutes and can only be used once.",
                  'onlydrivers4910@gmail.com', 
                  [email_address])
        
    return render(request, 'password_change/enter_email.html', {'form': form})