from django.db import models

class Registrant(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    
    TITLE_CHOICES = (
        ('Prof.', 'Prof.'),
        ('Dr.', 'Dr.'),
        ('Mr.', 'Mr.'),
        ('Ms.', 'Ms.'),
    )
    title = models.CharField(max_length=10, choices=TITLE_CHOICES)
    
    email = models.EmailField(db_index=True, max_length=100, unique=True)
    institution = models.CharField(max_length=100)
    department = models.CharField(max_length=100, blank=True)
    address = models.TextField()
    country = models.CharField(max_length=50)
    zipcode = models.CharField(verbose_name='Zip / Postal Code', max_length=15)
    
    creation_date = models.DateTimeField('Date Created', auto_now_add=True, editable=False)
    modified_date = models.DateTimeField('Date Modified', auto_now=True, editable=False)
    
    symposium_1 = models.BooleanField(verbose_name='Waste Prevention and Minimization')
    symposium_2 = models.BooleanField(verbose_name='Waste Biomass Utilization')
    symposium_3 = models.BooleanField(verbose_name='Integrated Solid Waste management')
    symposium_4 = models.BooleanField(verbose_name='Waste Processing and Treatment')
    symposium_5 = models.BooleanField(verbose_name='Sustainable Landfill')
    symposium_6 = models.BooleanField(verbose_name='Hazardous Waste Management')
    symposium_7 = models.BooleanField(verbose_name='Health and Environmental Aspect of Solid Waste Handling')
    symposium_8 = models.BooleanField(verbose_name='Municipal Solid Waste in Developing Countries')
    
    confirmed = models.BooleanField(default=False, db_index=True)
    payment_received = models.BooleanField(default=False, db_index=True)
    
    class Meta:
        verbose_name  = 'Registrant'
        verbose_name_plural  = 'Registrants'
    
    def __unicode__(self):
        return self.name
    