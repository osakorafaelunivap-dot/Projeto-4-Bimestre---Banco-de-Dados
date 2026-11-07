
"""Projeto 01: CRUD de alunos por matricula."""

from pymongo.errors import DuplicateKeyError
from datetime import datetime, timezone
import re
from conexao import banco

alunos = banco['alunos_p01']

alunos.create_index('matricula', unique=True)

while True:
    print('\n[1] Cadastrar')
    print('[2] Listar')
    print('[3] Alterar')
    print('[4] Excluir')
    print('[5] Buscar por curso')
    print('[0] Sair')

    opcao = input('Opção: ').strip()

    if opcao == '1':
        matricula = input('Matrícula (8 dígitos): ').strip()
        if len(matricula) != 8 or not matricula.isdigit():
            print('Matrícula inválida! Digite 8 números.')
            continue

        nome = input('Nome: ').strip()
        curso = input('Curso: ').strip()

        if not all([matricula, nome, curso]):
            print('Preencha todos os campos.')
            continue

        try:
            alunos.insert_one({
                'matricula': matricula,
                'nome': nome,
                'curso': curso,
                'data_matricula': datetime.now(timezone.utc)
            })

            print('Aluno cadastrado!')

        except DuplicateKeyError:
            print('Matrícula já cadastrada.')

    elif opcao == '2':
        for aluno in alunos.find({}, {'_id': 0}).sort('nome', 1):
            print(aluno)

    elif opcao == '3':
        matricula = input('Matrícula: ').strip()
        novo_curso = input('Novo curso: ').strip()

        if novo_curso:
            r = alunos.update_one(
                {'matricula': matricula},
                {'$set': {'curso': novo_curso}}
            )

            print('Atualizado!' if r.matched_count else 'Aluno não encontrado.')

    elif opcao == '4':
        matricula = input('Matrícula: ').strip()

        r = alunos.delete_one({'matricula': matricula})

        print('Excluído!' if r.deleted_count else 'Aluno não encontrado.')

    elif opcao == '5':
        curso = input('Digite o curso que deseja buscar: ').strip()

        if curso:
            encontrados = alunos.find(
                {'curso': {'$regex': f'^{re.escape(curso)}$', '$options': 'i'}},
                {'_id': 0}
            )

            resultados = list(encontrados)

            if resultados:
                for aluno in resultados:
                    print(aluno)
            else:
                print('Nenhum aluno encontrado nesse curso.')

    elif opcao == '0':
        break

    else:
        print('Opção inválida.')
