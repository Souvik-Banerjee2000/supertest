from django.shortcuts import render, redirect
from .models import UserProfile, AboutStartup,StartupGroup,Post
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required


def home(request):
    if request.user.is_authenticated:
        user_prof = UserProfile.objects.get(user = request.user)
        context = {
            'user' : user_prof,
        }
        return render(request, 'superapp/home.html',context)
    else:    
        return render(request, 'superapp/home2.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            return HttpResponse('Unsuccesfull')     
    return render(request,'superapp/login.html')  


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect('/')
    else:
        return HttpResponse('Login First')


def register(request):
    if request.method == 'POST':
        # Domains_Covered = request.POST.getlist('checks[]')
        # startup_name = request.POST['name']
        # startup_description = request.POST['description']
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        user = User(email=email, username=username, password=password)
        user.set_password(request.POST['password'])    ## To set the hash is none without this login is not possible
        user.save()
        contact = request.POST['contact-number']
        role = request.POST['role']
        status = request.POST['status']
        userprofile = UserProfile(user=user, contact=contact, status=status, role=role)
        # return HttpResponse(str(domain.Domains_Covered))
        userprofile.save()
        if user:
            auth.login(request, user)
            if userprofile.status == 'EXPLORER':
                return redirect('/')
            else:
                return redirect('/startupinfo')

        # if userprofile.status == 'EXPLORER':
        #     return redirect('/')
        # else:
        #     return redirect('/startupinfo')
    return render(request, 'superapp/submission.html')


@login_required
def startupinfo(request):
    current_user = User.objects.get(username=request.user.username)
    new_user = UserProfile.objects.get(user=current_user)
    if new_user.status == 'EXPLORER':
        return HttpResponse("You Do not Have the Permissions to Visit this page Try to access another pages")
    if request.method == 'POST':
        startup_name = request.POST['startupname']
        description = request.POST['description']
        domains_Covered = request.POST.getlist('checks[]')
        about = AboutStartup(startup_name=startup_name,
                             Domains_Covered=domains_Covered, description=description)
        if AboutStartup.objects.filter(startup_name=startup_name, Domains_Covered=domains_Covered, description=description).exists():
            a = AboutStartup.objects.get(
                startup_name=startup_name, Domains_Covered=domains_Covered, description=description)
            new_user.startup = a
            new_user.save()
            return redirect('/')
        about.save()
        new_user.startup = about
        new_user.save()
        return redirect('/')
        print(new_user.status)
    return render(request, 'superapp/startupdescription.html')



def searchforagroup(request): 
    return render(request,'superapp/searchforagroup.html')    
def searchgroup(request):
    search = request.GET['searchgroup']
    print(search)
    user = request.user
    userprof = UserProfile.objects.get(user=user)
    all_groups = StartupGroup.objects.filter(group_name__icontains = search).exclude(users = userprof)
    context = {
        'all_groups': all_groups,
        'search': search,
    }
    return render(request,'superapp/searchgroupresults.html',context)



def search(request):
    search = request.GET['search']
    all_startups_domains = AboutStartup.objects.filter(Domains_Covered__icontains=search)
    all_startups_name = AboutStartup.objects.filter(startup_name=search)
    all_startups = all_startups_domains.union(all_startups_name)
    user_startup_name = UserProfile.objects.filter(startup__startup_name__icontains=search)
    user_startup_domain = UserProfile.objects.filter(startup__Domains_Covered__icontains=search)
    all_user_startups = user_startup_domain.union(user_startup_name)
        # result = all_user_startup.union(all_startups)
    context = {
        'all_startups': all_startups,
        'all_user_startups': all_user_startups,
        'search': search
        }
    return render(request, 'superapp/searchresults.html', context)


@login_required    
def cretaeGroup(request):
    if request.method == 'POST':
        description = request.POST['description']
        groupname = request.POST['groupname']
        current_user = User.objects.get(username = request.user.username)
        # print(current_user.username)
        profile = UserProfile.objects.get(user = current_user)
        group = StartupGroup(description = description,group_name = groupname)
        group.save()
        group.users.add(profile)
        return redirect('viewallgroups')
    return render(request,'superapp/creategroup.html')


def viewallgroups(request):
    user = request.user
    userprofile = UserProfile.objects.get(user = user)
    context = {
        'all_groups' : userprofile.startupgroup_set.all(),
    }
    return render(request,'superapp/allgroups.html',context)
def group_details(request,id):
    group = StartupGroup.objects.get(id = id)
    members = group.users.all()
    current_user = request.user
    current_user_prof = UserProfile.objects.get(user = current_user)
    if current_user_prof in members:
        key = True
    else:
        key = False          
    context = {
        'group' : group,
        'members' : members,
        'key' : key,
    }
    return render(request,'superapp/groupdetails.html',context)

def joingroup(request,id):
    current_group = StartupGroup.objects.get(id = id)
    current_user = request.user
    current_user_prof = UserProfile.objects.get(user = current_user)
    current_group.users.add(current_user_prof)
    return redirect('/')   


def leavegroup(request,id):
    current_group = StartupGroup.objects.get(id=id)
    current_user = request.user
    current_user_prof = UserProfile.objects.get(user=current_user)
    current_group.users.remove(current_user_prof)
    return redirect('/')
def createpost(request,id):
    if request.method == 'POST':
        current_user = request.user
        current_user_prof = UserProfile.objects.get(user = current_user)
        title = request.POST['title']
        description = request.POST['description']
        current_group = StartupGroup.objects.get(id=id)
        post = Post(title = title,description = description,group = current_group,author = current_user_prof)
        post.save()
        return redirect('/')
    # else:
    #     current_group_users = StartupGroup.objects.get(id=id).users.all()
    #     current_user = request.user
    #     current_user_prof = UserProfile.objects.get(user=current_user)
    #     if current_user_prof in current_group_users:
    #         return render(request,'superapp/postforgroups.html')    
    #     else:
    return render(request, 'superapp/postforgroups.html')
def viewposts(request,id):
    current_group = StartupGroup.objects.get(id=id)
    current_group_posts = Post.objects.get(group = current_group)
    print(current_group_posts)
    # context = {
    #     'posts' : current_group_posts
    # }
    # return render(request,'superapp/groupposts.html',context)

    
def ideasubmission(request):
    return render(request,'superapp/rating_submit.html')