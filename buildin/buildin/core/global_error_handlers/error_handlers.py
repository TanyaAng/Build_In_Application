from django.shortcuts import render


# permission_denied
def custom_handler403(request, exception):
    context = {}
    response = render(request, "403.html", context=context)
    response.status_code = 403
    return response


# page_not_found
def custom_handler404(request, exception):
    context = {}
    response = render(request, "404.html", context=context)
    response.status_code = 404
    return response


# server_error
def custom_handler500(request):
    context = {}
    response = render(request, "500.html", context=context)
    response.status_code = 500
    return response
