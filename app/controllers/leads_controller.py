from flask import request, jsonify, current_app
from http import HTTPStatus
from app.models.leads_model import LeadsModel
from app.configs.database import db
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import Query
from sqlalchemy.exc import IntegrityError, NoResultFound
from psycopg2.errors import UniqueViolation
from datetime import datetime
import re

class NotFound(Exception):
    pass

def create_leads():
    data = request.get_json()
    try:
        required_keys = ["name", "email", "phone"]
        data_request_keys = data.keys()

        for item in data_request_keys:
            if item not in required_keys:
                return {'msg': "Essa chave não é permitida"}, HTTPStatus.BAD_REQUEST
        for item in data_request_keys:
            if type(item) != str:
                return {'msg': "Todos os campos devem ser strings"}, HTTPStatus.BAD_REQUEST

        phone_regex = "^\([1-9]{2}\) (?:[2-8]|9[1-9])[0-9]{3}\-[0-9]{4}$"
        if not (re.fullmatch(phone_regex, data['phone'])):
            return {'msg': 'O formato do telefone precisa ser: (xx)xxxxx-xxxx'}, HTTPStatus.BAD_REQUEST
            
        leads_data = LeadsModel(**data)       
                
        session: Session = db.session
        session.expire_on_commit = False
        session.add(leads_data)
        session.add
        session.commit() 

        return jsonify(leads_data), HTTPStatus.CREATED
    except IntegrityError as e:
        if type(e.orig) == UniqueViolation:
            return {'msg': "Email ou telefone já existente"}, HTTPStatus.BAD_REQUEST

    
def retrieve_leads():
    try:
        all_leads = Query(LeadsModel,current_app.db.session).order_by(LeadsModel.visits.desc()).all()
        if not all_leads:
            raise NotFound
        
        return jsonify(all_leads), HTTPStatus.OK
    except NotFound:
        return {'error': 'Nenhum dado encontrado'},HTTPStatus.NOT_FOUND

def edit_leads():
    data = request.get_json()
    try:
        if type(data['email'])!=str:
            raise TypeError
        for key in data.keys():
            if key != 'email':
                raise KeyError                  
        
        lead_edit = LeadsModel.query.filter_by(email=data["email"]).one()
        
        setattr(lead_edit,'last_visit',datetime.utcnow())
        setattr(lead_edit,'visits',f"{lead_edit.visits+1}")     

        current_app.db.session.add(lead_edit)
        current_app.db.session.commit()
        return "", HTTPStatus.OK
    except NoResultFound:
        return {'msg': "Não foi encontrado nenhum dado com esse email"}
    except KeyError:
        return {'msg': "A chave deve ser um email"}
    except TypeError:
        return {'msg': "O conteúdo da requisição deve ser do tipo string"}



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
        return jsonify({'msg': "Dado não encontrado no banco com esse email"}), HTTPStatus.NOT_FOUND
    except NoResultFound:
        return jsonify({'msg': "Nenhum dado foi encontrado"}), HTTPStatus.NOT_FOUND
