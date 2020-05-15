from django.db import models

# Create your models here.


class Staff(models.Model):
    name = models.CharField(max_length=40)
    position = models.CharField(max_length=40)
    commission_percentage = models.IntegerField(default=0)

    def __str__(self):
        return str(self.name) + ", " + str(self.position)+", " + str(self.commission_percentage)+"% commission"


class Lemonade(models.Model):
    name = models.CharField(max_length=40)
    price = models.FloatField(default=0)

    def __str__(self):
        return str(self.name) + " @ $"+str(self.price)+"/cup"


class Sale(models.Model):
    lemonade = models.ForeignKey(Lemonade, on_delete=models.CASCADE)
    date = models.DateTimeField()
    sales_person = models.ForeignKey(Staff, on_delete=models.CASCADE)

    def __str__(self):
        return "Sale " + str(self.id) + ": " + str(self.date)

