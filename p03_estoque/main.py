"""Projeto 03: estoque com entradas e saidas seguras."""
from pymongo.errors import DuplicateKeyError
from conexao import banco

produtos = banco['produtos_p03']
produtos.create_index('sku', unique=True)

def inteiro_positivo(rotulo):
    try:
        n = int(input(rotulo))
        if n <= 0:
            raise ValueError
        return n
    except ValueError:
        print('Digite um inteiro maior que zero.')
        return None

while True:
    print('\n[1] Cadastrar [2] Entrada [3] Saída [4] Estoque baixo [0] Sair')
    op = input('Opção: ').strip()
    if op == '1':
        sku, nome = input('SKU: ').strip(), input('Produto: ').strip()
        minimo = inteiro_positivo('Estoque mínimo (>0): ')
        if not sku or not nome or minimo is None: continue
        try:
            produtos.insert_one({'sku': sku, 'nome': nome, 'quantidade': 0,
                                 'minimo': minimo})
            print('Cadastrado.')
        except DuplicateKeyError:
            print('SKU existente.')
    elif op in ('2', '3'):
        sku = input('SKU: ').strip()
        qtd = inteiro_positivo('Quantidade: ')
        if qtd is None: continue
        filtro = {'sku': sku}
        delta = qtd if op == '2' else -qtd
        if delta < 0:
            filtro['quantidade'] = {'$gte': qtd}
        r = produtos.update_one(filtro, {'$inc': {'quantidade': delta}})
        print('Movimentação realizada.' if r.modified_count else
              'Produto inexistente ou estoque insuficiente.')
    elif op == '4':
        # $expr permite comparar dois campos do mesmo documento.
        for p in produtos.find({'$expr': {'$lte': ['$quantidade', '$minimo']}}):
            print(f"{p['sku']} | {p['nome']} | {p['quantidade']} unidades")
    elif op == '0':
        break
    else:
        print('Opção inválida.')