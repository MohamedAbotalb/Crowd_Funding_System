from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import Category
from .forms import CategoryForm


def category_index(request):
    categories = Category.get_all_categories()
    return render(request, 'categories/index.html', {'categories': categories})


def category_show(request, name):
    category = Category.get_category_by_name(name)
    return render(request, 'categories/show.html', {'category': category})


@login_required(login_url='login_')
def category_create(request):
    if not request.user.is_superuser:
        return redirect('category_index')

    form = CategoryForm()
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_index')

    return render(request, 'categories/create.html', {'form': form})


@login_required(login_url='login_')
def category_update(request, name):
    if not request.user.is_superuser:
        return redirect('category_index')

    category = Category.get_category_by_name(name)
    form = CategoryForm(instance=category)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_index')

    return render(request, 'category/update.html', context={"form": form})


@login_required(login_url='login_')
def category_delete(request, name):
    if not request.user.is_superuser:
        return redirect('category_index')

    category = get_object_or_404(Category, name=name)
    category.delete()
    return redirect('category_index')
