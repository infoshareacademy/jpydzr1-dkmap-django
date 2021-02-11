from allauth.account.utils import complete_signup
from allauth.account.views import LoginView, SignupView
from allauth.account import app_settings
import logging
from allauth.exceptions import ImmediateHttpResponse


db_logger = logging.getLogger('db')


class OurLoginView(LoginView):

    def __init__(self):
        super(OurLoginView, self).__init__()

    def form_valid(self, form):
        success_url = self.get_success_url()
        try:
            db_logger.info(f'Successfully logged in user - {form.cleaned_data["login"]}')
            return form.login(self.request, redirect_url=success_url)
        except ImmediateHttpResponse as e:
            return e.response

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        error_message = str(form.errors).split('<li>')[2].split('</li></ul>')[0]
        db_logger.warning(f'Unsuccessfully logged in user - {form.cleaned_data["login"]} - {error_message}')
        return self.render_to_response(self.get_context_data(form=form))


class OurSignUpView(SignupView):

    def __init__(self):
        super(OurSignUpView, self).__init__()

    def form_valid(self, form):
        # By assigning the User to a property on the view, we allow subclasses
        # of SignupView to access the newly created User instance
        self.user = form.save(self.request)
        try:
            db_logger.info(f'Account successfully created by user - {form.cleaned_data["username"]}')
            return complete_signup(
                self.request,
                self.user,
                app_settings.EMAIL_VERIFICATION,
                self.get_success_url(),
            )
        except ImmediateHttpResponse as e:
            return e.response

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        error_message = str(form.errors).split('<li>')[2].split('</li></ul>')[0]
        db_logger.warning(f'Account not created for username: {form.cleaned_data["username"]} - {error_message}')
        return self.render_to_response(self.get_context_data(form=form))

