from datetime import datetime


def get_current_year(request):
    curr_year = datetime.today().strftime('%Y')

    return {'year': curr_year}
