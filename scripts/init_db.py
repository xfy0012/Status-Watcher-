from app import create_app
from app.tool import db
from app.models import Website

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    sit = Website(
        url = "https://github.com/xfy0012",
        user_id = 1
    )

    db.session.add(sit)
    db.session.commit()
