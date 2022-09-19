from django.contrib import admin
from .models import Links, Statistic, UsersInfo
from constance.admin import ConstanceAdmin, ConstanceForm, Config


# start config page module
class CustomConfigForm(ConstanceForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ConfigAdmin(ConstanceAdmin):
    change_list_form = CustomConfigForm
# end config page module


class StatisticAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'numbers_of_visits_shortened_link']


class LinksAdmin(admin.ModelAdmin):
    list_display = ['original_link', 'shortened_link']


class LinksToUserAdmin(admin.TabularInline):
    model = Links
    fields = ['original_link', 'shortened_link']
    max_num = 0


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['ip']
    inlines = [LinksToUserAdmin]


admin.site.register(Links, LinksAdmin)
admin.site.register(UsersInfo, UserInfoAdmin)
admin.site.register(Statistic, StatisticAdmin)
# start config page module
admin.site.unregister([Config])
admin.site.register([Config], ConfigAdmin)
# end config page module
