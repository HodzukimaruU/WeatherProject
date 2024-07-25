from django.db import models
    

class BaseModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class SearchHistory(BaseModel):
    city = models.CharField(max_length=100)
    search_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.city} - {self.search_date}"
