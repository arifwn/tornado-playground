
from django.contrib.auth.models import User

from tastypie.authentication import BasicAuthentication, ApiKeyAuthentication, MultiAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource, Resource
import tastypie.fields

from testapp.models import Registrant

class UserResource(ModelResource):
    class Meta:
        #queryset = User.objects.filter(is_active=True)
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['password', 'is_active', 'is_staff', 'is_superuser']
        allowed_methods = ['get']
        filtering = {
            "username": 'exact',
            "email": 'exact',
        }
        
        # pass username=<user>&api_key=<key> in GET or POST or
        # set HTTP header Authorization: ApiKey <username>:<api_key>
        
        #authentication = MultiAuthentication(BasicAuthentication(), ApiKeyAuthentication())
        #authorization = DjangoAuthorization()
        

class RegistrantResource(ModelResource):
    class Meta:
        queryset = Registrant.objects.all()
        resource_name = 'registrant'


class AuthResource(Resource):
    '''
    Used to authenticate username and password pair.
    Usage: pass auth-username and auth-password pair in GET or POST request
    '''
    
    id = tastypie.fields.IntegerField(attribute='id')
    pk = tastypie.fields.IntegerField(attribute='pk')
    username = tastypie.fields.CharField(attribute='username')
    email = tastypie.fields.CharField(attribute='email')
    first_name = tastypie.fields.CharField(attribute='first_name')
    last_name = tastypie.fields.CharField(attribute='last_name')
    last_login = tastypie.fields.DateTimeField(attribute='last_login')
    date_joined = tastypie.fields.DateTimeField(attribute='date_joined')
    
    class Meta:
        resource_name = 'auth'
        object_class = User
        allowed_methods = ['get', 'post']
        
        # permission:
        # pass username=<user>&api_key=<key> in GET or POST or
        # set HTTP header Authorization: ApiKey <username>:<api_key>
        
        #authentication = MultiAuthentication(BasicAuthentication(), ApiKeyAuthentication())
        #authorization = DjangoAuthorization()
        
    def authenticate(self, username, password):
        from django.contrib.auth import authenticate
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                return user
            else:
                return None
        else:
            return None
    
    def authenticate_request(self, request):
        username = request.REQUEST.get('auth-username')
        password = request.REQUEST.get('auth-password')
        
        if (username is not None) and (password is not None):
            print username, password
            user = self.authenticate(username, password)
            return user
        
        return None
    
    def detail_uri_kwargs(self, bundle_or_obj):
        from tastypie.bundle import Bundle
        kwargs = {}
        print bundle_or_obj, type(bundle_or_obj)
        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.id
        else:
            kwargs['pk'] = bundle_or_obj.id
            
        return kwargs
    
    def get_object_list(self, request):
        obj_list = []
        user = self.authenticate_request(request)
        if user is not None:
            obj_list.append(user)
        return obj_list
    
    def obj_get_list(self, request=None, **kwargs):
        return self.get_object_list(request)
    
    def obj_get(self, request=None, **kwargs):
        print ">>>>", kwargs['pk']
        return User.objects.get(pk=kwargs['pk'])
    
    def obj_create(self, bundle, request=None, **kwargs):
        pass
    
    def obj_update(self, bundle, request=None, **kwargs):
        pass
    
    def obj_delete_list(self, request=None, **kwargs):
        pass
    
    def obj_delete(self, request=None, **kwargs):
        pass
    
    def rollback(self, bundles):
        pass
    