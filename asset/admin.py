from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(CustomUser)



@admin.register(Assets)
class AssetsAdmin(admin.ModelAdmin):
    list_display=['id','title','total_count','available_count']
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display=['id','name','position']    

@admin.register(UpdateAssets)
class UpdateAssetAdmin(admin.ModelAdmin):
    list_display=['id','assets','count']

@admin.register(AssetAsign)
class AssetAssignAdmin(admin.ModelAdmin):
    list_display=['id','employee','create_at']

@admin.register(AssetReturn)
class AssetReturnAdmin(admin.ModelAdmin):
    list_display=['id','employee',]

@admin.register(BadAsset)
class BadAssetAdmin(admin.ModelAdmin):
    list_display=['id','asset','count']