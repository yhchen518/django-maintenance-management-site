from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'partserver'
urlpatterns = [
	path('', views.index, name='index'),
	path('lines/<int:pk>', views.LineDetailView.as_view(), name='line-detail'),
	path('parts/', views.PartListView.as_view(), name='parts'),
	path('parts/<int:pk>', views.PartDetailView.as_view(), name='part-detail'),
	path('part/create/', views.PartCreate.as_view(), name='part_create'),
    path('part/<int:pk>/update/', views.PartUpdate.as_view(), name='part_update'),
    path('part/<int:pk>/delete/', views.PartDelete.as_view(), name='part_delete'),
    path('schematics/', views.SchematicListView.as_view(), name='schematics'),
	path('schematic/create/', views.SchematicCreate.as_view(), name='schematic_create'),
	path('schematic/<int:pk>/update/', views.SchematicUpdate.as_view(), name='schematic_update'),
	path('schematic/<int:pk>/delete/', views.SchematicDelete.as_view(), name='schematic_delete'),
	path('manuals/', views.ManualListView.as_view(), name='manuals'),
	path('manual/create/', views.ManualCreate.as_view(), name='manual_create'),
	path('manual/<int:pk>/update/', views.ManualUpdate.as_view(), name='manual_update'),
	path('manual/<int:pk>/delete/', views.ManualDelete.as_view(), name='manual_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)