"""Projeto 04: agenda com filtro por nome e indice unico."""
import re
from pymongo.errors import DuplicateKeyError
from conexao import banco

contatos = banco['contatos_p04']
contatos.create_index('email', unique=True)

while True:
    print('\n[1] Adicionar [2] Buscar [3] Atualizar [4] Remover [0] Sair')
    op = input('Opção: ').strip()
    if op == '1':
        nome = input('Nome: ').strip()
        email = input('E-mail: ').strip().lower()
        telefone = input('Telefone: ').strip()
        if not all([nome, email, telefone]): continue
        try:
            contatos.insert_one({'nome': nome, 'email': email,
                                 'telefone': telefone})
            print('Contato salvo!')
        except DuplicateKeyError:
            print('E-mail já utilizado.')
    elif op == '2':
        trecho = input('Parte do nome: ').strip()
        if not trecho:
            print('Informe um termo.'); continue
        busca = {'nome': {'$regex': re.escape(trecho), '$options': 'i'}}
        for item in contatos.find(busca, {'_id': 0}).sort('nome'):
            print(item)
    elif op == '3':
        email = input('E-mail do contato: ').strip().lower()
        telefone = input('Novo telefone: ').strip()
        if telefone:
            r = contatos.update_one({'email': email}, {'$set': {'telefone': telefone}})
            print('Atualizado!' if r.matched_count else 'Contato não encontrado.')
    elif op == '4':
        email = input('E-mail: ').strip().lower()
        r = contatos.delete_one({'email': email})
        print('Excluído!' if r.deleted_count else 'Contato não encontrado.')
    elif op == '0':
        break
    else:
        print('Opção inválida.')