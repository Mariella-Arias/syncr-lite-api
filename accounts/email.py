import os
from djoser.email import ActivationEmail, ConfirmationEmail, PasswordResetEmail, PasswordChangedConfirmationEmail, UsernameChangedConfirmationEmail, UsernameResetEmail

class CustomActivationEmail(ActivationEmail):
    def get_context_data(self):
        context = super().get_context_data()
        context['domain'] = os.environ.get('FRONTEND_DOMAIN', 'localhost:5173')

        return context

class CustomConfirmationEmail(ConfirmationEmail):
    def get_context_data(self):
        context = super().get_context_data()
        context['domain'] = os.environ.get('FRONTEND_DOMAIN', 'localhost:5173')

        return context

class CustomPasswordResetEmail(PasswordResetEmail):
    def get_context_data(self):
        context = super().get_context_data()
        context['domain'] = os.environ.get('FRONTEND_DOMAIN', 'localhost:5173')

        return context

class CustomPasswordChangedConfirmationEmail(PasswordChangedConfirmationEmail):
    def get_context_data(self):
        context = super().get_context_data()
        context['domain'] = os.environ.get('FRONTEND_DOMAIN', 'localhost:5173')

        return context

class CustomUsernameChangedConfirmationEmail(UsernameChangedConfirmationEmail):
    def get_context_data(self):
        context = super().get_context_data()
        context['domain'] = os.environ.get('FRONTEND_DOMAIN', 'localhost:5173')

        return context

class CustomUsernameResetEmail(UsernameResetEmail):
    def get_context_data(self):
        context = super().get_context_data()
        context['domain'] = os.environ.get('FRONTEND_DOMAIN', 'localhost:5173')

        return context
