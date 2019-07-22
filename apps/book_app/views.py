from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import User, Book

def index(request):
    return render(request,"book_app/index.html")

def registration(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        if request.method == "POST":
            new_first_name = request.POST["first_name"]
            new_last_name = request.POST["last_name"]
            new_email = request.POST["email"]
            new_password = request.POST["password"]
            hash1 = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
            print(hash1)
            new_user = User.objects.create(first_name=new_first_name, last_name=new_last_name, email=new_email, password=hash1)
            messages.success(request,"You have sucessfully registered. Please Login")
            return redirect("/")

def login(request):
    errors = User.objects.user_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    # valid = True
    # if len(request.POST['email']) < 1:
    #     valid = False
    #     messages.error(request, "You must enter an email to login")
    # if len(request.POST['password']) < 8: 
    #     valid = False
    #     messages.error(request, "Password must be longer than 8 characters")
    #     return redirect('/')
    else:
        if request.method == "POST":
            user = User.objects.filter(email=request.POST['email'])
            print(user)
            if len(user) == 0: 
                messages.error(request,"Records do not match, please try again")
                return redirect('/')
            else:
                person = user[0]
                if bcrypt.checkpw(request.POST['password'].encode(),person.password.encode()):
                    request.session['id'] = person.id
                    request.session['book_message'] = "this is one of your favorites"
                    return redirect("/books")
                else:
                    messages.error(request,"Records do not match, please try again")
                    return redirect('/')

def main_page(request):
    if 'id' not in request.session:
        messages.error(request,"You must be logged in first")
        return redirect("/")
    else:
        this_user = User.objects.get(id=request.session['id'])
        context = {
            "user" : this_user,
            "all_books": Book.objects.all(),
            "user_favorite_books": this_user.liked_books.all()
        }
        return render(request,"book_app/main_page.html", context)

def add_book(request):
    errors = Book.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/books")
    else:
        if request.method == "POST":
            new_title = request.POST["title"]
            new_description = request.POST["description"]
            this_user = User.objects.get(id=request.session['id'])
            new_book = Book.objects.create(title=new_title, description=new_description, uploaded_by=this_user)
            new_book.users_who_like.add(this_user)
            request.session['book_message'] = "this is one of your favorites"
            return redirect("/books")

def view_book(request,id):
    a_book = Book.objects.get(id=id)
    context = {
        "this_user" : User.objects.get(id=request.session['id']),
        # "user_uploaded_book": this_user.books_uploaded.all(),
        "this_book" : Book.objects.get(id=id),
        "this_book_favorite_users": a_book.users_who_like.all()
    }
    return render(request, "book_app/view_book.html", context)

def update(request,id):
    errors = Book.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f"/books/{id}")
    else:
        if request.method == "POST":
            updated_title = request.POST["title"]
            updated_description = request.POST["description"]
            update_book = Book.objects.get(id=id)
            update_book.title = updated_title
            update_book.description = updated_description
            update_book.save()
            return redirect(f"/books/{id}")

def favorite(request,id):
    this_user = User.objects.get(id=request.session['id'])
    this_book = Book.objects.get(id=id)
    book_add_favorite = this_book.users_who_like.add(this_user)
    return redirect("/books")

def favorite1(request,id):
    this_user = User.objects.get(id=request.session['id'])
    this_book = Book.objects.get(id=id)
    book_add_favorite = this_book.users_who_like.add(this_user)
    return redirect(f"/books/{id}")
        
def unfavorite(request,id):
    this_user = User.objects.get(id=request.session['id'])
    this_book = Book.objects.get(id=id)
    unfavorited_user = this_user.liked_books.remove(this_book)
    return redirect(f'/books/{id}')

def delete(request):
    this_user = User.objects.get(id=request.session['id'])
    delete_book = Book.objects.get(uploaded_by_id=this_user)
    delete_book.delete()
    return redirect("/books")

def logout(request):
    del request.session['id']
    return redirect("/")