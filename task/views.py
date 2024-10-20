from django.shortcuts import redirect


def root_view(request):
    """The root view should redirect to the API redoc."""
    return redirect("redoc")
