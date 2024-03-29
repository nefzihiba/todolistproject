from django.db import models

class task(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=45)
    completed = models.BooleanField(default=False)  

    def __str__(self):
        return self.title
