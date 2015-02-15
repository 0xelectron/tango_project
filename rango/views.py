from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm
from rango.forms import UserForm, UserProfileForm
from datetime import datetime


def index(request):
    category_list = Category.objects.order_by('-likes')[:8]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories' : category_list, 'pages' : page_list,}

    visits = request.session.get('visits')
    if not visits:
        visits = 1
    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        if (datetime.now() - last_visit_time).days > 0:
            # ...reassign the value of the cookie to +1 of what it was before...
            visits = visits + 1
            # ...and update the last visit cookie, too.
            reset_last_visit_time = True
    else:
        # Cookie last_visit doesn't exist, so create it to the current date/time.
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits
    context_dict['visits'] = visits


    response = render(request,'rango/index.html', context_dict)

    return response

#def register (request):
#	registered = False
#
#	if request.method == 'POST':
#
#		user_form = UserForm(data = request.POST)
#		profile_form = UserProfileForm(data = request.POST)
#
#		if user_form.is_valid() and profile_form.is_valid():
#
#			user = user_form.save()
#
#			user.set_password(user.password)
#			user.save()
#
#			profile = profile_form.save(commit = False)
#			profile.user = user
#
#			if 'picture' in request.FILES:
#				profile.picture = request.FILES['picture']
#
#			profile.save()
#
#			registered = True
#
#		else:
#			print user_form.errors, profile_form.errors
#
#	else:
#		user_form = UserForm()
#		profile_form = UserProfileForm()
#
#	return render(request, 'rango/register.html', {'user_form': user_form, 'profile_form' : profile_form, 'registered' : registered})
#
#def user_login(request):
	
#	if request.method == 'POST':
#		username = request.POST['username']
#		password = request.POST['password']
#
#		user = authenticate(username = username, password = password)
#
#		if user:
#			if user.is_active:
#
#				login(request, user)
#				return HttpResponseRedirect('/rango/')
#
#			else:
#
#				return HttpResponse("Your Rango account is disabled.")
#
#		else:
#
#			print "Invalid login details: {0}, {1}".format(username, password)
#			return HttpResponse("Invalid login details supplied.")
#
#	else:
#
#		return render(request, 'rango/login.html', {})

#@login_required
#def user_logout(request):
#	logout(request)
#
#	return HttpResponseRedirect('/rango/')

def category(request, category_name_slug):
	#create a  context dictionary to pass in to template engine
	context_dict = {}
	try:
		#get category name from db if there, and add to context dict
		category = Category.objects.get(slug = category_name_slug)
		context_dict['category_name'] = category.name

		#get pages of the the particular category if any add to context dict
		pages = Page.objects.filter(category = category)
		context_dict['pages'] = pages

		#we'll need category object in template to verify if category exist
		context_dict['category'] = category

		context_dict['category_name_slug'] = category_name_slug

	except Category.DoesNotExist:
		#doesn't need to do anything
		pass   									

	return render(request, 'rango/category.html', context_dict)



@login_required
def restricted(request):
	return (render (request, 'rango/restricted.html', {}))

def about(request):
    
    return render(request,'rango/about.html',{})

@login_required
def add_category(request):
	if request.method == "POST":
		form = CategoryForm(request.POST)

		if form.is_valid():
			cat = form.save(commit=True)
			return index(request)

		else:
			print form.errors

	else:
		form = CategoryForm()

	return render(request, 'rango/add_category.html', {'form' : form})


@login_required
def add_page(request, category_name_slug):
	
	try:
		cat = Category.objects.get(slug = category_name_slug)

	except Category.DoesNotExist:
		cat = None 

	if request.method == 'POST':
		form = PageForm(request.POST)
		if form.is_valid():
			if cat:
				page = form.save(commit = False)
				page.category = cat
				page.views = 0
				page.save()
				return category(request, category_name_slug)
		else:
			print form.errors

	else:
		form = PageForm()

	context_dict = {'form': form, 'category': cat, 'category_name_slug': category_name_slug}

	return render(request, 'rango/add_page.html', context_dict)