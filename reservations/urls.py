from django.urls import path

from reservations.views import DefaultView

from reservations.views import SubscriptionsCalendarView, CreateReservation, RemoveReservation, activity_subscription

urlpatterns = [
    path('activity/<int:court>', SubscriptionsCalendarView.as_view(), name="subscriptions_calendar"),
    path('', DefaultView.as_view(), name="default"),
    path('create/<int:court>/<str:hour>/<int:weekday>', CreateReservation.as_view(), name="create_reservation"),
    path('remove/<int:court>/<str:hour>/<int:weekday>', RemoveReservation.as_view(), name="remove_reservation")
]
