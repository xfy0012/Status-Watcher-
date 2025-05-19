from flask import Flask
from app.tool import db, scheduler
from app.watcher import check_all_websites
from .models import Website
from .watcher import setup_jobs
from flask import render_template


def create_app():
    app = Flask(
        __name__, 
        instance_relative_config=True, 
        template_folder="../templates"
    )

    # Load default config from config.py (Config class)
    app.config.from_object('config.Config')
    # Load instance config from instance/config.py (for secrets, DB URI, etc.)
    # This file is ignored by git and can override default config
    app.config.from_pyfile('config.py', silent=True)

    db.init_app(app)
    scheduler.init_app(app)
    setup_jobs(app)

    with app.app_context():
        db.create_all()

    from .routes import main
    app.register_blueprint(main)

    @app.route('/')
    def home():
        return render_template('index.html')

    return app