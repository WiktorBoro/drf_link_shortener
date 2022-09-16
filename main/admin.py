from django.contrib import admin
from .models import Links, Statistic, UsersInfo
from constance.admin import ConstanceAdmin, ConstanceForm, Config


class CustomConfigForm(ConstanceForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ConfigAdmin(ConstanceAdmin):
    change_list_form = CustomConfigForm


# class LinksAdmin(admin.ModelAdmin):
#     @admin.display(ordering='statistic__numbers_of_visits_shortened_link',
#                    description='Link statistic')
#     def get_link_statistic(self, obj):
#         return obj.statistic.numbers_of_visits_shortened_link
#
#     fields = ['original_link', 'shortened_link', 'get_link_statistic']


class LinksToUserAdmin(admin.TabularInline):
    model = Links
    fields = ['original_link', 'shortened_link']
    max_num = 0


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['ip']
    inlines = [LinksToUserAdmin]

#
# class StatisticAdmin(admin.ModelAdmin):
#     list_display = ['shortened_link', 'numbers_of_visits_shortened_link']


admin.site.register(Links)
admin.site.register(UsersInfo, UserInfoAdmin)
admin.site.register(Statistic)
admin.site.unregister([Config])
admin.site.register([Config], ConfigAdmin)
