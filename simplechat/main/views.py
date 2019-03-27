from datetime import datetime, timedelta

from django.views.generic import ListView

from simplechat.main.models import Message, Member


class IndexView(ListView):
    template_name = 'main/index.html'
    model = Message
    ordering = 'created'
    context_object_name = 'messages'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        users = Member.objects.values_list('username', flat=True).distinct().filter(
            updated__gte=datetime.now() - timedelta(minutes=60))
        ctx.update({'users': users})
        return ctx
