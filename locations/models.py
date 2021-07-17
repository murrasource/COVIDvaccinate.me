from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=100, blank=False, default='Vaccination Site')
    address = models.CharField(max_length=250, null=True)
    postal = models.CharField(max_length=15, null=True)
    latitude = models.DecimalField(max_digits=6, decimal_places=4, null=True)
    longitude = models.DecimalField(max_digits=7, decimal_places=4, null=True)
    state = models.CharField(max_length=2, null=True)
    url = models.URLField(default='https://www.cdc.gov/vaccines/covid-19/index.html')
    availabilities = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}{self.id}'

STATE_CHOICES = (
    ('AL','AL'),
    ('AK','AK'),
    ('AZ','AZ'),
    ('AR','AR'),
    ('CA','CA'),
    ('CO','CO'),
    ('CT','CT'),
    ('DE','DE'),
    ('DC','DC'),
    ('FL','FL'),
    ('GA','GA'),
    ('HI','HI'),
    ('ID','ID'),
    ('IL','IL'),
    ('IN','IN'),
    ('IA','IA'),
    ('KS','KS'),
    ('KY','KY'),
    ('LA','LA'),
    ('ME','ME'),
    ('MD','MD'),
    ('MA','MA'),
    ('MI','MI'),
    ('MN','MN'),
    ('MS','MS'),
    ('MO','MO'),
    ('MT','MT'),
    ('NE','NE'),
    ('NV','NV'),
    ('NH','NH'),
    ('NJ','NJ'),
    ('NM','NM'),
    ('NY','NY'),
    ('NC','NC'),
    ('ND','ND'),
    ('OH','OH'),
    ('OK','OK'),
    ('OR','OR'),
    ('PA','PA'),
    ('RI','RI'),
    ('SC','SC'),
    ('SD','SD'),
    ('TN','TN'),
    ('TX','TX'),
    ('UT','UT'),
    ('VT','VT'),
    ('VA','VA'),
    ('WA','WA'),
    ('WV','WV'),
    ('WI','WI'),
    ('WY','WY'),
)

class Subscriber(models.Model):
    email = models.EmailField()
    state = models.CharField(max_length=2, choices=STATE_CHOICES, default='MN')
    zipcode = models.IntegerField(null=True)
    latitude = models.DecimalField(max_digits=6, decimal_places=4, null=True)
    longitude = models.DecimalField(max_digits=7, decimal_places=4, null=True)

    def __str__(self):
        return self.email

class Geocode(models.Model):
    zipcode = models.IntegerField()
    latitude = models.DecimalField(max_digits=6, decimal_places=4)
    longitude = models.DecimalField(max_digits=7, decimal_places=4)

    def __str__(self):
        return f'{self.zipcode}: ({self.latitude},{self.longitude})'