def my_custom_context(request):
    white = request.session.get('white', 1)
    return {'white': white}
