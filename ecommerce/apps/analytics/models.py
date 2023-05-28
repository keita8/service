from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.db.models.query import QuerySet
from django.urls import reverse
from django.contrib.sessions.models import Session
from ecommerce.apps.analytics.utils import get_client_ip
from .signals import *
from ecommerce.apps.products.models import Product
from ecommerce.apps.order.models import Orders
from django.db.models.signals import *
from ecommerce.apps.account.signals import *
from django.contrib.auth.models import AnonymousUser






User = settings.AUTH_USER_MODEL 
FORCE_SESSION_TO_ONE = getattr(settings, 'FORCE_SESSION_TO_ONE', False)
FORCE_INACTIVE_USER_END_SESSION =  getattr(settings, 'FORCE_INACTIVE_USER_END_SESSION', False)



class ObjectViewedQuerySet(models.query.QuerySet):

    def by_model(self, model_class, model_queryset=False):
        
        c_type = ContentType.objects.get_for_model(model_class)
        qs = self.filter(content_type=c_type)
        
        if model_queryset:
            viewed_ids = [x.object_id for x in qs]
            return model_class.objects.filter(pk__in=viewed_ids)
        
        return qs



class ObjectViewedManager(models.Manager):

    def get_queryset(self) -> QuerySet:
        return ObjectViewedQuerySet(self.model, using=self._db)
    
    def by_model(self, model_class, model_queryset=False):
        return self.get_queryset().by_model(model_class, model_queryset=model_queryset)



class ObjectView(models.Model):
    user = models.ForeignKey(User,verbose_name='client', null=True, blank=True, on_delete=models.CASCADE)
    ip_address = models.CharField(max_length = 350, null=True, blank=True, verbose_name='adresse ip du client')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name='contenu')
    object_id = models.PositiveIntegerField(verbose_name='identifiant')
    content_object = GenericForeignKey('content_type', 'object_id')
    timestamp = models.DateTimeField("consulté le ", auto_now_add=True)
    
    
    objects = ObjectViewedManager()

    def __str__(self):
        return f"{self.content_object} vue le {self.timestamp:%d-%m-%Y à %H:%M}"
    
    
    class Meta:
        verbose_name = "Objet Vue"
        verbose_name_plural = "Objets Vues"
        ordering = ('-timestamp', )



class UserSession(models.Model):
    user = models.ForeignKey(User,verbose_name='client', null=True, blank=True, on_delete=models.CASCADE)
    ip_address = models.CharField(max_length = 350, null=True, blank=True, verbose_name='adresse ip')
    session_key = models.CharField(max_length = 150, null=True, blank=True, verbose_name='clé session')
    timestamp = models.DateTimeField("date de creation", auto_now_add=True)
    active = models.BooleanField(verbose_name='activé', default=True)
    ended = models.BooleanField(verbose_name="session terminée", default=False)

    def end_session(self):
        session_key = self.session_key
        ended = self.ended 
        try:
            Session.objects.get(pk=session_key).delete()
            self.ended = True
            self.active = False
            self.save()
        except:
            pass
        return self.ended

    class Meta:
        verbose_name = "Session client"
        verbose_name_plural = "Sessions client"

    def __str__(self):
        return f'{self.user}'





def post_save_user_change_receiver(sender, instance, created, *args, **kwargs):
    if not created:
        if instance.is_active == False:
            qs = UserSession.objects.filter(user=instance.user, active=False, ended=False)
            for i in qs:
                i.end_session()
                





def post_save_session_receiver(sender, instance, created, *args, **kwargs):
    if created:
        qs = UserSession.objects.filter(user=instance.user, active=False, ended=False).exclude(id=instance.id)
        for i in qs:
            i.end_session()
            
    if not instance.active and not instance.ended:
        instance.end_session()






def object_viewed_receiver(sender, instance, request, *args, **kwargs):
    c_type = ContentType.objects.get_for_model(sender)
    ip_address = None
    try:
        ip_address = get_client_ip(request)
    except:
        pass
    user = request.user
    new_view_instance = ObjectView.objects.create(
                user=request.user, 
                content_type=c_type,
                object_id=instance.id,
                ip_address=ip_address
                )





def user_logged_in_receiver(sender, instance, request, *args, **kwargs):
    print(instance)
    user = instance
    ip_address = get_client_ip(request)
    session_key = request.session.session_key
    UserSession.objects.create(
        user=user,
        ip_address=ip_address,
        session_key=session_key
    )
    


user_logged_in.connect(user_logged_in_receiver)

if FORCE_SESSION_TO_ONE:
    post_save.connect(post_save_session_receiver, sender=UserSession)

if FORCE_INACTIVE_USER_END_SESSION:
    post_save.connect(post_save_user_change_receiver, sender=User)

object_viewed_signal.connect(object_viewed_receiver)

