from django.db import models
from django.contrib.auth.models import User

class RecyclingActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    plastic = models.FloatField(default=0)
    paper = models.FloatField(default=0)
    glass = models.FloatField(default=0)
    metal = models.FloatField(default=0)

    def total_recycled(self):
        return self.plastic + self.paper + self.glass + self.metal