from django.utils import timezone
import datetime

# revers and redirect
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse

# messages
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

# validation
from django.core.exceptions import ValidationError

# random number
import random

# requests
import requests
import re

# settingd imports
from django.conf import settings
from . import app_settings

# mail
from django.core.mail import EmailMultiAlternatives  # form html send
from django.core.mail import send_mail

# template rendering
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# jason response
from django.http import JsonResponse

# appp imports views
from django.views.generic import TemplateView, CreateView, View, FormView, ListView



class ChatBotView(TemplateView):
    """HomePage View"""
    template_name = "Chatbot/index." + app_settings.TEMPLATE_EXTENSION
    extra_context = {
        "page_title": " Chatbot Beta |  Fixenix - Best Mobile Repair in Siliguri"
        }

