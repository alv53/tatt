from django.template import Context, RequestContext
from django.views.decorators.csrf import csrf_protect
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth import login, logout, authenticate
from main.models import *
from main.forms import *

@csrf_protect
def index(request):
    c = RequestContext(request, {
        'page_title' : 'index',
		'badcred' : False
    })

    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_data = login_form.cleaned_data
            user = authenticate(username=user_data['username'], password=user_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    print "user logged in!" 
                    return HttpResponseRedirect('/items')
                else:
                    print "user not active"
            else:
                c['badcred'] = True

    return render_to_response('index.html',context_instance=c)

def logout_view(request):
    logout(request)
    return redirect('/')

@csrf_protect
def register(request, *args, **kwargs):
    """Register a new user"""
    if request.method == 'POST':
        print request.POST
        user_form = UserForm(request.POST)
        if user_form.is_valid():

            user_form = user_form.cleaned_data
            new_user = User.objects.create_user(username=user_form['username'],
                                                password=user_form['password'])
            new_user.first_name = user_form['first_name']
            new_user.last_name = user_form['last_name']

            new_user.save()
            print "new user created"
            # TODO: we should redirect to a login with a special header or something
            return HttpResponseRedirect('/')
        else:
            print "user_form not valid!"
    else:
        user_form = UserForm()
        
    kwargs.update(csrf(request))
    c = RequestContext(request, dict(registration_form=user_form, **kwargs))
    return render_to_response('register.html', c)

def userpage(request):
    c = RequestContext(request, {
            'page_title' : 'user_page',
        })
    return render_to_response('user_page.html', c)

def items(request):
    if request.method == 'GET':
        #TODO: parse search string and show new items
        pass

    items = Item.objects.all()
    c = RequestContext(request, {'items' : items})
    return render_to_response('items.html', c)

def item_info(request, item_id):
    try:
        item =  Item.objects.get(pk=item_id)
    except Items.DoesNotExist:
        #TODO: print out an error message or something about the item not exhisting
        raise Http404
    return render_to_response('itemDetail.html', {'item' : item} )

def search(request, search_query):
    #TODO: Search the database and return a list of items, put in to requestcontext
    c = RequestContext(request, {'search_query' : search_query})
    return render_to_response('search.html', c)

def search_query(query_string):
    #TODO: Search the database and return all items matching the query string as a list
    item_lis = []
    return item_lis

def about(request):
    c = RequestContext(request, {})
    return render_to_response('about.html', c)


##### Views that are used to add to the database #####
def add_item(request):
    if request.method == 'POST':
        item_form = ItemForm(request)
        if item_form.is_valid():
            item_form = item_form.cleaned_data
            #TODO: Test that this works if not we'll need to pull each item from the form
            new_item = Item(item_form)
            new_item.location = 'None'
            new_item.has_photo = False
            new_item.save()
            print "Item added to database"
        else:
            print "item_form not valid"
    else:
        HttpResponseRedirect("/items")

def add_item_type(request):
    if request.method == 'POST':
        item_type_form = ItemTypeForm(request)
        if item_type_form.is_valid():
            item_type_form = item_type_form.cleaned_data
            #TODO: Test that this works if not we'll need to pull each item from the form
            new_type = ItemType(item_type_form)
            print "ItemType added to database"
        else:
            print "item_type_form not valid"
    else:
        HttpResponseRedirect("/items")

def add_attribute(request):
    if request.method == 'POST':
        attr_form = AttributeForm(request)
        if attr_form.is_valid():
            attr_form = attr_form.cleaned_data
            #TODO: Like item, verify this works
            attr = Attribute(attr_form)
            attr.save() 
            print "Attribute added to database"
        else:
            print "attr_form is not valid!"
    else:
        HttpResponseRedirect("/items")

def add_attribute_value(request):
    if request.method == 'POST':
        attr_val_form = AttributeValueForm(request)
        if attr_val_form.is_valid():
            attr_val_form = attr_val_form.cleaned_data
            #TODO: Like item, verify this works
            attr_val = AttributeValue(attr_val_form)
            attr_val.save()
            print "Attribute value added to database"
        else:
            print "attr_val_form is not valid!"
    else:
        HttpResponseRedirect("/items")
