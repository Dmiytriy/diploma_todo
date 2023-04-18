from django.contrib import admin
from todolist.goals.models import GoalCategory, Goal, Board


@admin.register(GoalCategory)
class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created', 'updated')
    search_fields = ('title',)
    list_filter = ('is_deleted',)


@admin.register(Goal)
class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created', 'updated')
    search_fields = ('title', 'discription')
    list_filter = ('status', 'priority')


@admin.register(Board)
class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created', 'updated')
    search_fields = ('title', )
    list_filter = ('is_deleted',)
