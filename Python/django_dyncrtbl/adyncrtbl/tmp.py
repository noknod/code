http://ryanberg.net/blog/2008/jun/24/basics-creating-tumblelog-django/



------

from django.db import models
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
 
 
class GlobalPermissionManager(models.Manager):
    def get_query_set(self):
        return super(GlobalPermissionManager, self).\
            get_queryset().filter(content_type__name='APP')
 
# it should be created once
ct, created = ContentType.objects.get_or_create(
    name="app", app_label='app'
)
 
class GlobalPermission(Permission):
    """A global permission, not attached to a model"""
    objects = GlobalPermissionManager()
 
    class Meta:
        proxy = True
 
    def save(self, *args, **kwargs):
        self.content_type = ct
        super(GlobalPermission, self).save(*args, **kwargs)
 
 
def register_permission(code, namespace='app'):
    '''Create custom permissions in django'''
    perm, created = Permission.objects.get_or_create(
        content_type=ct,
        codename=code,
    )
    return perm
 
 
#register_permission('show_mainpage2')
#permission_required('app.show_mainpage2')