from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from .forms import GrabberForm
from imgurpython import ImgurClient
from datetime import datetime
from .models import Grabber
import praw
import json
from django.conf import settings


@user_passes_test(lambda u: u.is_superuser)
def index(request):
    return render(request, 'webapp/index.html')


@user_passes_test(lambda u: u.is_superuser)
def post_list(request):
    grabber_data = Grabber.objects.order_by('-time_added')
    form = GrabberForm()
    # form = GrabberForm()
    return render(request, 'webapp/post_list.html', {
        'grabber_data': grabber_data,
        'form': form,
    })


@user_passes_test(lambda u: u.is_superuser)
def post_detail(request, pk):
    # form = GrabberForm()
    return render(request, 'webapp/post_detail.html', {
        'pk': pk,
    })


@user_passes_test(lambda u: u.is_superuser)
def create_post(request):
    if request.method == 'POST':
        # image_id = request.POST.get('image_id')
        form = GrabberForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.time_added = datetime.now()
            post.downloaded = False
            post.save()
            response_data = {}
            response_data['result'] = 'Create post successful!'
            response_data['image_id'] = post.image_id
            response_data['description'] = post.description
            response_data['url'] = post.url
            response_data['time_added'] = post.time_added.strftime('%B %d, %Y %I:%M %p')

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


def post_new(request):
    if request.method == "POST" and request.is_ajax:
        form = GrabberForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.time_added = datetime.now()
            post.save()
            # return redirect('post_detail', pk=post.pk)
            print request.POST
            print request.is_ajax
            return HttpResponse(
                json.dumps(request.POST),
                content_type="application/json"
            )
    else:
        form = GrabberForm()
    return render(request, 'webapp/post_edit.html', {'form': form})


@user_passes_test(lambda u: u.is_superuser)
def imgur(request, section='user', sort='rising', page=0):
    if request.method == "POST":
        form = GrabberForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.time_added = datetime.now()
            post.downloaded = False
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = GrabberForm()
    page = int(page)
    client_id = getattr(settings, 'IMGUR_CLIENT_ID', '')
    client_secret = getattr(settings, 'IMGUR_CLIENT_TOKEN', '')
    client = ImgurClient(client_id, client_secret)
    current_limits = client.credits
    items = client.gallery(section=section, sort=sort, page=page, show_viral=True)
    album_images = {}
    form = GrabberForm()
    # images = client.get_album_images(items[1].id)
    # Grab all the images in album
    for item in items:
        if item.is_album is True:
            id = item.id
            images = client.get_album_images(item.id)
            album_images[id] = images
            # album_images[id] = "test"

    return render(request, 'webapp/dashboard.html', {
        'items': items,
        'current_limits': current_limits,
        'album_images': album_images,
        'section': section,
        'sort': sort,
        'page': page,
        'form': form,

    })


@user_passes_test(lambda u: u.is_superuser)
def reddit(request, sort="hot"):
    reddit = praw.Reddit(user_agent="u_aww")
    subreddit = reddit.get_subreddit("aww")
    if sort == "hot":
        submissions = subreddit.get_hot(limit=50)
    if sort == "top":
        submissions = subreddit.get_top(limit=50)
    if sort == "new":
        submissions = subreddit.get_new(limit=50)

    form = GrabberForm()
    return render(request, 'webapp/reddit.html', {
        'submissions': submissions,
        'form': form,
    })
