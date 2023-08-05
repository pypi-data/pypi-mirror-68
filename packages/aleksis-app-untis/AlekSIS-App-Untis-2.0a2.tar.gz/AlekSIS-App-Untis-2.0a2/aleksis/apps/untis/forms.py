from django import forms
from django.utils.translation import ugettext_lazy as _

from material import Fieldset

from aleksis.core.forms import EditGroupForm
from aleksis.core.models import Group


class UntisUploadForm(forms.Form):
    untis_xml = forms.FileField(label=_("Untis XML export"))


class GroupSubjectForm(forms.ModelForm):
    child_groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all())

    class Meta:
        model = Group
        fields = [
            "name",
            "short_name",
            "untis_subject",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget = forms.HiddenInput()
        self.fields["short_name"].widget = forms.HiddenInput()


GroupSubjectFormset = forms.modelformset_factory(Group, form=GroupSubjectForm, max_num=0, extra=0)

EditGroupForm.add_node_to_layout(Fieldset(_("UNTIS import"), "untis_subject"))
