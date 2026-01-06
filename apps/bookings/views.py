"""
Booking views and Stripe integration
"""

from django.views.generic import View, TemplateView
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
from django.shortcuts import get_object_or_404
import stripe
import json

from apps.tours.models import Tour
from .models import Booking, Payment

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

