from .models import Restaurant, Review
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseForbidden
from django.template import loader
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, Avg, Func

from .forms import LoginForm, RegistrationForm, ReviewForm
from .models import Restaurant, Review



def log_out(request):
    logout(request)
    redirect_url = request.GET.get('next') or reverse('index')
    return redirect(redirect_url)


def log_in(request):
    if request.method == 'POST':
        logout(request)
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(request.GET.get('next'))
            else:
                form.add_error('Invalid credentials!')
    else:  # GET
        form = LoginForm()
    return render(request, 'rest_reviews/login.html', {'form': form})


def sign_up(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            logout(request)
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password_again = form.cleaned_data['password_again']
            if User.objects.filter(username=username).exists():
                form.add_error('username', 'User already exists!')
            elif password != password_again:
                form.add_error('password_again', 'Passwords mismatch!')
            else:
                user = User.objects.create_user(username, email, password)
                return redirect(reverse('login'))
    else:  # GET
        form = RegistrationForm()
    return render(request, 'rest_reviews/signup.html', {'form': form})


class Round(Func):
    function = 'ROUND'
    template='%(function)s(%(expressions)s, 2)'


def get_rest_list(request):
    rests = Restaurant.objects.annotate(review_stars=Round(Avg('review__stars'))).order_by('-review_stars')
    context = {'restaurants': rests}

    return render(request, 'rest_reviews/index.html', context)


def restaurant(request, rest_id):
    if request.method == 'POST':
        return create_review(request, rest_id)
    return render_rest(request, rest_id)


def render_rest(request, rest_id, additional_context={}):

    rest = get_object_or_404(Restaurant, id=rest_id)

    context = {'rest': rest,
               'reviews': rest.review_set.order_by('-created_at'),
               **additional_context
               }

    return render(request, 'rest_reviews/restaurant.html', context)


@login_required(login_url='login')
def create_review(request, rest_id):
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            rest = get_object_or_404(Restaurant, id=rest_id)
            subject = form.cleaned_data['subject']
            stars = form.cleaned_data['stars']
            text = form.cleaned_data['text']
            image = form.cleaned_data['image']
            user_id = None
            if request.user.is_authenticated:
                user_id = request.user.id
            else: 
                user_id = 1
            author = User.objects.get(id=user_id)
            Review(rest_id=rest.id, subject=subject, text=text, author=author, review_image=image, stars=stars).save()
            return HttpResponseRedirect(reverse('rest_by_id', kwargs={'rest_id': rest_id}))
            
    else:  # GET
        form = ReviewForm()
    return render_rest(request, rest_id, {'form': form})
