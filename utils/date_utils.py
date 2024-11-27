# utils.py

from datetime import datetime, timedelta

def format_dates(num_days=14):
    """Generate a list of formatted dates for today and the last num_days."""
    today = datetime.today()
    dates = [today - timedelta(days=i) for i in range(num_days)]
    formatted_dates = []

    nb_months = ["januar", "februar", "mars", "april", "mai", "juni", 
                  "juli", "august", "september", "oktober", "november", "desember"]
    
    for date in dates:
        day = date.strftime('%d')
        month = nb_months[date.month - 1]  # Get month name from the list
        year = date.strftime('%Y')
        formatted_date = f"{day}. {month} {year}"  # Combine them
        formatted_dates.append(formatted_date)

    return formatted_dates

def get_dates(num_days=14):
    """Generate a list of dates in 'YYYY-MM-DD' format for today and the last num_days."""
    today = datetime.today()
    dates = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(num_days)]
    return dates