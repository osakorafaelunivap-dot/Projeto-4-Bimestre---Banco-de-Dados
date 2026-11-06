"""Projeto 09: API REST CRUD de produtos com FastAPI + MongoDB."""
from bson import ObjectId
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from conexao import banco

app = FastAPI(title='API de Produtos - MongoDB', version='1.0')
produtos = banco['produtos_p09']

class ProdutoEntrada(BaseModel):
    nome: str = Field(min_length=1, max_length=100)
    preco_centavos: int = Field(ge=0)
    quantidade: int = Field(ge=0)

def serializar(p):
    return {'id': str(p['_id']), 'nome': p['nome'],
            'preco_centavos': p['preco_centavos'], 'quantidade': p['quantidade']}

def buscar(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(400, 'Identificador inválido')
    p = produtos.find_one({'_id': ObjectId(id)})
    if not p:
        raise HTTPException(404, 'Produto não encontrado')
    return p

@app.post('/produtos', status_code=201)
def criar(p: ProdutoEntrada):
    id = produtos.insert_one(p.model_dump()).inserted_id
    return serializar(produtos.find_one({'_id': id}))

@app.get('/produtos')
def listar(limite: int = Query(default=50, ge=1, le=100)):
    return [serializar(p) for p in produtos.find().limit(limite)]

@app.get('/produtos/{id}')
def consultar(id: str):
    return serializar(buscar(id))

@app.put('/produtos/{id}')
def atualizar(id: str, p: ProdutoEntrada):
    buscar(id)
    produtos.update_one({'_id': ObjectId(id)}, {'$set': p.model_dump()})
    return serializar(buscar(id))

@app.delete('/produtos/{id}', status_code=204)
def excluir(id: str):
    buscar(id)
    produtos.delete_one({'_id': ObjectId(id)})
    return None