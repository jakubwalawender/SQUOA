from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, RedirectView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from reservations import calendar
from reservations.calendar.calendar import HOURS_STRINGS
from reservations.models import ActivityType, ActivitySubscription, Hour
from reservations.serializers import CreateReservationSerializer


class SubscriptionsCalendarView(LoginRequiredMixin, TemplateView):
    template_name = "reservations/subscriptions.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        types = ActivityType.objects.all()
        court = kwargs['court']
        if court not in types.values_list('id', flat=True):
            raise Http404
        court = ActivityType.objects.get(id=court)
        context["hours"] = HOURS_STRINGS
        context["user"] = self.request.user
        context["court"] = court
        context["courts"] = types
        context["calendar"] = calendar.gather(court=court)
        return context


class DefaultView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            activity = ActivitySubscription.objects.all()
            if activity.exists():
                first = activity.first()
                return redirect(reverse('subscriptions_calendar', kwargs={'court':first.id}))
            else:
                return render(request, "reservations/index.html")
        return redirect(reverse('login'))


class CreateReservation(View):
    def post(self, request, court, hour, weekday, **kwargs):
        hour = Hour.objects.get(time=hour)
        try:
            ActivitySubscription.objects.create(user=request.user, type_id=court, hour=hour, weekday=weekday)
        except Exception as e:
            pass
        return redirect(reverse('subscriptions_calendar', kwargs={"court": court}))


class RemoveReservation(View):
    def post(self, request, court, hour, weekday, **kwargs):
        hour = Hour.objects.get(time=hour)
        try:
            activity = ActivitySubscription.objects.get(user=request.user, type_id=court, hour=hour, weekday=weekday)
            activity.delete()
        except Exception as e:
            pass
        return redirect(reverse('subscriptions_calendar', kwargs={"court": court}))


@api_view(['POST', 'DELETE'])
def activity_subscription(request):
    if request.method == 'POST':
        serializer = CreateReservationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
