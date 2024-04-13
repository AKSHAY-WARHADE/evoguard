from django.contrib import admin
from .models import*

# Register your models here.
admin.site.register(Complaint)
admin.site.register(Queries)
admin.site.register(MyUser)
admin.site.register(Employee)



admin.site.site_header = 'Evo Guard'                   
admin.site.index_title = 'ADMIN'                 
admin.site.site_title = 'Evo Guard'                 



