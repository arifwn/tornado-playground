
from django.conf.urls.defaults import patterns, include, url
from tastypie.api import Api
from exposer.api import UserResource, RegistrantResource, AuthResource

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(RegistrantResource())
v1_api.register(AuthResource())

urlpatterns = patterns('',
    url(r'^', include(v1_api.urls)),
)
