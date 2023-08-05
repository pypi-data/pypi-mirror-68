from db.models import PostList
from web.forms import ModelForm


class PostListForm(ModelForm):
    class Meta:
        model = PostList
        fields = [
            "name",
            "public",
            "removable"
            "type",
            "owner"
        ]
