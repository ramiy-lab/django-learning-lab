from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
import time

from .forms import SimpleNameForm


def form_page(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = SimpleNameForm(request.POST)

        time.sleep(4)
        print("🟡 is_valid 呼ぶ前")
        time.sleep(2)
        print("cleaned_data:", getattr(form, "cleaned_data", None))

        if form.is_valid():
            print("🟢 is_valid True")
            print("cleaned_data:", form.cleaned_data)
        else:
            print("🔴 is_valid False")
            print("errors:", form.errors)

    else:
        form = SimpleNameForm()

    return render(request, "form_lab/form_page.html", {"form": form})
