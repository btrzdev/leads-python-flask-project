from flask import Blueprint
from app.controllers import leads_controller

bp_vaccination = Blueprint('bp_vaccination', __name__, url_prefix="/leads")

bp_vaccination.post("")(leads_controller.create_leads)
bp_vaccination.get("")(leads_controller.retrieve_leads)
bp_vaccination.delete("")(leads_controller.delete_leads)