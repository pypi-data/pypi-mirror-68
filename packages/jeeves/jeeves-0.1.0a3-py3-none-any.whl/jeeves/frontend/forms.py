from django import forms

from jeeves.db.models import Flow, Task


class FlowForm(forms.ModelForm):
    class Meta:
        model = Flow
        fields = ("name",)


class TaskForm(forms.ModelForm):
    definition = forms.CharField(widget=forms.Textarea, empty_value="{}")

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj._definition = self.cleaned_data["definition"]
        obj.save()
        return obj

    class Meta:
        model = Task
        fields = ("name", "type", "definition")
