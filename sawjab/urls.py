from django.conf.urls import url,include
from django.contrib import admin
from accounts import views as account_view
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
	url(r'^$',views.index_redirect),
    url(r'^admin/', admin.site.urls),
    url(r'^posts/',include("posts.urls",namespace="posts")), 
    url(r'^main/',include("main.urls",namespace="main")),
    url(r'^search/',views.SearchView.as_view(),name="search"),
    url(r'^account/',include("accounts.urls",namespace="accounts")), 
    url(r'^ajax/autocomplete/$', views.autocomplete, name='ajax_autocomplete'),
    url(r'^tinymce/', include('tinymce.urls')),
]
if settings.DEBUG:
	urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
	urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
	
