from django.db import models

# Create your models here.


# -----------------SET UP WILAYA COMMUNE --------------
class Wilaya(models.Model):
    code = models.IntegerField(blank=True)
    name = models.CharField(max_length=200, blank=True)
    ar_name = models.CharField(max_length=200, blank=True)
    longitude = models.CharField(max_length=50, null=True, blank=True)
    latitude = models.CharField(max_length=50, null=True, blank=True)
    class Meta:
        ordering=['name']
    
    def __str__(self) -> str:
        return self.name

class Commune(models.Model):
    post_code = models.IntegerField(blank=True)
    name = models.CharField(max_length=200, blank=True)
    wilaya_id = models.ForeignKey(Wilaya, on_delete=models.CASCADE)
    ar_name = models.CharField(max_length=200, blank=True)
    latitude = models.CharField(max_length=50, null=True, blank=True)
    longitude = models.CharField(max_length=50, null=True, blank=True)
    class Meta:
        ordering=['name']
    
    def __str__(self) -> str:
        return self.name

# -----------------SET UP CAR MAKES MODELS --------------
# setup is in vehicle model...