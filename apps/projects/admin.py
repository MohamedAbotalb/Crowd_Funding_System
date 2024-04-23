from django.contrib import admin

from .models import Project, ProjectReport, CommentReport, Comment


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'total_target', 'current_fund', 'start_time', 'end_time', 'creator', 'category', 'rate', 'status', 'featured')
    list_filter = ('start_time', 'end_time', 'creator', 'category', 'featured')
    search_fields = ('title', 'category', 'creator')
    date_hierarchy = 'start_time'
    list_editable = ['featured']
    list_per_page = 10
    list_max_show_all = 10


class ProjectReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'reason', 'created_at')
    list_filter = ('user', 'project', 'created_at')
    search_fields = ('user', 'project', 'created_at')
    date_hierarchy = 'created_at'
    list_per_page = 10
    list_max_show_all = 10


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'text', 'created_at')
    list_filter = ('user', 'project', 'created_at')
    search_fields = ('user', 'project', 'created_at')
    date_hierarchy = 'created_at'
    list_per_page = 10
    list_max_show_all = 10


class CommentReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment', 'reason', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('user', 'created_at')
    date_hierarchy = 'created_at'
    list_per_page = 10
    list_max_show_all = 10


admin.site.register(Project, ProjectAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(ProjectReport, ProjectReportAdmin)
admin.site.register(CommentReport, CommentReportAdmin)
