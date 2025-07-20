from django.db import models # type: ignore
from django.conf import settings # type: ignore
from django.utils import timezone # type: ignore

User = settings.AUTH_USER_MODEL


#ORM
class Documents(models.Model):
    owner= models.ForeignKey(User, on_delete=models.CASCADE)
    title= models.CharField(default="Title")
    content = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    active_at = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null= True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"


    def save(self, *args, **kwargs):
        if self.active and self.active_at is None:
            self.active_at = timezone.now()
        else:
            self.active_at = None

        super().save(*args, **kwargs)




