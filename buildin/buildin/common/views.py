from django.shortcuts import render, redirect
from django.views import generic as view

# def home_view(request):
#     return render(request, 'common/home_page.html')
from buildin.common.helpers.user_helpers import get_full_of_logged_user


class HomeView(view.TemplateView):
    template_name = 'common/home_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['show_hidden_nav_items'] = False
        # context['show_logout'] = False

        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user_full_name = get_full_of_logged_user(request)
            self.get_context_data(kwargs={'user_full_name': user_full_name})
            # self.get_context_data(kwargs={'show_hidden_nav_items': True, 'show_logout': True})
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)
