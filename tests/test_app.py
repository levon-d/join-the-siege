import os
from io import BytesIO
import pytest
from src.app import app, allowed_file

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def files_dir():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '../files'))

@pytest.mark.parametrize("filename, expected", [
    ("file.pdf", True),
    ("file.png", True),
    ("file.jpg", True),
    ("file.txt", False),
    ("file", False),
])
def test_allowed_file(filename, expected):
    assert allowed_file(filename) == expected

def test_no_file_in_request(client):
    response = client.post('/classify_file')
    assert response.status_code == 400

def test_no_selected_file(client):
    data = {'file': (BytesIO(b""), '')}  # Empty filename
    response = client.post('/classify_file', data=data, content_type='multipart/form-data')
    assert response.status_code == 400

def test_success(client, mocker):
    mocker.patch('src.app.classify_file', return_value='test_class')

    data = {'file': (BytesIO(b"dummy content"), 'file.pdf')}
    response = client.post('/classify_file', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    assert response.get_json() == {"file_class": "test_class"}

def test_unknown_jpg(client, mocker, files_dir):
    mocker.patch('src.text_extraction.get_text_from_image', return_value='This is a driving license document.')
    mocker.patch('src.app.classify_file', return_value='drivers_license')

    with open(os.path.join(files_dir, 'unknown_file.jpg'), 'rb') as f:
        data = {'file': (BytesIO(f.read()), 'unknown_file.jpg')}
    response = client.post('/classify_file', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    assert response.get_json() == {"file_class": "drivers_license"}

def test_unknown_pdf(client, mocker, files_dir):
    mocker.patch('src.text_extraction.get_text_from_pdf', return_value='This is a bank statement document.')
    mocker.patch('src.app.classify_file', return_value='bank_statement')

    with open(os.path.join(files_dir, 'unknown_file.pdf'), 'rb') as f:
        data = {'file': (BytesIO(f.read()), 'unknown_file.pdf')}
    response = client.post('/classify_file', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    assert response.get_json() == {"file_class": "bank_statement"}

def test_example_docx(client, mocker, files_dir):
    mocker.patch('src.text_extraction.get_text_from_docx', return_value='This is an invoice document.')
    mocker.patch('src.app.classify_file', return_value='invoice')

    with open(os.path.join(files_dir, 'example.docx'), 'rb') as f:
        data = {'file': (BytesIO(f.read()), 'example.docx')}
    response = client.post('/classify_file', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    assert response.get_json() == {"file_class": "invoice"}