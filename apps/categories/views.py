from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Category
from .forms import CategoryForm
from apps.projects.models import Project


def category_index(request):
    categories = Category.get_all_categories()
    projects = Project.objects.all().filter(status='active')
    return render(request, 'categories/index.html', {'categories': categories, 'projects': projects})


def category_show(request, slug):
    category = Category.get_category_by_slug(slug)
    projects = Project.objects.filter(category=category,status='active')
    return render(request, 'categories/show.html', {'category': category, 'projects': projects})


@login_required(login_url='login_')
def category_create(request):
    if not request.user.is_superuser:
        return redirect('category_index')

    form = CategoryForm()
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_show', slug=form.cleaned_data['slug'])

    return render(request, 'categories/create.html', {'form': form})


@login_required(login_url='login_')
def category_update(request, slug):
    if not request.user.is_superuser:
        return redirect('category_index')

    category = Category.get_category_by_slug(slug)
    form = CategoryForm(instance=category)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_show', slug=category.slug)

    return render(request, 'categories/update.html', context={"form": form})


@login_required(login_url='login_')
def category_delete(request, slug):
    if not request.user.is_superuser:
        return redirect('category_index')

    category = get_object_or_404(Category, slug=slug)
    category.delete()
    return redirect('category_index')
