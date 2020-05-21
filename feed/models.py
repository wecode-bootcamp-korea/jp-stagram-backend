from django.db import models
from account.models import Account


class Feed(models.Model):
    account = models.ForeignKey(
        'account.Account', on_delete=models.SET_NULL, null=True)
    content = models.TextField(max_length=3000)
    liked = models.ManyToManyField(
        'account.Account', through='FeedLike', related_name='liked_feeds')
    comments = models.ManyToManyField(
        'account.Account', through='Comment', related_name='comments')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if len(self.content) > 20:
            return self.content[:20]
        return self.content

    class Meta:
        db_table = 'feeds'


class Photo(models.Model):
    feed = models.ForeignKey('Feed', on_delete=models.SET_NULL, null=True)
    image_url = models.URLField(max_length=2000)

    class Meta:
        db_table = 'photos'


class Comment(models.Model):
    feed = models.ForeignKey('Feed', on_delete=models.SET_NULL, null=True)
    account = models.ForeignKey(
        'account.Account', on_delete=models.SET_NULL, null=True)
    liked = models.ManyToManyField(
        'account.Account', through='CommentLike', related_name='liked_comments')
    content = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if len(self.content) > 20:
            return self.content[:20]
        return self.content

    class Meta:
        db_table = 'comments'


class FeedLike(models.Model):
    account = models.ForeignKey(
        'account.Account', on_delete=models.SET_NULL, null=True)
    feed = models.ForeignKey('Feed', on_delete=models.SET_NULL, null=True)
    # has_liked = models.BooleanKey()...

    class Meta:
        db_table = 'feed_likes'


class CommentLike(models.Model):
    account = models.ForeignKey(
        'account.Account', on_delete=models.SET_NULL, null=True)
    comment = models.ForeignKey(
        'Comment', on_delete=models.SET_NULL, null=True)
    # has_liked = models.BooleanKey()...

    class Meta:
        db_table = 'comment_likes'
