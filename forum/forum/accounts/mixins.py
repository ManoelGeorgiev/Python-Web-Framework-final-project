from django.shortcuts import redirect


class RedirectIfLoggedMixin:

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)
