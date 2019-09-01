from django.db import models

class DatabseServerProps(models.Model):
    host = models.CharField(max_length=500)
    dbname = models.CharField(max_length=500)
    user_name = models.CharField(max_length=500)
    password = models.CharField(max_length=500)
    schema_name = models.CharField(max_length=500)
    created_date = models.DateTimeField(auto_now_add=True)
    

