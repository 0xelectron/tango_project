from django.shortcuts import render
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm
from django.http import HttpResponse

def index(request):
    #Construct a dictionary to pass to the template engine as its context.
    # Query to retrive all the categries from the database
    category_list = Category.objects.order_by('-likes')[:8]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories' : category_list, 'pages' : page_list,}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.

    return render(request,'rango/index.html',context_dict)

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


def about(request):
    
    return render(request,'rango/about.html')

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

	context_dict = {'form': form, 'Category': cat, 'category_name_slug': category_name_slug}

	return render(request, 'rango/add_page.html', context_dict)