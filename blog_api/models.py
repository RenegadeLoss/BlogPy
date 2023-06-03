from django.db import models
from django.urls import reverse
from .slug import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from taggit.managers import TaggableManager
# TODO: Подготовить модели БД
# Create your models here.


def user_derictory_path(instance, filename):
        return 'user_{0}/profile_image'.format(instance.user.id)

class Profile(models.Model):
    user = models.OneToOneField(User, auto_created=True, on_delete=models.CASCADE)
    foto = models.ImageField(verbose_name='Изображение', upload_to=user_derictory_path, blank=True)
    status = models.CharField(verbose_name='Статус', max_length=200, blank=True)

    def get_absolute_url(self):
        return reverse('profile_view', kwargs={'name': self.user.username, 'pk': self.id})
    


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# TODO: поддержка изображений
# TODO: поддержка разметки текста
class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    creator = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)
    label = models.CharField(max_length=100)
    text = models.TextField(max_length=1000)
    slug = models.CharField(max_length=120, blank=True, null=True)
    tag = TaggableManager()
    published = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-published']

    def save(self, *args, **kwargs):
        self.slug = '{label}_{creator_id}'.format(label=slugify(self.label), creator_id=self.creator.id)
        super(Post, self).save(args, **kwargs)

    def display_creator(self):
        return self.creator.username
    
    def display_tags(self):
        return [tag.name for tag in self.tag.all()]
    
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk':self.id})


# class Categories(models.Model):
#     pass



# class Comment(models.Model):
#     pass


