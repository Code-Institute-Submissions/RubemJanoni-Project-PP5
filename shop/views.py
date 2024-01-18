from django.shortcuts import render

# Create your views here.


class Make_login (LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('myecommerce:login_page')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Login successfully. Welcome!')
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, 'Something is wrong, Try again.')
        return response

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(self.get_success_url())

        return super().get(request, *args, **kwargs)
