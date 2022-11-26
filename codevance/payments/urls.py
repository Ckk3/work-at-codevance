"""payments URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from . import views

urlpatterns = [
    path('', views.payment_list, name='payment-list'),
    path('payment/<int:id>', views.payment_view, name='payment-view'),
    path('anticipaterequest/<int:id>', views.anticipate_request_view, name='payment-view'),
    path('anticipateinfo/<int:id>', views.anticipate_info_view, name='payment-view'),
]
