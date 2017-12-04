from django.shortcuts import render
from django.template.loader import render_to_string


def setUp(data):

    return  render_to_string( 'notification.html', data)

