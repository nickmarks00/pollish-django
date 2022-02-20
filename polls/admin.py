from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from polls.forms import PollForm
from users.models import Profile, User
from .models import Poll, Choice, Comment


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    # Change form
    autocomplete_fields = ['poll']
    fields = ['choice_text', 'votes', 'choice_image', 'poll']

    list_display = ['choice_text', 'poll_link', 'votes', 'choice_image']
    list_editable = []
    list_per_page = 50
    list_select_related = ['poll']

    ordering = ['-votes']

    search_fields = ['choice_text', 'poll__question_text']

    @admin.display(ordering='poll')
    def poll_link(self, choice:Choice):
        #TODO change so it filters the profile list rather than entering change view
        url = (
            reverse('admin:polls_poll_changelist')
            + str(choice.poll.id)
            + '/change'
        )
        return format_html(f'<a href={url}>{choice.poll.id}</a>')


class ChoiceInline(admin.TabularInline):
    model = Choice

class CommentInline(admin.TabularInline):
    model = Comment




@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    # Change form
    autocomplete_fields = ['profile']
    fields = ['question_text', 'created_at','updated_at', 'profile']
    readonly_fields = ['created_at', 'updated_at']
    

    #Change list
    list_display = ['question_text', 'created_at', 'updated_at', 'profile_link', 'choices_count', 'total_votes', 'comments_count']
    list_editable = []
    list_per_page = 10
    list_prefetch_related = ['comments', 'choices']  #this is currently not doing anything...

    ordering = ['-created_at', 'profile']

    search_fields = ['question_text', 'profile__user__username']

    @admin.display(ordering='choice')
    def choices_count(self, poll):
        return poll.choices.count()
    
    @admin.display(ordering='comment')
    def comments_count(self, poll):
        return poll.comments.count()
    
    @admin.display(ordering='profile')
    def profile_link(self, poll):
        #TODO change so it filters the profile list rather than entering change view
        url = (
            reverse('admin:users_profile_changelist')
            + str(poll.profile.id)
            + '/change'
        )
        return format_html(f'<a href={url}>{poll.profile.user.username}</a>')
    
    @admin.display(ordering='total_votes')
    def total_votes(self, poll):
        return sum([choice.votes for choice in poll.choices.all() ])
    



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # Change form
    autocomplete_fields = ['poll', 'profile']
    fields = ['comment_text', 'created_at', 'profile', 'poll']
    readonly_fields = ['created_at']

    # Change list
    list_display = ['comment_text', 'created_at', 'poll_link', 'profile_link']
    list_editable = []
    list_per_page = 100
    list_select_related = ['profile', 'poll', 'profile__user']

    ordering = ['-created_at']

    search_fields = ['comment_text', 'poll__question_text', 'profile__user__username']

    @admin.display(ordering='poll')
    def poll_link(self, comment:Comment):
        #TODO change so it filters the profile list rather than entering change view
        url = (
            reverse('admin:polls_poll_changelist')
            + str(comment.poll.id)
            + '/change'
        )
        return format_html(f'<a href={url}>{comment.poll.id}</a>')
    
    @admin.display(ordering='profile')
    def profile_link(self, comment:Comment):
        #TODO change so it filters the profile list rather than entering change view
        url = (
            reverse('admin:users_profile_changelist')
            + str(comment.profile.id)
            + '/change'
        )
        return format_html(f'<a href={url}>{comment.profile.user.username}</a>')
