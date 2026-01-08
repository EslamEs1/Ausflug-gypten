"""
Booking views and Stripe integration
"""

from django.views.generic import View, TemplateView
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
import stripe
import json

from apps.tours.models import Tour
from apps.excursions.models import Excursion
from apps.activities.models import Activity
from apps.transfers.models import Transfer
from .models import Booking, Payment
from .forms import BookingInquiryForm

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionView(View):
    """Create Stripe checkout session"""
    
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            tour_id = data.get('tour_id')
            participants = int(data.get('participants', 1))
            
            tour = get_object_or_404(Tour, id=tour_id, is_active=True)
            
            # Calculate total price
            total_price = tour.price * participants
            
            # Create Stripe checkout session
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'eur',
                        'product_data': {
                            'name': tour.title,
                            'description': tour.short_description,
                        },
                        'unit_amount': int(tour.price * 100),  # Convert to cents
                    },
                    'quantity': participants,
                }],
                mode='payment',
                success_url=request.build_absolute_uri('/booking/success/'),
                cancel_url=request.build_absolute_uri('/booking/cancel/'),
                metadata={
                    'tour_id': tour.id,
                    'participants': participants,
                }
            )
            
            return JsonResponse({'sessionId': session.id})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(View):
    """Handle Stripe webhooks"""
    
    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError:
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError:
            return HttpResponse(status=400)
        
        # Handle the event
        if event['type'] == 'payment_intent.succeeded':
            payment_intent = event['data']['object']
            # Update booking and payment status
            # TODO: Implement booking creation and update logic
            
        elif event['type'] == 'payment_intent.payment_failed':
            payment_intent = event['data']['object']
            # Handle failed payment
            
        return HttpResponse(status=200)


class BookingSuccessView(TemplateView):
    """Booking success page"""
    template_name = 'bookings/success.html'


class BookingCancelView(TemplateView):
    """Booking cancelled page"""
    template_name = 'bookings/cancel.html'


class BookingInquiryView(View):
    """Simple booking inquiry without payment"""
    
    def post(self, request, *args, **kwargs):
        # Determine booking type
        tour_id = request.POST.get('tour_id')
        excursion_id = request.POST.get('excursion_id')
        activity_id = request.POST.get('activity_id')
        transfer_id = request.POST.get('transfer_id')
        
        tour = None
        excursion = None
        activity = None
        transfer = None
        redirect_url = reverse('core:home')
        
        if tour_id:
            tour = get_object_or_404(Tour, id=tour_id, is_active=True)
            redirect_url = tour.get_absolute_url()
            form = BookingInquiryForm(request.POST, tour=tour)
        elif excursion_id:
            excursion = get_object_or_404(Excursion, id=excursion_id, is_active=True)
            redirect_url = excursion.get_absolute_url()
            form = BookingInquiryForm(request.POST, excursion=excursion)
        elif activity_id:
            activity = get_object_or_404(Activity, id=activity_id, is_active=True)
            redirect_url = activity.get_absolute_url()
            form = BookingInquiryForm(request.POST, activity=activity)
        elif transfer_id:
            transfer = get_object_or_404(Transfer, id=transfer_id, is_active=True)
            redirect_url = transfer.get_absolute_url()
            form = BookingInquiryForm(request.POST, transfer=transfer)
        else:
            messages.error(request, "Ungültige Buchungsanfrage.")
            return redirect('core:home')
        
        if form.is_valid():
            booking = form.save(commit=False)
            
            # Link to user if authenticated
            if request.user.is_authenticated:
                booking.user = request.user
            
            booking.save()
            
            messages.success(
                request,
                f'Vielen Dank für Ihre Buchungsanfrage! '
                f'Ihre Bestätigungsnummer ist {booking.confirmation_code}. '
                f'Wir werden uns in Kürze mit Ihnen in Verbindung setzen.'
            )
            # TODO: Send confirmation email to customer and notification to admin
            return redirect('bookings:inquiry_success', confirmation_code=booking.confirmation_code)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{form.fields[field].label}: {error}")
            return redirect(redirect_url)


class BookingInquirySuccessView(TemplateView):
    """Booking inquiry success page"""
    template_name = 'bookings/inquiry_success.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        confirmation_code = self.kwargs.get('confirmation_code')
        if confirmation_code:
            context['booking'] = get_object_or_404(Booking, confirmation_code=confirmation_code)
        return context

