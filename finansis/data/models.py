from django.db import models

# Столбцы из финама
#<TICKER>
# <PER>
# <DATE>
# <TIME>
# <OPEN>
# <HIGH>
# <LOW>
# <CLOSE>
# <VOL>
class Share(models.Model):
    filename = models.CharField(max_length=70)
    ticker = models.CharField(max_length=5)
    date = models.DateField()
    open = models.DecimalField(max_digits = 20, decimal_places = 10)
    high = models.DecimalField(max_digits = 20, decimal_places = 10)
    low = models.DecimalField(max_digits = 20, decimal_places = 10)
    close = models.DecimalField(max_digits = 20, decimal_places = 10)
    vol = models.IntegerField()

    class Meta:
        ordering = ['-id']
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'