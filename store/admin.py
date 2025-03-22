from django.contrib import admin
from .models import Product,Variation

# Register your models here.
class productAdmin(admin.ModelAdmin):
    list_display=('product_name','price','stock','is_available','category','modified_date')
    prepopulated_fields={
        'slug':('product_name',)
    }
    list_display_links=('modified_date','product_name')


class varitationAdmin(admin.ModelAdmin):
    list_display=('product','variation_category','varation_value','is_active','created_date')
    list_editable=('is_active',)
    list_filter=('product','variation_category','varation_value')
  

admin.site.register(Product,productAdmin)
admin.site.register(Variation,varitationAdmin)