from flask import Flask
def init_app(app: Flask):
    from app.routes.leads_route import bp_leads
    app.register_blueprint(bp_leads)