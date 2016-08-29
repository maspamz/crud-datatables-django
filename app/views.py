from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseGone
from django.shortcuts import render, redirect, get_object_or_404

from app.models import Book


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'pages', 'date_written', 'type']

def home(request):
    html = """
    <h1>Django CRUD Example</h1>
    <a href="/books/">Book list</a><br>
    """
    return HttpResponse(html)

def book_list(request, template_name='book_list.html'):
    book = Book.objects.all()
    data = {}
    data['object_list'] = book
    return render(request, template_name, data)

def book_create(request, template_name='book_form.html'):
    form = BookForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('book_list')
    return render(request, template_name, {'form':form})

def book_update(request, pk, template_name='book_form.html'):
    book= get_object_or_404(Book, pk=pk)
    form = BookForm(request.POST or None, instance=book)
    print(request.POST);
    if form.is_valid():
        form.save()
        return HttpResponse(status=200)
    return HttpResponse(status=400)

def book_delete(request, pk):
    book= get_object_or_404(Book, pk=pk)    
    if request.method=='DELETE':
        book.delete()
        return HttpResponse(status=204)
    return HttpResponse(status=405)
