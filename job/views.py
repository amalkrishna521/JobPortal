from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import recruiter 
from datetime import date
from .forms import ProfileForm, UserForm
from job.models import *


# Create your views here.

def index(request):
    return render(request,'index.html')
def admin_login(request):
    error = ''
    if request.method == 'POST':
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u,password=p)
        try:
            if user.is_staff:
                login(request,user)
                error='no'
            else:
                error = 'yes'
        except:
            error = 'yes'
    d = {'error':error}

    return render(request,'admin_login.html',d)
def user_login(request):
    error = ''
    if request.method == 'POST':
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u,password=p)
        if user:
            try:
                user1 = studentuser.objects.get(user=user)
                if user1.type == 'student':
                    login(request,user)
                    error='no'
                else:
                    error="yes"
            except:
                error="yes"
        else:
            error="yes"
    d = {'error':error}
    return render(request,'user_login.html',d)
def recruter_login(request):
    error = ''
    if request.method == 'POST':
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u,password=p)
        if user:
            try:
                user1 = recruiter.objects.get(user=user)
                if user1.type == 'recruiter' and user1.status!="pending":
                    login(request,user)
                    error='no'
                else:
                    error="not"
            except:
                error="yes"
        else:
            error="yes"
    d = {'error':error}
    return render(request,'recruter_login.html',d)

def recruiter_signup(request):
    error = ''
    d = {'error': error}  # Initialize the context dictionary

    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        i = request.FILES['image']
        p = request.POST['pwd']
        e = request.POST['email']
        con = request.POST['contact']
        gen = request.POST['gender']
        company = request.POST['company']
        try:
            # Create a User instance
            user = User.objects.create_user(first_name=f, last_name=l, username=e, password=p)
            # Create a recruiter object with the User instance
            recruiter.objects.create(user=user, mobile=con, image=i, gender=gen, company=company, type='recruiter', status='pending')
            error = 'no'
        except:
            error = 'yes'

        d = {'error': error}  # Update the context dictionary

    return render(request, 'recruiter_signup.html', d)



def user_home(request):
    user = request.user
    student = studentuser.objects.get(user=user)
    
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=student)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_home')
    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=student)

    context = {
        'student': student,
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'user_home.html', context)
def admin_home(request):
    if not request.user.is_authenticated:
        return redirect(admin_login)
    rcount=recruiter.objects.all().count()
    scount=studentuser.objects.all().count()
    d={'rcount':rcount,'scount':scount}
    return render(request,'admin_home.html',d)
def recruiter_home(request):
    if not request.user.is_authenticated:
        return redirect(recruter_login)

    user = request.user
    recruiter_instance = recruiter.objects.get(user=user)
    error = ''

    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        con = request.POST['contact']
        company = request.POST['company']
        e = request.POST['email']
        gen = request.POST['gender']
        i = request.FILES.get('image')

        try:
            user.first_name = f
            user.last_name = l
            user.username = e
            user.save()

            recruiter_instance.mobile = con
            recruiter_instance.company = company
            recruiter_instance.gender = gen
            if i:
                recruiter_instance.image = i
            recruiter_instance.save()

            error = 'no'
        except:
            error = 'yes'

    d = {'recruiter': recruiter_instance, 'error': error}
    return render(request, 'recruiter_home.html', d)


def Logout(request):
    logout(request)
    return redirect('index')
   
def user_signup(request):
    error = ''
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        i = request.FILES['image']
        p = request.POST['pwd']
        e = request.POST['email']
        con = request.POST['contact']
        gen = request.POST['gender']
        try:
            # Create a User instance
            user = User.objects.create_user(first_name=f, last_name=l, username=e, password=p)
            # Create a studentuser object with the User instance
            studentuser.objects.create(user=user, mobile=con, image=i, gender=gen, type='student')
            error = 'no'
        except:
            error = 'yes'
    d = {'error': error}

    return render(request, 'user_signup.html', d)
def view_users(request):
    if not request.user.is_authenticated:
        return redirect(admin_login)
    else:
        data=studentuser.objects.all()
        d={'data':data}
    return render(request,'view_users.html',d)

def recruiter_pending(request):
    if not request.user.is_authenticated:
        return redirect(admin_login)
    data=recruiter.objects.filter(status='pending')
    d={'data':data}
    return render(request,'recruiter_pending.html',d)
def change_status(request, pid):
    if not request.user.is_authenticated:
        return redirect(admin_login)
    
    error = ''
    try:
        recruiter_instance = recruiter.objects.get(id=pid)  # Corrected the model name to lowercase 'recruiter'
    except recruiter.DoesNotExist:
        return redirect('recruiter_pending')  # Handle case where recruiter does not exist
    
    if request.method == 'POST':
        s = request.POST['status']
        recruiter_instance.status = s
        try:
            recruiter_instance.save()
            error = 'no'
        except:
            error = 'yes'

    d = {'recruiter': recruiter_instance, 'error': error}
    return render(request, 'change_status.html', d)
def recruiter_accepted(request):
    if not request.user.is_authenticated:
        return redirect(admin_login)
    data=recruiter.objects.filter(status='accept')
    d={'data':data}
    return render(request,'recruiter_accepted.html',d)
def recruiter_rejected(request):
    if not request.user.is_authenticated:
        return redirect(admin_login)
    data=recruiter.objects.filter(status='reject')
    d={'data':data}
    return render(request,'recruiter_rejected.html',d)
def recruiter_all(request):
    if not request.user.is_authenticated:
        return redirect(admin_login)
    data=recruiter.objects.all()
    d={'data':data}
    return render(request,'recruiter_all.html',d)
def delete_recruiter(request,pid):
    if not request.user.is_authenticated:
        return redirect(admin_login)
    recruiter=User.objects.get(id=pid)
    recruiter.delete()
    return redirect('recruiter_all')
def delete_user(request,pid):
    if not request.user.is_authenticated:
        return redirect(admin_login)
    student=User.objects.get(id=pid)
    student.delete()
    return redirect('view_users')
def change_passwordadmin(request):
    if not request.user.is_authenticated:
        return redirect(admin_login)
    
    error = ''
   
    if request.method == 'POST':
        c = request.POST['currentpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error = 'no'
            else:
                error = 'yes'
        except:
            error = 'yes'
    
    d = {'error': error}
    return render(request, 'change_passwordadmin.html', d)
def change_passworduser(request):
    if not request.user.is_authenticated:
        return redirect(user_login)
    
    error = ''
   
    if request.method == 'POST':
        c = request.POST['currentpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error = 'no'
            else:
                error = 'yes'
        except:
            error = 'yes'
    
    d = {'error': error}
    return render(request, 'change_passworduser.html', d)
def change_passwordrecruiter(request):
    if not request.user.is_authenticated:
        return redirect(recruter_login)
    
    error = ''
   
    if request.method == 'POST':
        c = request.POST['currentpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error = 'no'
            else:
                error = 'yes'
        except:
            error = 'yes'
    
    d = {'error': error}
    return render(request, 'change_passwordrecruiter.html', d)
def add_job(request):
    if not request.user.is_authenticated:
        return redirect(recruter_login)
    error=''


    return render(request,'add_job.html')
def job_list(request):
    if not request.user.is_authenticated:
        return redirect(recruter_login)
    user = request.user
    recruiter_instance = recruiter.objects.get(user=user)  # Use lowercase 'recruiter' for the instance
    jobs = job.objects.filter(recruiter=recruiter_instance)  # Use lowercase 'jobs' for the queryset
    context = {'jobs': jobs}  # Use lowercase 'jobs' in the context
    return render(request, 'job_list.html', context)


def add_job(request):
    if not request.user.is_authenticated:
        return redirect(recruter_login)
    error = ''
    if request.method == 'POST':
        jt = request.POST.get('jobtitle')
        sd = request.POST.get('startdate')
        ed = request.POST.get('enddate')
        sal = request.POST.get('salary')
        exp = request.POST.get('experience')
        loc = request.POST.get('location')
        skills = request.POST.get('skills')
        des = request.POST.get('description')
        user = request.user
        recruiter_obj = recruiter.objects.get(user=user)
        
        l = request.FILES.get('logo')  # Use get method to avoid KeyError

        try:
            job.objects.create(
                recruiter=recruiter_obj,
                start_date=sd,
                end_date=ed,
                title=jt,
                salary=sal,
                image=l,
                description=des,
                experience=exp,
                location=loc,
                skills=skills,
                creationdate=date.today()
            )
            error = 'no'
        except Exception as e:
            error = 'yes'
            print(f"Error occurred: {e}")  # This will help in debugging

    d = {'error': error}
    return render(request, 'add_job.html', d)
def edit_job(request, job_id):
    Job = get_object_or_404(job, pk=job_id)
    if request.method == 'POST':
        # Update job details based on form submission
        Job.title = request.POST.get('jobtitle')
        Job.start_date = request.POST.get('startdate')
        Job.end_date = request.POST.get('enddate')
        Job.salary = request.POST.get('salary')
        if 'logo' in request.FILES:
            Job.image = request.FILES['logo']  # Ensure the image field matches your model
        Job.experience = request.POST.get('experience')
        Job.location = request.POST.get('location')
        Job.skills = request.POST.get('skills')
        Job.description = request.POST.get('description')
        Job.save()
        return redirect('job_list')  # Redirect to job list after editing
    return render(request, 'edit_job.html', {'Job': Job})
def latest_jobs(request):
    jobs=job.objects.all().order_by('-start_date')
    d={'jobs':jobs}
    return render(request,'latest_jobs.html',d)
def user_latestjobs(request):
    jobs=job.objects.all().order_by('-start_date')
    user =request.user
    new_student=studentuser.objects.get(user=user)
    data=apply.objects.filter( student= new_student)
    li=[]
    for i in data:
        li.append(i.Job.id)
    d={'jobs':jobs,'li':li}
    return render(request,'user_latestjobs.html',d)
def job_detail(request,pid):
    jobs=job.objects.get(id=pid)
    d={'jobs':jobs}
    return render(request,'job_detail.html',d)






def applyforjob(request,pid):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error=''
    user = request.user
    student=studentuser.objects.get(user=user)
    jobs=job.objects.get(id=pid)
    date1=date.today()
    if jobs.end_date< date1:
        error='close'
    elif jobs.start_date>date1:
        error='notopen'
    else:
        if request.method=='POST':
            r=request.FILES['resume']
            apply.objects.create(Job=jobs,student=student,resume=r,applydate=date.today())
            error='done'
       
    
    d={'error':error}
    return render(request,'applyforjob.html',d)
def applied_candidatelist(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    data=apply.objects.all()
    d={'data':data}
    return render(request,'applied_candidatelist.html',d) 
def contact(request):
    return render(request,'contact.html')  
def delete_job(request, job_id):
    if not request.user.is_authenticated:
        return redirect('recruter_login')  

    job_instance = get_object_or_404(job, id=job_id)  
    job_instance.delete()  
    return redirect('job_list')   