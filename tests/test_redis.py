from fastapi import status
from fastapi.testclient import TestClient
from app.main import app



def test_deve_criar_um_novo_usuario_depois_excluir():
    
    url = '/user'
    
    data = {
        'name':'Usuário Teste',
        'age': 99
    }
    
    client = TestClient(app)
    
    request = client.post(url=url, json=data)
    
    responseJSON = request.json()
    
    assert request.status_code == status.HTTP_201_CREATED
    assert responseJSON['name'] == data['name']
    assert responseJSON['age'] == data['age']  
    
    id = responseJSON['id']
    url = f'/user/{id}'
    
    request = client.delete(url)
    

def test_deve_buscar_um_usuario_pelo_id(cria_un_novo_usuario_depois_deleta):
    
    url = '/user/1'
    
    client = TestClient(app)
    
    request = client.get(url)
    
    responseJSON = request.json()
    
    assert request.status_code == status.HTTP_200_OK
    assert responseJSON['name'] == 'Paciente Teste'
    assert responseJSON['age'] == 99
    

    
    
    