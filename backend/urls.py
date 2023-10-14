"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include, re_path
from rest_framework import routers
from assets import views

router = routers.DefaultRouter()

router.register(r'client', views.clientViewSet, basename="client")
router.register(r'upload', views.UploadViewSet, basename="upload")
#route set for FirebaseDB Connection
router.register(r'firebasedb', views.FirebaseViewSet, basename="firebasedb")
#route set for GitHub Connection
router.register(r'gitprivate', views.gitprivateSet, basename="gitprivate")
router.register(r'gitpublic', views.gitpublicSet, basename="gitpublic")
#route set for MariaDB Connection
router.register(r'mariadbList', views.mariadb_ListSet, basename="mariadbList")
router.register(r'mariadbtables', views.mariadb_TableSet, basename="mariadbtables")
router.register(r'mariadb', views.mariadbSet, basename="mariadb")
#route set for MongoDB Connection
router.register(r'mongodbList', views.mongodb_ListSet, basename="mongodbList")
router.register(r'mongodbCollection', views.mongodb_CollectionSet, basename="mongodbCollection")
router.register(r'mongodb', views.mongodbSet, basename="mongodb")
#route set for MS SQL Server Connection
router.register(r'sqlServerList', views.MSsql_ListSet, basename="sqlServerList")
router.register(r'sqlServertables', views.MSsql_TableSet, basename="sqlServertables")
router.register(r'sqlServer', views.MSsqlViewSet, basename="sqlServer")
#route set for MySQL Connection
router.register(r'mysqlList', views.mysql_ListSet, basename="mysqldbList")
router.register(r'mysqltables', views.mysql_TableSet, basename="mysqldbtables")
router.register(r'mysqldb', views.mysqlViewSet, basename="mysqldb")
#route set for PostgreSQL Connection
router.register(r'postgrestables', views.postgres_TableSet, basename="postgrestables")
router.register(r'postgresdb', views.postgresSet, basename="postgresdb")
#route set for SQLite DB Connection
router.register(r'sqlitetables', views.SQLite_TableSet, basename="sqlitetables")
router.register(r'sqlitedb', views.SQLiteViewSet, basename="sqlitedb")
#route set for scrape data through APIs & Webs
router.register(r'webapis', views.ApisViewSet, basename="webapis")
router.register(r'webscrapping', views.ApisViewSet, basename="webscrapping")
#route set for Data Transformation
router.register(r'columndtypes', views.ColumnsdtypeViewSet, basename="columndtypes")
router.register(r'columndedits', views.ColumnEditViewSet, basename="columndedits")
router.register(r'columnfilters', views.ColumnFiltersViewSet, basename="columnfilters")
router.register(r'uploadconcate', views.concatViewSet, basename="uploadconcate")
router.register(r'uploadmerge', views.mergingViewSet, basename="uploadmerge")
router.register(r'aggfunc', views.aggregateViewSet, basename="aggfunc")
router.register(r'visualize', views.VisualizeViewSet, basename="visualize")
#route set for ORM
router.register(r'AllDataSet', views.AllDataSetViewSet, basename="AllDataSet")
router.register(r'deletedb', views.DeleteDBViewSet, basename="deletedb"),
router.register(r'editdb', views.EditDBViewSet, basename="editdb")
router.register(r'SaveFileDB', views.SaveFileDBViewSet, basename="SaveFileDB")

# route set for User Authentication
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    re_path(r'^api/user_register', views.UserRegistration.as_view()),
    re_path(r'^api/userView', views.UserView.as_view()),
    re_path(r'^api/user/(?P<pk>[0-9]+)$', views.UserList.as_view()),
    re_path(r'^api/login', views.LoginView.as_view(), name='login'),
    re_path(r'^api/logout', views.Logout.as_view()),
    re_path(r'^api/change_pass/(?P<pk>[0-9]+)$', views.ChangePassword.as_view()),
    # re_path(r'^api/forget', views.ForgetPassword().as_view()),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)