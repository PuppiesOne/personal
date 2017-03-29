"""Write a method which will remove any given character from a target string. 
Don't use the String.replace() method in your solution. 
If the given character is not found in the target string,
your method should raise a CharacterNotFound exception.
"""

"""
class CharacterNotFound(Exception):

    def __init__(self, notFound):
        self.notFound = notFound

    def __str__(self):
    	return repr(self)

def removalfunction(target,toRemove):
    if not toRemove in target:
        raise CharacterNotFound(toRemove)
    else:
        removed = target.translate(None, toRemove)
        print removed

removalfunction('This is a strxing','y')
"""

"""Write a method that accepts a list argument and efficiently finds
 and returns a distinct list of any duplicate numbers in the list. 
 Include unit tests to verify correct output for a few test lists.
"""

"""
import unittest

def listDedupe(needsCleaning):
    
    checked = set()
    position = 0

    for i in xrange(len(needsCleaning)-1, -1, -1):
        y = needsCleaning[i]
        if y in checked:
            del needsCleaning[i]
        else:
            checked.add(y)
    print needsCleaning

class dupeTest(unittest.TestCase):
    def test(self):
        for i in listDedupe:
           self.assertEqual(listDedupe.count(i),1)

listDedupe([1,2,3,4,4,5,5,5,6,7,7])
"""

"""
Write a method that converts its argument from integer to roman numeral if a numeric value is passed, or from roman 
numeral to an integer if a roman numeral is passed.  Your solution should rely on the parameter's class to determine 
its type and if a non-roman numeral character is passed (i.e. 'M3I',) the method should raise a BadRomanNumeral exception.
The solution should be a single method that accepts a single argument and return the converted value.  
Additionally, your solution should demonstrate your mastery of Python's exception handling capabilities.
Include unit tests to verify correct conversion of both types of input, and verify exception output with bad input.
"""

"""
numerals = [(1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'), (100, 'C'), (90, 'XC'),
           (50, 'L'), (40, 'XL'), (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]

validletters = ('M','D','C','L','X','V','I')

class BadRomanNumeral(Exception):

    def __init__(self, notFound):
        self.notFound = notFound

    def __str__(self):
    	return repr(self)


def twowayconverter(toConvert):
    if isinstance(toConvert, int):
        return numtoroman(toConvert)
    else:
        return romantonum(toConvert)


def numtoroman(x):

    converted = ""

    if not (0 < x < 3999):
        raise BadRomanNumeral(x)

    if not isinstance(x, int):
        raise BadRomanNumeral(x)

    for integer, numeral in numerals:
        while x >= integer:
            converted += numeral
            x -= integer
    return converted


def romantonum(y):
    
    converted = 0
    pos = 0

    if not y:
        raise BadRomanNumeral(y)

    for i in y:
        if i not in validletters:
            raise BadRomanNumeral(i)

    for integer, numeral in numerals:
        while y[pos:pos + len(numeral)] == numeral:
            converted += integer
            pos += len(numeral)
    return converted


def tests():
   try: 
       twowayconverter('MCVI')
       print 'Test Succeeded for value MCVI'
   except: 
       print 'Test Failed for value MCVI'
   try:
       twowayconverter('MCVQI')
       print 'Test Succeeded for value MCVQI'
   except:
       print 'Test Failed for value MCVQI'
   try:
       twowayconverter('')
       print 'Test Succeeded for value (blank)'
   except:
       print 'Test Failed for value (blank)'
   try:
       twowayconverter(150)
       print 'Test Succeeded for value 150'
   except:
       print 'Test Failed for value 150'
   try:
       twowayconverter(4050)
       print 'Test Succeeded for value 4050'
   except:
       print 'Test Failed for value 4050'
   try:
       twowayconverter(0)
       print 'Test Succeeded for value 0'
   except:
       print 'Test Failed for value 0'
 
tests()
"""


"""Write a command line utility called gif2png that takes a single command line argument
(the name of a GIF file), opens the GIF file, converts the image format to PNG and
stores the converted image as a new PNG file in the current working directory.
"""

"""
from PIL import image
from optparse import OptionParser


def giftopng(options):
	im = Image.open(options.file_name)
	transparency = im.info['transparency'] 
	im.save('Jmiller.png', transparency=transparency)

if __name__ == '__main__':
	parser = OptionParser()
	parser.add_option("-f", "--file", dest="file_name", help="file name for the gif")
	options, args = parser.parse_args()
	giftopng(options)
"""


"""
Only provide a solution for this problem if you consider yourself a senior Django developer.

Create a Django-based web shopping list application designed for use by a single user.  
The application should use Django's ORM to persist the shopping list items to the data store.  
Each item should be stored as a single row in the data store.  The class to represent an item should be named ListItem.

The application should allow the user to add and delete items from their shopping list.  
Adding and removing items from the user's shopping list requires the user be authenticated.  
Use Django's built-in authentication system and function decorators to handle the user authentication.

Your solution should define a User class that represents the single user of the application, 
and should provide methods to get the total number of items on the user's shopping list and a 
list of the ListItem objects belonging to the user.
"""

"""
Settings.py 

from os import path
import sqlserver_ado

PROJECT_ROOT = path.dirname(path.abspath(path.dirname(__file__)))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = (
    #'localhost', 'PSCAPPP02002',
    #'10.2.177.226',
    #'10.2.177.226:9876',
    '*'

)

ADMINS = (
    ('John Miller', 'john.miller@mecglobal.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sql_server.pyodbc',
        'NAME': 'xxxxxx',
        'USER': 'xxxxx',
        'PASSWORD': 'xxxxx',
        'HOST': 'xxxx',
        'PORT': '',
        'OPTIONS': {
            'driver': 'SQL Server Native Client 11.0',
            'unicode_results': True,
        },
    }
}

LOGIN_URL = '/login'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = path.join(PROJECT_ROOT, 'static').replace('\\', '/')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'n(bd1f1c%e8=_xad02x5qtfn%wgwpi492e$8_erx+d)!tpeoim'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',

    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'PopRocks.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'PopRocks.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or
    # "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
    'rest_framework',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    #'sql_app',
    'corsheaders',
    'rest_framework_swagger',
    'rest_framework.authtoken',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Specify the default test runner.
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
    'PAGE_SIZE': 1000000,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        )
}

CORS_ORIGIN_ALLOW_ALL = True

#CORS_ORIGIN_WHITELIST = (
        #'10.2.177.226',
        #'10.2.177.226:9876',
        #'*'
#)


urls.py

from poprocks import views
from datetime import datetime
from django.conf.urls import patterns, url
from app.forms import BootstrapAuthenticationForm
# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
admin.autodiscover()
# for api authentication
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views


urlpatterns = patterns('',
    url(r'^api-token-auth/', views.obtain_auth_token),
    url(r'^login/$',
        'django.contrib.auth.views.login',
        {
            'template_name': 'app/login.html',
            'authentication_form': BootstrapAuthenticationForm,
            'extra_context':
            {
                'title':'Log in',
                'year':datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        'django.contrib.auth.views.logout',
        {
            'next_page': '/',
        },
        name='logout'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^shoplist/$',
        views.shopList.as_view(),
        name='shop-list'),

    url(r'^shoplist/(?P<pk>[0-9]+)/$',
        viewsca.shopList.as_view(),
        name='shop-list'),

    url(r'^users/$',
        viewsca.UserList.as_view(),
        name='user-list'),
    url(r'^users/$', viewsca.UserList.as_view()),

    url(r'^users/(?P<pk>[0-9]+)/$',
        viewsca.UserDetail.as_view(),
        name='user-detail'),

    url(r'^$', viewsca.api_root),

)

urlpatterns = format_suffix_patterns(urlpatterns)

Views.py

# Create your views here.
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from classifications.serializers import UserSerializer, ShopListSerializer
from poprocks.models import shoplist
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions
from rest_framework.permissions import IsOwnerOrReadOnly
from rest_framework.reverse import reverse
from rest_framework import renderers
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'shoplist': reverse('shop-list', request=request, format=format),
    })

class ShopList(generics.ListCreateAPIView):
    queryset = Feeds.objects.all()
    serializer_class = ShopListSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ShopListDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Feeds.objects.all()
    serializer_class = ShopListSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                      IsOwnerOrReadOnly,)
                      
                      
serializers.py

from django.contrib.auth.models import User
from rest_framework import serializers
from django.forms import widgets
from poprocks.models import LANGUAGE_CHOICES, STYLE_CHOICES, ShopList
from rest_framework_recursive.fields import RecursiveField
from django.forms.models import model_to_dict
import ast, json
from collections import OrderedDict

class UserSerializer(serializers.ModelSerializer):
    shoplist = serializers.PrimaryKeyRelatedField(many=True, queryset=Feeds.objects.all())

    class Meta:
        model = User
        fields = ('id', 'shoplist')


class ShopListSerializer(serializers.ModelSerializer):

    #extensions = serializers.RelatedField(source='extension', read_only=True)
    
    class Meta:
        model = ShopList
        fields = ('id', 'itemname', 'owner')

    def create(self, validated_data):
        return ShopList.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.itemname = validated_data.get('itemname', instance.itemname)
        instance.owner = validated_data.get('owner', instance.owner)
        instance.save()
        return instance

    owner = serializers.ReadOnlyField(source='owner.username')

admin.py

from django.contrib import admin
from poprocks.models import ShopList

admin.site.register(Feeds)

models.py

from django.db import models
from django.utils import timezone
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class Feeds(models.Model):
    itemname = models.CharField(max_length=125,null=False)
    owner = models.ForeignKey('auth.User', related_name='feeds')
    
class Meta:
    ordering = ('created',)
"""