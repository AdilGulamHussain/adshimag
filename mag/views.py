import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .models import Article, MagUser, Category, Comment
from .forms import CommentForm, LoginForm, NewUserForm


# Create your views here.

defaultUser = MagUser.objects.get(email="anon@default.com")


def __anon_user(request):
    del request.session['currentUser']


def index(request):
    articles = Article.objects.all()
    user = __user(request)
    return render(request, 'mag/index.html', context={'articles': articles, 'user': user})


def article_view(request, a_id):
    article = Article.objects.get(pk=a_id)
    user = __user(request)
    like_val = "Like"
    if user is not defaultUser:
        like_val = "Dislike" if user in article.likes.all() else "Like"
    return render(request, 'mag/article.html', context={'article': article, 'user': user, 'form': CommentForm(),
                                                        'like': like_val})


def all_categories(request):
    categories = Category.objects.all()
    user = __user(request)
    return render(request, 'mag/categories.html', context={'categories': categories, 'user': user})


def articles_in_category(request, c_title):
    articles = Article.objects.filter(category__slug=c_title)
    user = __user(request)
    return render(request, 'mag/category_articles.html', context={'articles': articles, 'user': user})


def __user(request):
    user_email = request.session.get('currentUser')
    if user_email is not None:
        return MagUser.objects.get(email=user_email)
    else:
        return defaultUser


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            first = form.cleaned_data['first_name']
            last = form.cleaned_data['last_name']
            phone = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']

            new_user = MagUser(email=email, first_name=first, last_name=last, phone_number=phone, password=password)
            new_user.logged_in = True
            new_user.save()
            request.session['currentUser'] = new_user.email
            return redirect('index')
    else:
        form = NewUserForm()

    return render(request, 'mag/registration.html', context={'form': form})


def process_login(request):  # Test this next!
    if request.method == "POST":
        form = LoginForm(request.POST)
        # print(request.session.get('currentUser'))
        if "email" in request.POST and "password" in request.POST:
            email = request.POST["email"]
            password = request.POST["password"]
            try:
                user = MagUser.objects.get(email=email, password=password)
                user.logged_in = True
                user.save()
                request.session['currentUser'] = user.email
                # print(request.session.get('currentUser') + " in")
                return redirect('index')
            except MagUser.DoesNotExist:
                # print(request.session.get('currentUser'))
                return HttpResponse(""""<script type="text/javascript">alert("Invalid email or password!");
                                    window.location="/magazine/login/";</script>""")
    else:
        form = LoginForm()

    return render(request, 'mag/login.html', context={'form': form})


def logged_in(f):
    def is_logged_in(request):
        if __user(request).is_authenticated():
            return f(request)
        else:
            return HttpResponse("""<script>alert("You're not logged in!");
                                location.href = "/magazine/login/";</script>""")
    return is_logged_in


@logged_in
def logout(request):
    user = __user(request)
    user.logged_in = False
    print(user)
    user.save()
    __anon_user(request)
    return redirect('index')


def new_comment(request):
    if request.is_ajax() and request.method == "POST":
        comment_body = request.POST.get('comment_body')
        article_id = request.POST.get('article_id')
        article = Article.objects.get(pk=article_id)
        comment = Comment(body=comment_body, user=__user(request), article=article)
        comment.save()
        ret_dict = {'body': comment.body, 'date_time': comment.date_time, 'user_name': comment.user.get_full_name()}

        return JsonResponse(ret_dict, safe=False)


@logged_in
def dash(request):
    user = __user(request)
    return render(request, 'mag/dashboard.html', context={'user': user})


@logged_in
def like(request):
    if request.is_ajax():
        user = __user(request)
        data = json.loads(request.body.decode('utf-8'))
        a_id = data['article_id']
        article = Article.objects.get(pk=a_id)
        # print(data['is_liked'])

        if request.method == "DELETE":
            article.remove_like(user)
            return JsonResponse({'status': 'Disliked'})

        if request.method == "POST":
            article.add_like(user)
            return JsonResponse({'status': 'Liked'})


@logged_in
def delete_comment(request):
    if request.is_ajax() and request.method == "DELETE":
        data = json.loads(request.body.decode('utf-8'))
        print(data['comment_id'])
        Comment.objects.get(pk=data['comment_id']).delete()  # article_id=data['article_id'], user_id=data['user_id'])
        return JsonResponse({'status': True})


def update_details(request):
    if request.is_ajax() and request.method == "PUT":
        data = json.loads(request.body.decode('utf-8'))
        fname = data['fname']
        lname = data['lname']
        pnum = data['pnum']

        user = __user(request)
        user.first_name = fname
        user.last_name = lname
        user.phone_number = pnum

        user.save()

        return JsonResponse({'status': True})
