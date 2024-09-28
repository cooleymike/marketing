from django.template.response import TemplateResponse


from django.http import HttpResponse

def homepage(request):
   return TemplateResponse(request, "home.html")

def welcome(request):
    return HttpResponse(request,'welcome.html')

def bookeeping(request):
    return HttpResponse(request,'bookkeeping.html')

def managing(request):
    return HttpResponse(request,'managing.html')

def confirm(request):
    return HttpResponse(request,'confirm.html')

def signup(request):
    return HttpResponse(request,'signup.html')

def upload(request):
    return HttpResponse(request,'upload.html')

def password_reset(request):
    return HttpResponse(request,'password_reset.html')

def password_reset_complete(request):
    return HttpResponse(request,'password_reset_complete.html')

def password_reset_confirm(request):
    return HttpResponse(request,'password_reset_confirm.html')

def password_reset_done(request):
    return HttpResponse(request,'password_reset_done.html')

def expenses(request):
    return HttpResponse(request,'expenses.html')

