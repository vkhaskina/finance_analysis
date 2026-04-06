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
    #Данные из файла
    filename = models.CharField(max_length = 70)
    ticker = models.CharField(max_length = 5)
    period = models.CharField(max_length = 3) #D, M, Y
    date = models.DateField()
    open = models.DecimalField(max_digits = 20, decimal_places = 4)
    high = models.DecimalField(max_digits = 20, decimal_places = 4)
    low = models.DecimalField(max_digits = 20, decimal_places = 4)
    close = models.DecimalField(max_digits = 20, decimal_places = 4)
    vol = models.IntegerField()

    #Расчетные данные
    #Для графиков
    profit_simple = models.DecimalField(max_digits = 20, decimal_places = 4, null = True, blank = True)
    profit_ln = models.DecimalField(max_digits = 20, decimal_places = 4, null = True, blank = True)
    #Что еще добавить то? Риск? Истинный диапазон?

    class Meta:
        ordering = ['-id']
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'