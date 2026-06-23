import PySimpleGUI as sg
import csv
import os

ARQUIVO = 'senhas.csv'

# Cria arquivo se não existir
if not os.path.exists(ARQUIVO):
    with open(ARQUIVO, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Equipamento', 'Usuario', 'Senha'])

def salvar(equipamento, usuario, senha):
    with open(ARQUIVO, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([equipamento, usuario, senha])

def carregar():
    dados = []
    with open(ARQUIVO, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None)
        for linha in reader:
            dados.append(linha)
    return dados

def excluir(indice):
    dados = carregar()

    if indice is not None and len(dados) > indice:
        dados.pop(indice)

        with open(ARQUIVO, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Equipamento', 'Usuario', 'Senha'])
            writer.writerows(dados)

    return carregar()

# ------------------ LAYOUT ------------------
layout = [
    [sg.Text('Equipamento', size=(15,1)),
     sg.Input(key='equipamento', size=(30,1)),
     sg.Button('Pesquisar', size=(12,1), button_color=('white', 'darkgreen'))],

    [sg.Text('Usuário', size=(15,1)),
     sg.Input(key='usuario', size=(30,1)),
     sg.Button('Cadastrar', size=(12,1), button_color=('white', 'darkgreen'))],

    [sg.Text('Senha', size=(15,1)),
     sg.Input(password_char='*', key='senha', size=(30,1)),
     sg.Button('Excluir', size=(12,1), button_color=('white', 'darkblue'))],

    [sg.Table(
        values=[],   # começa vazio ✅
        headings=['Equipamento', 'Usuário', 'Senha'],
        col_widths=[20, 20, 20],
        auto_size_columns=False,
        num_rows=3,
        enable_events=True,
        key='tabela'
    )],

    [sg.Text('    ' * 12), sg.Button('Sair', size=(12,1))]
]

janela = sg.Window(
    'Cadastro de Senhas',
    layout,
    size=(600, 200),
    finalize=True
)

# ------------------ LOOP ------------------
while True:
    evento, valores = janela.read()

    if evento is None or evento == 'Sair':
        break

    # ✅ PESQUISAR (agora manual)
    if evento == 'Pesquisar':
        dados = carregar()

        filtro_equip = valores['equipamento'].lower()
        filtro_user = valores['usuario'].lower()

        if not filtro_equip and not filtro_user:
            janela['tabela'].update(values=dados)
        else:
            filtrado = []
            for linha in dados:
                if filtro_equip in linha[0].lower() and filtro_user in linha[1].lower():
                    filtrado.append(linha)

            janela['tabela'].update(values=filtrado)

    # ✅ CADASTRAR
    if evento == 'Cadastrar':
        if valores['equipamento'] and valores['usuario'] and valores['senha']:
            salvar(valores['equipamento'], valores['usuario'], valores['senha'])
            sg.popup('Salvo com sucesso!')

            janela['equipamento'].update('')
            janela['usuario'].update('')
            janela['senha'].update('')
        else:
            sg.popup('Preencha todos os campos')

    # ✅ EXCLUIR
    if evento == 'Excluir':
        selecionado = valores['tabela']

        if selecionado:
            indice = selecionado[0]

            confirmacao = sg.popup_yes_no('Tem certeza que deseja excluir?')

            if confirmacao == 'Yes':
                novos_dados = excluir(indice)
                janela['tabela'].update(values=novos_dados)
                sg.popup('Registro excluído!')
        else:
            sg.popup('Selecione um registro na tabela')

janela.close()
