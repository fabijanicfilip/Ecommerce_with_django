from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect, render, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from django.contrib import messages

from orders.models import Order
from .forms import RegistrationForm, UserEditForm, UserAddressForm
from .models import Customer, Address
from store.models import Product
from .tokens import account_activation_token
from orders.views import user_orders


# Login, register, account


@login_required
def dashboard(request):
    orders = user_orders(request)
    context = {
        "orders": orders,
    }
    return render(request, "account/dashboard/dashboard.html", context)


@login_required
def edit_details(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)

    context = {
        "user_form": user_form,
    }
    return render(request, "account/dashboard/edit_details.html", context)


@login_required
def delete_user(request):
    user = Customer.objects.get(user_name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect("account:delete_confirmation")


def account_register(request):
    """if request.user.is_authenticated:
    return redirect('/')"""

    if request.method == "POST":
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data["email"]
            user.user_name = registerForm.cleaned_data["user_name"]
            user.set_password(registerForm.cleaned_data["password"])
            user.is_active = False
            user.save()
            # Setup email
            current_site = get_current_site(request)
            subject = "Activate your Account"
            message = render_to_string(
                "account/registration/account_activation_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            user.email_user(subject=subject, message=message)
            context = {
                "form": registerForm,
            }
            return render(request, "account/registration/register_account_confirm.html", context)

    else:
        registerForm = RegistrationForm()

    context = {
        "form": registerForm,
    }
    return render(request, "account/registration/register.html", context)


def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Customer.objects.get(pk=uid)
    except ():
        pass
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect("account:dashboard")
    else:
        return render(request, "account/registration/activation_invalid.html")


# Addresses


@login_required
def view_address(request):
    addresses = Address.objects.filter(customer=request.user)
    context = {"addresses": addresses}
    return render(request, "account/dashboard/addresses.html", context)


@login_required
def add_address(request):
    if request.method == "POST":
        address_form = UserAddressForm(data=request.POST)
        if address_form.is_valid():
            address_form = address_form.save(commit=False)
            address_form.customer = request.user
            address_form.save()
            return HttpResponseRedirect(reverse("account:addresses"))
    else:
        address_form = UserAddressForm()

    context = {
        "form": address_form,
    }
    return render(request, "account/dashboard/edit_addresses.html", context)


@login_required
def edit_address(request, id):
    if request.method == "POST":
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address, data=request.POST)
        if address_form.is_valid():
            address_form.save()
            return HttpResponseRedirect(reverse("account:addresses"))
    else:
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address)

    context = {
        "form": address_form,
    }
    return render(request, "account/dashboard/edit_addresses.html", context)


@login_required
def delete_address(request, id):
    address = Address.objects.get(pk=id, customer=request.user).delete()
    return redirect("account:addresses")


@login_required
def set_default(request, id):
    # Promjena prijasnje postavljene defaultne adrese u False u bazi podataka za tog user
    Address.objects.filter(customer=request.user, default=True).update(default=False)
    # Stavljanje trenutne adrese (filtrirane id-em) u True, tako da je ta dresa nova default adresa
    Address.objects.filter(pk=id, customer=request.user).update(default=True)

    # Ovo je da tokom checkout promjene default adrese redirect ne vodi u account vec ostaje na istoj stranici u checkoutu
    previous_url = request.META.get("HTTP_REFERER")
    if "delivery_address" in previous_url:
        return redirect("checkout:delivery_address")
    
    return redirect("account:addresses")


# Whishlist


@login_required
def wishlist(request):
    wishlist = Product.objects.filter(users_wishlist=request.user)
    context = {
        "wishlist": wishlist,
    }
    return render(request, "account/dashboard/user_wish_list.html", context)


@login_required
def add_to_wishlist(request, id):
    product = get_object_or_404(Product, id=id)
    if product.users_wishlist.filter(id=request.user.id).exists():
        product.users_wishlist.remove(request.user)
        messages.success(request, product.title + " has been removed from your WishList")
    else:
        product.users_wishlist.add(request.user)
        messages.success(request, "Added " + product.title + " to your Wishlist")
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


@login_required
def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    context = {
        "orders": orders,
    }
    return render(request, "account/dashboard/user_orders.html", context)
