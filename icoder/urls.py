from django.contrib import admin
from django.urls import path,include

admin.site.site_header = "iCoder Admin"
admin.site.site_title = " iCoder Admin Panel"
admin.site.index_title = "Welcome to iCoder Admin Panel"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('home.urls')),
    path('blog/', include('blog.urls')),
]
