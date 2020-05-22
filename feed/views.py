import json
import jwt

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponse

from jp_stagram.utils import login_decorator
from feed.models import Feed, Comment


class FeedView(View):  # returns all instagram feeds on main page
    @login_decorator
    def get(self, request):
        user = request.user
        feeds = list(user.to_user.feed_set.all())
        feeds_values = []
        for feed in feeds:
            feed_values = {}
            feed_values['username'] = feed.account.username
            feed_values['content'] = feed.content
            feed_values['created_at'] = feed.created_at
            feed_values['image_url'] = list(feed.photo_set.all())
            feeds_values.append(feed_values)

        return JsonResponse({"all_feeds": feeds_values}, status=200)


# class PostView(View):  # returns a single instagram post
#    @login_decorator
#    def get(self, request):
#
#    def post(self, request):


class CommentView(View):
    @login_decorator
    def get(self, request):
        # user = request.user
        # feed = user.feed_set.get(pk=2)
        # feed_comments = list(feed.comments.all())
        feed_comments = list(Comment.objects.all())
        all_comments = []
        for comment in feed_comments:
            comment_values = {}
            comment_values['username'] = comment.account.username
            comment_values['content'] = comment.content
            all_comments.append(comment_values)

        # Additionally needs to return post image url, profile image url, username, post content
        # feed_values = {}
        # feed_values['username'] = feed.account.username
        # feed_values['content'] = feed.content
        # feed_values['created_at'] = feed.created_at
        # feed_values['image_url'] = feed.photo_set.get(pk=1)
        # feed_values['avatar_url'] = user.avatar

        return JsonResponse({'comments': all_comments}, status=200)

    @login_decorator
    def post(self, request):
        user = request.user
        data = json.loads(request.body)
        try:
            """
            new_comment = Comment(
                feed=Feed.objects.get(id=data['feed_id']),
                account=user,
                content=data['text']
            )
            new_comment.save()
            comments = list(new_comment.feed.comment_set.all())
            all_comments = []
            for comment in comments:
                comment_values = {}
                comment_values['username'] = comment.account.username
                comment_values['content'] = comment.content
                all_comments.append(comment_values)
            """
            Comment.objects.create(feed=Feed.objects.get(
                id=data['feed_id']), account=user, content=data['text'])
            comments = list(Comment.objects.all())
            all_comments = []
            for comment in comments:
                comment_values = {}
                comment_values['username'] = comment.account.username
                comment_values['content'] = comment.content
                all_comments.append(comment_values)
            return JsonResponse({'comments': all_comments}, status=200)
        except KeyError:
            return JsonResponse({'message': 'INVALID_KEY'}, status=400)
