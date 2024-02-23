from django.shortcuts import redirect

class PhoneNumberMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated and 'require_phone_number' in request.session:
            if not request.path.startswith('/add_phone_number/'):  # Adjust the path as necessary
                return redirect('add_phone_number')  # Redirect to the phone number form
        return response
