"""Projeto 07: duas colecoes e relatorio com $lookup."""
from pymongo.errors import DuplicateKeyError
from conexao import banco

turmas = banco['turmas_p07']
alunos = banco['alunos_p07']
notas = banco['notas_p07']
turmas.create_index('codigo', unique=True)
alunos.create_index('matricula', unique=True)
notas.create_index([('matricula', 1), ('bimestre', 1)], unique=True)

while True:
    print('\n[1] Turma [2] Aluno [3] Nota [4] Boletim [0] Sair')
    op = input('Opção: ').strip()
    try:
        if op == '1':
            codigo = input('Código da turma: ').strip()
            if codigo:
                turmas.insert_one({'codigo': codigo})
                print('Turma criada.')
        elif op == '2':
            matricula = input('Matrícula: ').strip()
            nome = input('Nome: ').strip()
            codigo = input('Código da turma: ').strip()
            if not all([matricula, nome, codigo]) or not turmas.find_one({'codigo': codigo}):
                print('Dados inválidos ou turma não existe.'); continue
            alunos.insert_one({'matricula': matricula, 'nome': nome, 'turma': codigo})
            print('Aluno cadastrado.')
        elif op == '3':
            matricula = input('Matrícula: ').strip()
            if not alunos.find_one({'matricula': matricula}):
                print('Aluno não existe.'); continue
            bimestre = int(input('Bimestre (1-4): '))
            valor = float(input('Nota (0-10): ').replace(',', '.'))
            if bimestre not in range(1, 5) or not 0 <= valor <= 10:
                print('Bimestre ou nota fora do intervalo.'); continue
            notas.update_one({'matricula': matricula, 'bimestre': bimestre},
                             {'$set': {'valor': valor}}, upsert=True)
            print('Nota salva.')
        elif op == '4':
            codigo = input('Código da turma: ').strip()
            pipeline = [
                {'$match': {'turma': codigo}},
                {'$lookup': {'from': 'notas_p07', 'localField': 'matricula',
                             'foreignField': 'matricula', 'as': 'notas'}},
                {'$project': {'_id': 0, 'matricula': 1, 'nome': 1,
                              'media': {'$avg': '$notas.valor'}}},
                {'$sort': {'nome': 1}}
            ]
            for a in alunos.aggregate(pipeline):
                media = f"{a['media']:.2f}" if a.get('media') is not None else 'sem notas'
                print(f"{a['matricula']} | {a['nome']} | média: {media}")
        elif op == '0':
            break
        else:
            print('Opção inválida.')
    except (ValueError, DuplicateKeyError):
        print('Dados inválidos ou registro duplicado.')