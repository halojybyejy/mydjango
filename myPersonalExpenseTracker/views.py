import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from .models import Post, Member, Account, Category, Tag
from .forms import SignUpForm, TransactionForm, AccountForm, CategoryForm, TagForm

logger = logging.getLogger('django')


def index(request):
    posts = Post.objects.all()
    return render(request, 'index.html', {'posts': posts})


class MyLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return '/home/'


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')  # Redirect to the home page after signup
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def protected_view(request):
    return render(request, 'protected.html')    

@login_required
def home(request):
    accounts = Account.objects.filter(user=request.user).exclude(type='total')
    total_balance = sum(account.balance for account in accounts)
    
    # Create a virtual Total Account for display purposes
    total_account = {
        'name': 'Total Account',
        'balance': total_balance,
        'user': request.user,
    }
    
    return render(request, 'home.html', {
        'accounts': accounts,
        'total_account': total_account,
    })

def member(request):
    mymembers = Member.objects.all()
    template = loader.get_template('member.html')
    context = {
        'mymembers': mymembers,
    }
    # logger.debug(context)
    return HttpResponse(template.render(context, request))      

@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, request.FILES)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            form.save_m2m()  # Save the many-to-many data for tags
            return redirect('home')
    else:
        form = TransactionForm(user=request.user)
    return render(request, 'add_transaction.html', {'form': form})

@login_required
def manage_accounts(request):
    # Handle form submission for adding new accounts
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            new_account = form.save(commit=False)
            new_account.user = request.user
            new_account.type = 'user'  # Set the type to 'user' for new accounts
            new_account.save()
            return redirect('manage_accounts')
    else:
        form = AccountForm()
    
    # Fetch all user accounts excluding the 'main' and 'total' accounts
    accounts = Account.objects.filter(user=request.user).exclude(type__in=['main', 'total'])
    main_account = Account.objects.get(user=request.user, type='main')
    total_account = Account.objects.get(user=request.user, type='total')

    return render(request, 'manage_accounts.html', {
        'form': form,
        'accounts': accounts,
        'main_account': main_account,
        'total_account': total_account,
    })

@login_required
def delete_account(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    if account.type == 'user':  # Only allow deletion of user-created accounts
        account.delete()
    return redirect('manage_accounts')

@login_required
def manage_categories(request):
    # Handle form submission for adding new categories
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            new_category = form.save(commit=False)
            new_category.user = request.user
            new_category.save()
            return redirect('manage_categories')
    else:
        form = CategoryForm()

    # Fetch all user categories
    user_categories = Category.objects.filter(user=request.user)

    return render(request, 'manage_categories.html', {
        'form': form,
        'user_categories': user_categories,
    })

@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id, user=request.user)
    category.delete()
    return redirect('manage_categories')

@login_required
def manage_tags(request):
    # Handle form submission for adding new tags
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            new_tag = form.save(commit=False)
            new_tag.user = request.user
            new_tag.save()
            return redirect('manage_tags')
    else:
        form = TagForm()

    # Fetch all user tags
    user_tags = Tag.objects.filter(user=request.user)

    return render(request, 'manage_tags.html', {
        'form': form,
        'user_tags': user_tags,
    })

@login_required
def delete_tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id, user=request.user)
    tag.delete()
    return redirect('manage_tags')