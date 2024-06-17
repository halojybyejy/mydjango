from django.db.models.signals import post_save, post_migrate
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Account, Category, Tag


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    
@receiver(post_save, sender=User)
def create_default_accounts(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance, name='Total Account', type='total')
        Account.objects.create(user=instance, name='Main Account', type='main')
        
@receiver(post_save, sender=User)
def create_default_categories(sender, instance, created, **kwargs):
    if created:
        default_categories = ['Food', 'Transport', 'Utilities', 'Entertainment']
        for category_name in default_categories:
            Category.objects.create(name=category_name, user=instance)

@receiver(post_save, sender=User)
def create_default_tags(sender, instance, created, **kwargs):
    if created:
        default_tags = ['Urgent', 'Personal', 'Work', 'Important']
        for tag_name in default_tags:
            Tag.objects.create(name=tag_name, user=instance)
