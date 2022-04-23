from django.db import models
# todo...
# import Agency, Vehicle models
# create client model
# create order model [vehicle, agency, client, order_details]

#1
from agency.models import Agency
from vehicle.models import Vehicle

#2
class Client(models.Model):
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, null=True)

    first_name = models.CharField(max_length=100, help_text='Please insert your Firstname')
    last_name = models.CharField(max_length=100, help_text='Please insert your Lasttname')
    mobile = models.CharField(max_length=12, help_text='This field is important!')
    email = models.CharField(max_length=150, blank=True, null=True)
    GENDER_CHOICES = [
        ('m', 'Male'),
        ('f', 'Female'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, help_text='Please select gender')
    age = models.SmallIntegerField(null=True, blank=True)

    purpose = models.TextField(max_length=1000, help_text='(500)', blank=True)
    def get_full_name(self):
        return f'{self.first_name}, {self.last_name}'
    
    def __str__(self) -> str:
        return self.get_full_name()


#3
class Order(models.Model):
    """vehicle, agency, client, order_details"""
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='order')

    date_start = models.DateField()
    date_end = models.DateField()
    # time_start = models.TimeField()
    # time_end = models.TimeField()

    # current price
    price = models.DecimalField(max_digits=8, decimal_places=2, help_text='Vehicle price')

    STATUS_CHOICES = [
        ('p', 'Postponed'),
        ('a', 'Accepted'),
        ('r', 'Refused'),
    ]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='p')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-created_at']

    def get_full_date(self):
        return f'{self.date_start} - {self.date_end}'    

    def __str__(self) -> str:
        return f'{self.client} {self.vehicle.get_title()}'


