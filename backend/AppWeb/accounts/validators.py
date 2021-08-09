from django.core.exceptions import ValidationError


class WhiteSpaceValidator:

    def validate(self, password, user=None):
        if ' ' in password:
            raise ValidationError(
                'El password no debe contener espacios en blanco.',
                code='password_with_whitespace',
            )

    def get_help_text(self):
        return 'Evite utilizar espacios en blanco en el password.'
