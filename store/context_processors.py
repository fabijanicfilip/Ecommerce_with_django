from .models import Category


# Ovaj view je napravljen kako bi se u svakom templateu mogle koristiti returnane vrijednosti (u settings.py pod 'TEMPLATES' > 'context_processors' je dodano 'store.views.categories', kako bi bilo omoguceno koristenje vrijednosti iz categories viewa u svim templateima)
def categories(request):
    categories = Category.objects.filter(level=0)
    context = {
        "categories": categories,
    }
    return context
