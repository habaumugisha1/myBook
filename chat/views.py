from django.shortcuts import render, reverse
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from .models import Notification


def all_notification(request, pk=None):
    users = User.objects.get(pk=pk)
    n = Notification.objects.filter(user=users)
    return render(request, 'all_notification.html', {'notification': n})


def show_notification(request, notification_id):
    n = Notification.objects.get(id=notification_id)
    return render(request, 'notification.html', {'notification': n})


def delete_notification(request, notification_id):
    n = Notification.objects.get(id=notification_id)
    n.viewed = True
    n.save()
    return HttpResponseRedirect(reverse('home'))
    # return render(request, 'loggedin.html')


def loggedin(request):
    n = Notification.objects.filter(user=request.user, viewed=False)
    return render(request, 'loggedin.html', {'full_name': request.user.username,
                                    'notifications': n})