from db.models import Member
from web.forms import ModelForm


class ProfileGeneralInformationForm(ModelForm):
    id_form = ""

    def __init__(self, id_form: str):
        super().__init__()
        self.id_form = id_form

    class Meta:
        model = Member
        fields = [
            "username",
            "first_name",
            "last_name",
            "avatar",
            "web_site",
            "gender",
            "occupation",
            "phone_number",
            "postal_address",
            "postal_address_2",
            "postal_city",
            "postal_code",
            "language",
        ]

    def save_general_information(self):
        pass
