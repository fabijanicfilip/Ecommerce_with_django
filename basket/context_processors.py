from .basket import Basket


# Napravljeno kako bi se u klasu prenosio request info o korisnitku, na sve stranice, iz kojega se izvalici session vrijednost u klasi Basket u fileu basket.py
def basket(request):
    context = {
        "basket": Basket(request),
    }
    return context
