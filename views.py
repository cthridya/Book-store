from django.forms import BaseModelForm
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.views.generic import CreateView,ListView
from django.contrib.auth.models import User
from bookapp.models import Book
from bookapp.forms import RegisterForm,LoginForm,SearchForm
from django.contrib import messages
from django.shortcuts import redirect,render
from django.contrib.auth import authenticate,login,logout
from django.core.paginator import Paginator
# Create your views here.

def Bookview(request):
    return render(request,'home.html')
class Registerview(CreateView):
    template_name='register.html'
    model=Book
    form_class=RegisterForm
    def form_valid(self, form):
        messages.success(self.request,'registration is sucessfull')
        User.objects.create_user(**form.cleaned_data)
        return redirect('home_view')
    def form_invalid(self, form: BaseModelForm):
        messages.error(self.request,'invalid credentials')
        return render('home_view')


class LoginView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,'login.html',{'form':form})
    
    def post(self,request,*args,**kwargs):
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        
        if user:
            login(request,user)
            messages.success(request,'Login Successfully')
            return render(request,'index.html')
        else:
            messages.error(request,"invalid credentials")
            form=LoginForm()
            return render(request,'login.html',{'form':form})
def Logoutview(request):
    logout(request)
    return redirect('home_view')
def Listview(request):
    books=Book.objects.all()
    paginator=Paginator(books,4)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    return render(request,'index.html',{'page_obj':page_obj})
  
def Booklist(request):
    form=SearchForm()
    books=Book.objects.all()

    if 'title' in request.GET:
        form=SearchForm(request.GET)
        if form.is_valid():
            title=form.cleaned_data['title']
            books = Book.objects.filter(title__icontains=title)

    return render(request, 'search_books.html', {'form': form, 'books': books})

        

