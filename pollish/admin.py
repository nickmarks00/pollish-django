from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse


from .forms import PollForm
from .models import Poll, Choice, Comment, Profile


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    # Change form
    autocomplete_fields = ['poll']
    fields = ['choice_text', 'votes', 'choice_image', 'poll']

    list_display = ['choice_text', 'poll_link', 'votes']
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
    autocomplete_fields = ['user']
    fields = ['question_text', 'created_at','updated_at', 'user']
    readonly_fields = ['created_at', 'updated_at']
    

    #Change list
    list_display = ['question_text', 'created_at', 'updated_at', 'user_link', 'choices_count', 'total_votes', 'comments_count']
    list_editable = []
    list_per_page = 10
    list_prefetch_related = ['comments', 'choices']  #this is currently not doing anything...

    ordering = ['-created_at', 'user']

    search_fields = ['question_text', 'user__username']

    @admin.display(ordering='choice')
    def choices_count(self, poll):
        return poll.choices.count()
    
    @admin.display(ordering='comment')
    def comments_count(self, poll):
        return poll.comments.count()
    
    @admin.display(ordering='user')
    def user_link(self, poll):
        #TODO change so it filters the profile list rather than entering change view
        url = (
            reverse('admin:users_user_changelist')
            + str(poll.user.id)
            + '/change'
        )
        return format_html(f'<a href={url}>{poll.user.username}</a>')
    
    @admin.display(ordering='total_votes')
    def total_votes(self, poll):
        return sum([choice.votes for choice in poll.choices.all() ])


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # Change form
    autocomplete_fields = ['user']
    fields = ['user', 'created_at', 'updated_at', 'avatar', 'bio']
    readonly_fields = ['updated_at', 'created_at']

    # Change list
    list_display = ['user', 'updated_at', 'avatar',  'bio']
    list_editable = []
    list_per_page = 25

    search_fields = ['user__username']



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # Change form
    autocomplete_fields = ['poll', 'user']
    fields = ['comment_text', 'created_at', 'user', 'poll']
    readonly_fields = ['created_at']

    # Change list
    list_display = ['comment_text', 'created_at', 'poll_link', 'user_link']
    list_editable = []
    list_per_page = 100
    list_select_related = ['poll', 'user']

    ordering = ['-created_at']

    search_fields = ['comment_text', 'poll__question_text', 'user__username']

    @admin.display(ordering='poll')
    def poll_link(self, comment:Comment):
        #TODO change so it filters the profile list rather than entering change view
        url = (
            reverse('admin:polls_poll_changelist')
            + str(comment.poll.id)
            + '/change'
        )
        return format_html(f'<a href={url}>{comment.poll.id}</a>')
    
    @admin.display(ordering='user')
    def user_link(self, comment:Comment):
        #TODO change so it filters the profile list rather than entering change view
        url = (
            reverse('admin:users_user_changelist')
            + str(comment.user.id)
            + '/change'
        )
        return format_html(f'<a href={url}>{comment.user.username}</a>')
