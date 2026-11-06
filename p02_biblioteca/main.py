"""Projeto 02: livros com indice unico e emprestimo atomico."""
from pymongo import ReturnDocument
from pymongo.errors import DuplicateKeyError
from conexao import banco

livros = banco['livros_p02']
livros.create_index('isbn', unique=True)

while True:
    print('\n[1] Novo livro [2] Catálogo [3] Emprestar [4] Devolver [0] Sair')
    op = input('Opção: ').strip()
    if op == '1':
        isbn, titulo = input('ISBN: ').strip(), input('Título: ').strip()
        autor = input('Autor: ').strip()
        if not all([isbn, titulo, autor]):
            print('Dados incompletos.'); continue
        try:
            livros.insert_one({'isbn': isbn, 'titulo': titulo, 'autor': autor,
                               'disponivel': True})
            print('Livro adicionado.')
        except DuplicateKeyError:
            print('ISBN já existe.')
    elif op == '2':
        for livro in livros.find({}, {'_id': 0}).sort('titulo'):
            print(livro)
    elif op == '3':
        isbn = input('ISBN: ').strip()
        livro = livros.find_one_and_update(
            {'isbn': isbn, 'disponivel': True},
            {'$set': {'disponivel': False}},
            return_document=ReturnDocument.AFTER)
        print('Empréstimo realizado.' if livro else 'Indisponível ou inexistente.')
    elif op == '4':
        isbn = input('ISBN: ').strip()
        livro = livros.find_one_and_update(
            {'isbn': isbn, 'disponivel': False},
            {'$set': {'disponivel': True}},
            return_document=ReturnDocument.AFTER)
        print('Devolução registrada.' if livro else 'Não estava emprestado.')
    elif op == '0':
        break
    else:
        print('Opção inválida.')