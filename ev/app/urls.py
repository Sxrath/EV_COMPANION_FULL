from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    
    # path('',views.Home,name='home'),
    path('home/',views.Home.as_view(),name='home'),
    path('register/',views.register,name='register'),
    path('',views.user_login,name='LoginView'),
    path('logout/',views.UserLogoutView.as_view(),name='LogoutView'),
    path('ReservationListView/',views.ReservationListView.as_view(),name='ReservationListView'),
    # path('chargingspot/<int:chargingspot_id>/feedback/', views.chargingspot_feedback, name='chargingspot_feedback'),
    path('Reservation-delete/<int:pk>/',views.ReservationDeleteView.as_view(),name='delete-reservation'),
    
    path('select_place/', views.select_place, name='select_place'),
    path('StationList/<int:place_id>/', views.StationList, name='stationList'),
    path('select_place', views.select_place, name='select_place'),
    path('ReservationDetails/<int:id>', views.ReservationDetailsView, name='ReservationDetails'),
    path('chargingspotDetails/<int:chargingspot_id>', views.chargingspotDetails, name='chargingspotDetails'),
    path('PlaceReservation/', views.PlaceReservation, name='PlaceReservation'),
    path('PlaceReservationView/<int:chargingspot_id>',views.PlaceReservationView,name='PlaceReservationView')
    # path('ListFeedback/<int:id>', views.ListFeedback.as_view(), name='ListFeedback'),

    # path('stationList/',views.stationList,name='stationList')

]