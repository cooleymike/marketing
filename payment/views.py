import logging

import stripe
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse

stripe.api_key = settings.STRIPE_SECRET_KEY

import stripe
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse

# Initialize Stripe once at the top (optional, but good practice)
stripe.api_key = settings.STRIPE_SECRET_KEY


def pricing_view(request):
    plans = {
        "starter": settings.STRIPE_PRICE_STARTER,
        "professional": settings.STRIPE_PRICE_PROFESSIONAL,
        "enterprise": settings.STRIPE_PRICE_ENTERPRISE,
    }

    if request.method == "POST":
        if request.POST.get("plan") not in plans:
            logging.error("There's no plan found in request, or plan is not offered")
            return redirect("pricing")
        plan = request.POST["plan"]
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[{
                    "price": plans[plan],
                    "quantity": 1,
                }],
                mode="subscription",
                # + "?session_id={CHECKOUT_SESSION_ID}"
                success_url=request.build_absolute_uri(reverse("success")),
                cancel_url=request.build_absolute_uri(reverse("cancel")),
            )
            return redirect(checkout_session.url, code=303)
        except stripe.error.StripeError as e:
            # Log the error in production
            print(f"Stripe Error: {e}")
            return render(request, "pricing.html", {'error': "Something went wrong with payment."})

    return render(request, "pricing.html")


def success(request):
    # Optional: Verify session_id here later
    return render(request, "success.html")


def cancel(request):
    return render(request, "cancel.html")
