from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone

def send_order_confirmation_email(order):
    """
    Sends an HTML + plain-text order confirmation email.
    """
    subject = f"Order Confirmation - Fabstar Limited (#{order.order_key})"
    from_email = "Fabstar Limited <noreply@fabstarlimited.com>"
    to_email = [order.email]

    # Prepare context for template rendering
    context = {
        "customer_name": order.full_name,
        "order_id": order.order_key,
        "order_total": f"{order.total:,.2f}",
        "order_date": order.created.strftime("%B %d, %Y") if hasattr(order, "created") else timezone.now().strftime("%B %d, %Y"),
        "current_year": timezone.now().year,
    }

    # Render HTML content
    html_content = render_to_string("email/order_confirmation.html", context)
    # Create plain-text fallback
    text_content = strip_tags(html_content)

    # Create email
    email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    email.attach_alternative(html_content, "text/html")
    email.send()


def send_internal_order_notification(order):
    """
    Sends an email to Fabstar's internal sales team when a new order is placed.
    """
    subject = f"🛒 New Order Received - #{order.order_key}"
    from_email = "Fabstar Limited <noreply@fabstarlimited.com>"
    to_email = ["natashafranklyn123@gmail.com"]  

    context = {
        "order": order,
        "current_year": timezone.now().year,
    }

    html_content = render_to_string("email/new_order_notification.html", context)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    email.attach_alternative(html_content, "text/html")
    email.send()
