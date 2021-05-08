import os
from big_picture import celery, create_app

app = create_app()
app.app_context().push()
