from datetime import datetime

def inject_now():
    return {'current_year': datetime.utcnow().year}

app.context_processor(inject_now)