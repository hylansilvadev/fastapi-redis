from fastapi.testclient import TestClient
from fastapi import status
from pytest import fixture

from app.main import app

@fixture()
def cria_un_novo_usuario_depois_deleta():
    '''
        Este teste consiste em criar um novo usuário
        para um próximo teste vindo de **test_redis.py**
    '''
    
    url = '/user'
    
    data = {
        'id':1,
        'name':'Paciente Teste',
        'age': 99
    }
    
    client = TestClient(app)
    
    
    request = client.post(url, json=data)
    
    responseJSON = request.json()
    
    assert request.status_code == status.HTTP_201_CREATED
    assert responseJSON['name'] == data['name']
    assert responseJSON['age'] == data['age']
    
    yield
    
    id = responseJSON['id']
    
    url = f'/user/{id}'
    
    request = client.delete(url)
    
    assert request.status_code == status.HTTP_204_NO_CONTENT