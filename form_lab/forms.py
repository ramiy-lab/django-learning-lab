from django import forms
import time


class SimpleNameForm(forms.Form):  # type: ignore[misc]
    name = forms.CharField(max_length=10)

    def clean_name(self) -> str:

        print("🔵 clean_name 開始")
        time.sleep(2)
        print("🔵 clean_name 修了")
        value: str = self.cleaned_data["name"]

        if not value.strip():
            raise forms.ValidationError("空白だけは禁止")

        return value.strip()
