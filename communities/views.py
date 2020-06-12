from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import ReviewForm, CommentForm
from .models import Review, Comment

# Create your views here.
def review_list(request):
    reviews = Review.objects.order_by('-pk')
    context = {
        'reviews': reviews,
    }
    return render(request, 'communities/review_list.html', context)


@login_required
def new_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('communities:review_detail', review.pk)
        messages.warning(request, '다시 쓰세요.')
    else:
        form = ReviewForm()
    context = {
        'form': form,
    }
    return render(request, 'communities/form.html', context)


@login_required
def review_detail(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    form = CommentForm
    context = {
        'review':review,
        'form': form,
    }
    return render(request, 'communities/review_detail.html', context)


@login_required
def review_update(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if review.user == request.user:
        if request.method == 'POST':
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
                review.save()
                return redirect('communities:review_detail', review.pk)
            messages.warning(request, '다시 쓰세요.')
        else:
            form = ReviewForm(instance=review)
        context = {
            'form': form,
        }
        return render(request, 'communities/form.html', context)
    else:
        return redirect('communities:review_detail', review.pk)


@require_POST
@login_required
def review_delete(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.user == review.user:
        review.delete()
        return redirect('communities:review_list')
    else:
        return redirect('communities:review_detail', review.pk)


@require_POST
@login_required
def comments_create(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.review = review
        comment.save()
        return redirect('communities:review_detail', review.pk)


@login_required
def comments_delete(request, review_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
    return redirect('communities:review_detail', review_pk)