from flask import request, jsonify, current_app
from http import HTTPStatus
from app.models.leads_model import LeadsModel
from app.configs.database import db
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import Query
from sqlalchemy.exc import IntegrityError

class NotFound(Exception):
    pass

def create_leads():
        data = request.get_json()    
        leads_data = LeadsModel(**data)       
                
        session: Session = db.session
        session.expire_on_commit = False
        session.add(leads_data)
        session.add
        session.commit() 

        return jsonify(leads_data), HTTPStatus.CREATED
    
def retrieve_leads():
    try:
        all_leads = Query(LeadsModel,current_app.db.session).order_by(LeadsModel.visits.desc()).all()
        if not all_leads:
            raise NotFound
        serialized_leads = LeadsModel.serializer(all_leads)
        return jsonify(serialized_leads), HTTPStatus.OK
    except NotFound:
        return {'error': 'Nenhum dado encontrado'},HTTPStatus.NOT_FOUND

def delete_leads():
    try:
        data = request.get_json()
        all_keys_request= data.keys()
        if  len(list(all_keys_request)) > 1 or list(all_keys_request)[0] != 'email':            
            return jsonify({'error': "O valor precisa ser uma string email"}), HTTPStatus.BAD_REQUEST
        if type(data['email']) != str:
            return jsonify({'error': "O valor precisa ser uma string"}), HTTPStatus.BAD_REQUEST
            
        founded_lead = LeadsModel.query.filter_by(email=data["email"]).one()            
        current_app.db.session.delete(founded_lead)
        current_app.db.session.commit()

        return jsonify({'msg': 'Dado deletado'}), HTTPStatus.NO_CONTENT
    
    except NotFound:
        return jsonify({"message": "Dado não encontrado no banco com esse email"}), HTTPStatus.NOT_FOUND