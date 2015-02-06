from django.shortcuts import render
from rango.models import Category, Page

# Create your views here.

from django.http import HttpResponse

def index(request):
    #Construct a dictionary to pass to the template engine as its context.
    # Query to retrive all the categries from the database
    category_list = Category.objects.order_by('-likes')[:5]
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

	except Category.DoesNotExist:
		#doesn't need to do anything
		pass   									

	return render(request, 'rango/category.html', context_dict)


def about(request):
    
    return render(request,'rango/about.html')
