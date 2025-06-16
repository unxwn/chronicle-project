import datetime

def current_year(request):
    return {'current_year': datetime.date.today().year}