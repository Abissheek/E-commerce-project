from django.contrib import admin
from .models import Product

# Register your models here.
class productAdmin(admin.ModelAdmin):
    list_display=('product_name','price','stock','is_available','category','modified_date')
    prepopulated_fields={
        'slug':('product_name',)
    }
    list_display_links=('modified_date','product_name')
  

admin.site.register(Product,productAdmin)