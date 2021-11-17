from django.db import models

from resources.days.models import Day

# Create your models here.


class Category(models.Model):
    cat = models.CharField(max_length=20, null=False, unique=True)

    # Ex. SUSHI should be equal as sushi.
    # we don't want duplicates with Uppercase and Lowercase
    def save(self, *args, **kwargs):
        self.cat = self.cat.lower()
        return super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.cat


class DayCategory(models.Model):
    cat = models.ForeignKey(Category, on_delete=models.CASCADE)
    day = models.ForeignKey(Day, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["day", "cat"], name="unique_daycat")
        ]
