from django.contrib import admin
from blog.models import *
# Register your models here.

# # @admin.register(Book)#----->单给某个表加一个定制
# class MyAdmin(admin.ModelAdmin):
#     list_display = ("title","price","publisher")
#     search_fields = ("title","publisher")
#     list_filter = ("publisher",)
#     ordering = ("price",)
#     fieldsets =[
#         (None,               {'fields': ['title']}),
#         ('price information', {'fields': ['price',"publisher"], 'classes': ['collapse']}),
#     ]
#
# admin.site.register(Book,MyAdmin)
# admin.site.register(Publisher)
# admin.site.register(Author)

admin.site.register(Test)
