from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView


@property
def next_page_property(self):
    value = self.__dict__.get('_next_page_value', None)
    if value is None:
        value = reverse('playlister:home')
        self.__dict__['_next_page_value'] = value
    return value


# evaluate only when needed with lazy variant
LogoutView.next_page = reverse_lazy('playlister:home')
# or it can be done via property pattern
LogoutView.next_page = next_page_property


class AutoRedirectLoginView(LoginView):

    def should_redirect_to_admin(self):
        return (self.request.user and
                self.request.user.is_authenticated and
                self.request.user.is_active and
                self.request.user.is_superuser)

    def get_success_url(self):
        url = self.get_redirect_url()
        if self.should_redirect_to_admin():
            return url or '/admin/'
        else:
            return url or '/'
