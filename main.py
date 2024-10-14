import flet as ft
import json
import requests
import threading
import time
#import pyrebase


def main(page: ft.page):
    # CORES APP
    verde1 = '#054A29'
    verde2 = '#137547'
    branco1 = '#FFFFFF'
    branco2 = '#e9ecef'

    page.appbar = ft.AppBar(title=ft.Text('Gaiola Automatizada Inteligente para Aves', size=18), bgcolor=verde1)
    page.bgcolor = branco1
    page.auto_scroll = ft.ScrollMode.AUTO

    # Cortinas
    count_cortinas = 0

    state = False
    Cortina_ativa = False

    Seg_cor_ativo = False
    Ter_cor_ativo = False
    Qua_cor_ativo = False
    Qui_cor_ativo = False
    Sex_cor_ativo = False
    Sab_cor_ativo = False
    Dom_cor_ativo = False

    state_dias = {'Seg': False, 'Ter': False, 'Qua': False, 'Qui': False, 'Sex': False, 'Sab': False, 'Dom': False}
    DiasDaSemana = ('Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sab', 'Dom')
    horario_cortinas = {'abre': '', 'fecha': ''}
    horarios_cortinas_semana = {'Seg': [], 'Ter': [], 'Qua': [], 'Qui': [], 'Sex': [], 'Sab': [], 'Dom': []}
    i = 0

    DiasSelecionados = []

    lista_botoes_seg = []
    lista_botoes_ter = []
    lista_botoes_qua = []
    lista_botoes_qui = []
    lista_botoes_sex = []
    lista_botoes_sab = []
    lista_botoes_dom = []

    # Alimentação
    count_alimentar = 0

    Comida = ''
    LinkImagensComida = {
        'Pequeno': [
            'https://www.passaromix.com.br/wpmix/wp-content/uploads/2015/08/alpiste1-800x600.jpg',  # Alpiste
            'https://st2.depositphotos.com/1077338/47543/i/450/depositphotos_475436270-stock-photo-food-background-many-whole-grain.jpg',
            # Níger
            'https://acdn.mitiendanube.com/stores/818/927/products/aveia-em-graos1-331148acab8444850615330644374262-1024-1024.jpeg',
            # Aveia em Grão
            'https://www.nutribird.com.br/site/wp-content/uploads/2020/02/sorgo-branco.jpg',  # Sorgo Branco
            'https://agropos.com.br/wp-content/uploads/2021/06/Imagem-2023-12-18T070643.315.png',  # Trigo em Grão
        ],
        'Médio': [
            'https://images.tcdn.com.br/img/img_prod/1286719/painco_branco_1kg_7_1_e7c6f9ac32e29eb79dd6d7d0936384c5.jpeg',
            # Painço
            'https://img.freepik.com/fotos-premium/fundo-de-grao-de-milho-closeup-grao-de-milho-textura-de-grao-de-milho_71423-19.jpg',
            # Milho
            'https://images.tcdn.com.br/img/img_prod/928979/girassol_cartamo_1kg_3827_1_3c1451c932c0ce5da026036d271aa2a7.jpg',
            # Girassol Cártamo
            'https://temperosedoces.com.br/wp-content/uploads/2018/12/linhacamarrom0129.jpg',  # Linhaça Marrom
        ],
        'Grande': [
            'https://www.nutribird.com.br/site/wp-content/uploads/2019/11/girassol.jpg',  # Girassol
            'https://emporio4estrelas.vtexassets.com/arquivos/ids/156643/Amendoim-HPS-Com-Casca-Cru-500g.png?v=636908764350000000',
            # Amendoim Casca
            'https://www.sementesparapassaros.com.br/img/produtos/amendoim-graos.jpg'  # Amendoim HPS
        ]
    }
    NomeAlimentos = {
        'Pequeno': ['Alpiste', 'Níger', 'Aveia em Grão', 'Sorgo Branco', 'Trigo em Grão'],
        'Médio': ['Painço', 'Milho', 'Girassol\nCártamo', 'Linhaça Marrom'],
        'Grande': ['Girassol', 'Amendoim\nCasca', 'Amendoim HPS'],
    }

    alimentar = False

    Seg_ali_ativo = False
    Ter_ali_ativo = False
    Qua_ali_ativo = False
    Qui_ali_ativo = False
    Sex_ali_ativo = False
    Sab_ali_ativo = False
    Dom_ali_ativo = False

    VelocidadePWM = '0'

    state_dias_ali = {'Seg': False, 'Ter': False, 'Qua': False, 'Qui': False, 'Sex': False, 'Sab': False, 'Dom': False}
    horarios_alimentar_semana = {'Seg': [], 'Ter': [], 'Qua': [], 'Qui': [], 'Sex': [], 'Sab': [], 'Dom': []}
    horario_alimentar = ''
    i2 = 0

    DiasSelecionadosAli = []

    lista_botoes_seg2 = []
    lista_botoes_ter2 = []
    lista_botoes_qua2 = []
    lista_botoes_qui2 = []
    lista_botoes_sex2 = []
    lista_botoes_sab2 = []
    lista_botoes_dom2 = []

    # Clima
    temp = 0
    umidade = 0
    aquecer = False
    Temp_selec = 0

    FirstRead = True

    # MONITORAMENTO

    #firebaseConfig = {
    #    "apiKey": "AIzaSyBBTaxbeQ2n390J5GaWVSi-uzHbjJLogxE",
    #    "authDomain": "gaia-f6d06.firebaseapp.com",
    #    "databaseURL": "https://gaia-f6d06-default-rtdb.firebaseio.com",
    #    "projectId": "gaia-f6d06",
    #    "storageBucket": "gaia-f6d06.appspot.com",
    #    "messagingSenderId": "880845359113",
    #    "appId": "1:880845359113:web:8be21f5c56b1ee716e90d8",
    #    "serviceAccount": "serviceAccount.json"
    #}

    #firebase = pyrebase.initialize_app(firebaseConfig)
    #storage = firebase.storage()

    def carregar_imagem():
        url = f"https://firebasestorage.googleapis.com/v0/b/gaia-f6d06.appspot.com/o/LiveImage.jpg?alt=media&token=314018f0-4e53-478c-9dc7-2209e4a99e61"
        contador=0

        while True:
            try:
                if contador % 2 == 0:
                    image_url = f'{url}?nocache={int(time.time())}' # Forçando o recarregamento da página

                    img2.content.src = image_url
                    img2.visible = True
                    page.update()

                    time.sleep(6)
                    img1.visible = False
                    page.update()
                else:
                    image_url = f'{url}?nocache={int(time.time())}' # Forçando o recarregamento da página

                    img1.content.src = image_url
                    img1.visible = True
                    page.update()

                    time.sleep(6)
                    img2.visible = False
                    page.update()

                #print("Imagem atualizada !")
                contador+=1
            except Exception as e:
                print(f"Erro ao fazer o dowload da imagem: {e}")

    threading.Thread(target=carregar_imagem).start()

    # LENDO O BANCO DE DADOS ONLINE FIREBASE
    def Lendo_Firebase(Now=False):
        nonlocal FirstRead
        global temp
        global umidade
        nonlocal Cortina_ativa

        print("thread chamada")
        while True:
            localtime = time.localtime()
            if localtime.tm_sec == 0 or Now or FirstRead:
                FirstRead = False
                print("Lendo o Firebase")
                temp = requests.get("https://gaia-f6d06-default-rtdb.firebaseio.com/Dados/Temperatura.json")
                temp = temp.json()
                TF_temp.value = str(int(temp['temperatura'])) + '°C'
                ProgressRingTemp.value = int(temp['temperatura']) / 100

                umidade = requests.get("https://gaia-f6d06-default-rtdb.firebaseio.com/Dados/Umidade.json")
                umidade = umidade.json()
                TF_umidade.value = str(int(umidade['umidade'])) + '%'
                ProgressRingUmid.value = int(umidade['umidade']) / 100

                EstadoCortina = requests.get("https://gaia-f6d06-default-rtdb.firebaseio.com/Dados/EstadoCortina.json")
                EstadoCortina = EstadoCortina.json()
                Cortina_ativa = EstadoCortina["Cortinas"]
                MudarMostradores()

                page.update()

                Now = False
                try:
                    TF_umidade.update()
                    TF_temp.update()
                    ProgressRingTemp.update()
                    ProgressRingUmid.update()
                except AssertionError:
                    print('Elemento ainda não adicionado a página')
        pass

    thread_Firebase = threading.Thread(target=Lendo_Firebase)
    thread_Firebase.start()

    def Remove(e):
        nonlocal i
        nonlocal lista_botoes_seg
        nonlocal lista_botoes_ter
        nonlocal lista_botoes_qua
        nonlocal lista_botoes_qui
        nonlocal lista_botoes_sex
        nonlocal lista_botoes_sab
        nonlocal lista_botoes_dom
        nonlocal horarios_cortinas_semana
        print(e.control.content.value)
        if Seg_cor_ativo:
            for p, c in enumerate(lista_botoes_seg):
                if c == int(e.control.content.value):
                    del horarios_cortinas_semana['Seg'][p]
                    del list_horario_seg.controls[p]
                    del lista_botoes_seg[p]
        if Ter_cor_ativo:
            for p, c in enumerate(lista_botoes_ter):
                if c == int(e.control.content.value):
                    del horarios_cortinas_semana['Ter'][p]
                    del list_horario_ter.controls[p]
                    del lista_botoes_ter[p]
        if Qua_cor_ativo:
            for p, c in enumerate(lista_botoes_qua):
                if c == int(e.control.content.value):
                    del horarios_cortinas_semana['Qua'][p]
                    del list_horario_qua.controls[p]
                    del lista_botoes_qua[p]
        if Qui_cor_ativo:
            for p, c in enumerate(lista_botoes_qui):
                if c == int(e.control.content.value):
                    del horarios_cortinas_semana['Qui'][p]
                    del list_horario_qui.controls[p]
                    del lista_botoes_qui[p]
        if Sex_cor_ativo:
            for p, c in enumerate(lista_botoes_sex):
                if c == int(e.control.content.value):
                    del horarios_cortinas_semana['Sex'][p]
                    del list_horario_sex.controls[p]
                    del lista_botoes_sex[p]
        if Sab_cor_ativo:
            for p, c in enumerate(lista_botoes_sab):
                if c == int(e.control.content.value):
                    del horarios_cortinas_semana['Sab'][p]
                    del list_horario_sab.controls[p]
                    del lista_botoes_sab[p]
        if Dom_cor_ativo:
            for p, c in enumerate(lista_botoes_dom):
                if c == int(e.control.content.value):
                    del horarios_cortinas_semana['Dom'][p]
                    del list_horario_dom.controls[p]
                    del lista_botoes_dom[p]
        SalvarDados()
        Salvar_dados_no_firebase(__HorariosCortinas=True)
        page.update()

    def adicionar_cor(e):
        Text_field_abre = ''
        Text_field_fecha = ''
        digit_1 = ''
        digit_2 = ''
        erro = False

        # VERIFICANDO QUAL DIA ESTÁ ATIVO PARA SABER QUAL TEXT FIELD SERÁ VERIFICADO
        if Seg_cor_ativo:
            Text_field_abre = Text_field_abre_seg.value
            Text_field_fecha = Text_field_fecha_seg.value
        if Ter_cor_ativo:
            Text_field_abre = Text_field_abre_ter.value
            Text_field_fecha = Text_field_fecha_ter.value
        if Qua_cor_ativo:
            Text_field_abre = Text_field_abre_qua.value
            Text_field_fecha = Text_field_fecha_qua.value
        if Qui_cor_ativo:
            Text_field_abre = Text_field_abre_qui.value
            Text_field_fecha = Text_field_fecha_qui.value
        if Sex_cor_ativo:
            Text_field_abre = Text_field_abre_sex.value
            Text_field_fecha = Text_field_fecha_sex.value
        if Sab_cor_ativo:
            Text_field_abre = Text_field_abre_sab.value
            Text_field_fecha = Text_field_fecha_sab.value
        if Dom_cor_ativo:
            Text_field_abre = Text_field_abre_dom.value
            Text_field_fecha = Text_field_fecha_dom.value

        Text_field_fecha = str(Text_field_fecha)
        Text_field_abre = str(Text_field_abre)

        for numero in Text_field_abre:
            if numero.isalpha():
                erro = True
                break
        for numero in Text_field_fecha:
            if numero.isalpha():
                erro = True
                break

        # TEXT FIELD ABRE
        # TRATAMENO DO ERRO INPUT COM MAIS DE 5 CARACTERES:
        print(erro)
        if len(Text_field_abre) > 5 and not erro:
            erro = True
        elif not erro:
            digit_1 = Text_field_abre[0] + Text_field_abre[1]
            if digit_1.find(':') != -1:
                digit_1 = '0' + digit_1
                digit_1 = digit_1.replace(':', '')
                try:
                    digit_2 = Text_field_abre[2] + Text_field_abre[3]
                except IndexError:
                    digit_2 = Text_field_abre[2] + '0'
            else:
                try:
                    digit_2 = Text_field_abre[3] + Text_field_abre[4]
                except IndexError:
                    digit_2 = Text_field_abre[3] + '0'
            # TRATAMENO DO ERRO DIGITOS MAIORES QUE 24 E 59:
        if not erro:
            if int(digit_1) > 24 or int(digit_2) > 59:
                erro = True
            elif not erro:
                Text_field_abre = digit_1 + ':' + digit_2

            # TEXT FIELD FECHA
            # TRATAMENO DO ERRO DE INPUT TEM MAIS DE 5 CARACTERES:
        if len(Text_field_fecha) > 5 and not erro:
            erro = True
        elif not erro:
            digit_1 = Text_field_fecha[0] + Text_field_fecha[1]
            if digit_1.find(':') != -1:
                digit_1 = '0' + digit_1
                digit_1 = digit_1.replace(':', '')
                try:
                    digit_2 = Text_field_fecha[2] + Text_field_fecha[3]
                except IndexError:
                    digit_2 = Text_field_fecha[2] + '0'
            else:
                try:
                    digit_2 = Text_field_fecha[3] + Text_field_fecha[4]
                except IndexError:
                    digit_2 = Text_field_fecha[3] + '0'
            # TRATAMENO DO ERRO HORARIOS MAIORES QUE 23H E 59MIN:
        if not erro:
            if int(digit_1) > 23 or int(digit_2) > 59:
                erro = True
            elif not erro:
                Text_field_fecha = digit_1 + ':' + digit_2

            # TRATAMENO DO ERRO DA HORA DE FECHAR SER A MESMA DE ABRIR:
        if Text_field_fecha == Text_field_abre:
            erro = True
            # TRATAMENO DO ERRO CARACTERES NAS POSIÇÕES DOS NUMEROS:
            # ABRE
        if not Text_field_abre == '':
            for p, c in enumerate(Text_field_abre):
                if not c.isdecimal():
                    if not (c == ':' and p == 2) or c == '':
                        erro = True
                        break
        else:
            erro = True

            # FECHA
        if not Text_field_fecha == '':
            for p, c in enumerate(Text_field_fecha):
                if not c.isdecimal() or c == '':
                    if not (c == ':' and p == 2):
                        erro = True
                        break
        else:
            erro = True

        if erro:
            # VERIFICANDO QUAL DIA ESTA ATIVO PARA MANDA A MENSAGEM DE ERRO NO TEXT FIELD SELECIONADO
            if Seg_cor_ativo:
                Text_field_abre_seg.value = 'Erro.'
                Text_field_fecha_seg.value = 'Erro.'
                Text_field_abre_seg.update()
                Text_field_fecha_seg.update()
                page.update()
                print('Erro')
                print(erro)
            if Ter_cor_ativo:
                Text_field_abre_ter.value = 'Erro.'
                Text_field_fecha_ter.value = 'Erro.'
                Text_field_abre_ter.update()
                Text_field_fecha_ter.update()
                page.update()
                print('Erro')
                print(erro)
            if Qua_cor_ativo:
                Text_field_abre_qua.value = 'Erro.'
                Text_field_fecha_qua.value = 'Erro.'
                Text_field_abre_qua.update()
                Text_field_fecha_qua.update()
                page.update()
                print('Erro')
                print(erro)
            if Qui_cor_ativo:
                Text_field_abre_qui.value = 'Erro.'
                Text_field_fecha_qui.value = 'Erro.'
                Text_field_abre_qui.update()
                Text_field_fecha_qui.update()
                page.update()
                print('Erro')
                print(erro)
            if Sex_cor_ativo:
                Text_field_abre_sex.value = 'Erro.'
                Text_field_fecha_sex.value = 'Erro.'
                Text_field_abre_sex.update()
                Text_field_fecha_sex.update()
                page.update()
                print('Erro')
                print(erro)
            if Sab_cor_ativo:
                Text_field_abre_sab.value = 'Erro.'
                Text_field_fecha_sab.value = 'Erro.'
                Text_field_abre_sab.update()
                Text_field_fecha_sab.update()
                page.update()
                print('Erro')
                print(erro)
            if Dom_cor_ativo:
                Text_field_abre_dom.value = 'Erro.'
                Text_field_fecha_dom.value = 'Erro.'
                Text_field_abre_dom.update()
                Text_field_fecha_dom.update()
                page.update()
                print('Erro')
                print(erro)
        else:
            # PROXIMO DIA ?
            if int(Text_field_fecha[:2]) > int(Text_field_abre[:2]):  # SE A HORA DE FECHAR FOR DEPOIS DE ABRIR E SE FOREM IGUAIS TEREMOS QUE VERIFICAR OS MINUTOS
                page.dialog = msg_proximo_dia
                msg_proximo_dia.open = True  # SE O MINUTO DA HORA DE FECHAR FOR MAIOR DA DE ABRIR = proximo_dia()
                page.update()
            elif int(Text_field_fecha[:2]) == int(Text_field_abre[:2]) and int(Text_field_fecha[3:]) > int(Text_field_abre[3:]):
                print(Text_field_fecha[:2], Text_field_abre[:2])
                page.dialog = msg_proximo_dia
                msg_proximo_dia.open = True
                page.update()
            else:
                RegistroCor(Text_field_abre=Text_field_abre, Text_field_fecha=Text_field_fecha)

    # REGISTRANDO A HORA NO APP
    def RegistroCor(Text_field_abre='', Text_field_fecha=''):
        nonlocal horario_cortinas
        nonlocal i
        int(i)
        i += 1

        horario_cortinas['abre'] = Text_field_abre
        horario_cortinas['fecha'] = Text_field_fecha

        if Seg_cor_ativo:
            horarios_cortinas_semana['Seg'].append(horario_cortinas)
            lista_botoes_seg.append(i)
            print(lista_botoes_seg)
            list_horario_seg.controls.append(
                ft.Container(bgcolor=verde1, height=60, border_radius=10, offset=ft.transform.Offset(-0.05, 0),
                             content=ft.Row(width=200,
                                            controls=[
                                                ft.Text(
                                                    offset=ft.transform.Offset(0.03, 0),
                                                    value=f'Fechará as {Text_field_fecha}H, abrirá as {Text_field_abre[:5] + "H" + Text_field_abre[5:]}',
                                                    color=branco2,
                                                    size=12.5,
                                                ),
                                                ft.IconButton(icon=ft.icons.REMOVE, on_click=Remove,
                                                              offset=ft.transform.Offset(1.1, 0) if len(
                                                                  Text_field_abre) < 6 else ft.transform.Offset(0.5, 0),
                                                              icon_color=branco2,
                                                              content=ft.Text(value=f'{i}'))
                                            ], )))
            Text_field_fecha_seg.value = ''
            Text_field_abre_seg.value = ''
            Text_field_fecha_seg.update()
            Text_field_abre_seg.update()
        if Ter_cor_ativo:
            horarios_cortinas_semana['Ter'].append(horario_cortinas)
            lista_botoes_ter.append(i)
            list_horario_ter.controls.append(
                ft.Container(bgcolor=verde1, height=60, border_radius=10, offset=ft.transform.Offset(-0.05, 0),
                             content=ft.Row(width=100,
                                            controls=[
                                                ft.Text(
                                                    offset=ft.transform.Offset(0.03, 0),
                                                    value=f'Fechará as {Text_field_fecha}H, abrirá as {Text_field_abre[:5] + "H" + Text_field_abre[5:]}',
                                                    color=branco2,
                                                    size=12.5,
                                                ),
                                                ft.IconButton(icon=ft.icons.REMOVE, on_click=Remove,
                                                              offset=ft.transform.Offset(1.1, 0) if len(
                                                                  Text_field_abre) < 6 else ft.transform.Offset(0.5, 0),
                                                              icon_color=branco2, content=ft.Text(value=f'{i}'))
                                            ], )))
            Text_field_fecha_ter.value = ''
            Text_field_abre_ter.value = ''
            Text_field_fecha_ter.update()
            Text_field_abre_ter.update()
        if Qua_cor_ativo:
            horarios_cortinas_semana['Qua'].append(horario_cortinas)
            lista_botoes_qua.append(i)
            list_horario_qua.controls.append(
                ft.Container(bgcolor=verde1, height=60, border_radius=10, offset=ft.transform.Offset(-0.05, 0),
                             content=ft.Row(width=100,
                                            controls=[
                                                ft.Text(
                                                    offset=ft.transform.Offset(0.03, 0),
                                                    value=f'Fechará as {Text_field_fecha}H, abrirá as {Text_field_abre[:5] + "H" + Text_field_abre[5:]}',
                                                    color=branco2,
                                                    size=12.5,
                                                ),
                                                ft.IconButton(icon=ft.icons.REMOVE, on_click=Remove,
                                                              offset=ft.transform.Offset(1.1, 0) if len(
                                                                  Text_field_abre) < 6 else ft.transform.Offset(0.5, 0),
                                                              icon_color=branco2, content=ft.Text(value=f'{i}'))
                                            ], )))
            Text_field_fecha_qua.value = ''
            Text_field_abre_qua.value = ''
            Text_field_fecha_qua.update()
            Text_field_abre_qua.update()
        if Qui_cor_ativo:
            horarios_cortinas_semana['Qui'].append(horario_cortinas)
            lista_botoes_qui.append(i)
            list_horario_qui.controls.append(
                ft.Container(bgcolor=verde1, height=60, border_radius=10, offset=ft.transform.Offset(-0.05, 0),
                             content=ft.Row(width=100,
                                            controls=[
                                                ft.Text(
                                                    offset=ft.transform.Offset(0.03, 0),
                                                    value=f'Fechará as {Text_field_fecha}H, abrirá as {Text_field_abre[:5] + "H" + Text_field_abre[5:]}',
                                                    color=branco2,
                                                    size=12.5,
                                                ),
                                                ft.IconButton(icon=ft.icons.REMOVE, on_click=Remove,
                                                              offset=ft.transform.Offset(1.1, 0) if len(
                                                                  Text_field_abre) < 6 else ft.transform.Offset(0.5, 0),
                                                              icon_color=branco2, content=ft.Text(value=f'{i}'))
                                            ], )))
            Text_field_fecha_qui.value = ''
            Text_field_abre_qui.value = ''
            Text_field_fecha_qui.update()
            Text_field_abre_qui.update()
        if Sex_cor_ativo:
            horarios_cortinas_semana['Sex'].append(horario_cortinas)
            lista_botoes_sex.append(i)
            list_horario_sex.controls.append(
                ft.Container(bgcolor=verde1, height=60, border_radius=10, offset=ft.transform.Offset(-0.05, 0),
                             content=ft.Row(width=100,
                                            controls=[
                                                ft.Text(
                                                    offset=ft.transform.Offset(0.03, 0),
                                                    value=f'Fechará as {Text_field_fecha}H, abrirá as {Text_field_abre[:5] + "H" + Text_field_abre[5:]}',
                                                    color=branco2,
                                                    size=12.5,
                                                ),
                                                ft.IconButton(icon=ft.icons.REMOVE, on_click=Remove,
                                                              offset=ft.transform.Offset(1.1, 0) if len(
                                                                  Text_field_abre) < 6 else ft.transform.Offset(0.5, 0),
                                                              icon_color=branco2, content=ft.Text(value=f'{i}'))
                                            ], )))
            Text_field_fecha_sex.value = ''
            Text_field_abre_sex.value = ''
            Text_field_fecha_sex.update()
            Text_field_abre_sex.update()
        if Sab_cor_ativo:
            horarios_cortinas_semana['Sab'].append(horario_cortinas)
            lista_botoes_sab.append(i)
            list_horario_sab.controls.append(
                ft.Container(bgcolor=verde1, height=60, border_radius=10, offset=ft.transform.Offset(-0.05, 0),
                             content=ft.Row(width=100,
                                            controls=[
                                                ft.Text(
                                                    offset=ft.transform.Offset(0.03, 0),
                                                    value=f'Fechará as {Text_field_fecha}H, abrirá as {Text_field_abre[:5] + "H" + Text_field_abre[5:]}',
                                                    color=branco2,
                                                    size=12.5,
                                                ),
                                                ft.IconButton(icon=ft.icons.REMOVE, on_click=Remove,
                                                              offset=ft.transform.Offset(1.1, 0) if len(
                                                                  Text_field_abre) < 6 else ft.transform.Offset(0.5, 0),
                                                              icon_color=branco2, content=ft.Text(value=f'{i}'))
                                            ], )))
            Text_field_fecha_sab.value = ''
            Text_field_abre_sab.value = ''
            Text_field_fecha_sab.update()
            Text_field_abre_sab.update()
        if Dom_cor_ativo:
            horarios_cortinas_semana['Dom'].append(horario_cortinas)
            lista_botoes_dom.append(i)
            list_horario_dom.controls.append(
                ft.Container(bgcolor=verde1, height=60, border_radius=10, offset=ft.transform.Offset(-0.05, 0),
                             content=ft.Row(width=100,
                                            controls=[
                                                ft.Text(
                                                    offset=ft.transform.Offset(0.03, 0),
                                                    value=f'Fechará as {Text_field_fecha}H, abrirá as {Text_field_abre[:5] + "H" + Text_field_abre[5:]}',
                                                    color=branco2,
                                                    size=12.5,
                                                ),
                                                ft.IconButton(icon=ft.icons.REMOVE, on_click=Remove,
                                                              offset=ft.transform.Offset(1.1, 0) if len(
                                                                  Text_field_abre) < 6 else ft.transform.Offset(0.5, 0),
                                                              icon_color=branco2, content=ft.Text(value=f'{i}'))
                                            ], )))
            Text_field_fecha_dom.value = ''
            Text_field_abre_dom.value = ''
            Text_field_fecha_dom.update()
            Text_field_abre_dom.update()
        SalvarDados()
        Salvar_dados_no_firebase(__HorariosCortinas=True)
        page.update()

    def RestaurarHorarioCortinas(e=False):
        print('Função chamada')
        nonlocal horarios_cortinas_semana
        nonlocal lista_botoes_seg
        nonlocal lista_botoes_ter
        nonlocal lista_botoes_qua
        nonlocal lista_botoes_qui
        nonlocal lista_botoes_sex
        nonlocal lista_botoes_sab
        nonlocal lista_botoes_dom
        nonlocal count_cortinas
        # Segunda
        if not e or count_cortinas == 0:
            if isinstance(horarios_cortinas_semana['Seg'], list):
                for p, c in enumerate(lista_botoes_seg):
                    list_horario_seg.controls.append(
                        ft.Container(bgcolor=verde1, height=60, border_radius=10, offset=ft.transform.Offset(-0.05, 0),
                                     content=ft.Row(width=100,
                                                    controls=[
                                                        ft.Text(
                                                            offset=ft.transform.Offset(0.03, 0),
                                                            # Fechará as {horarios_cortinas_semana['Seg'][p]['fecha']}, abrirá as {horarios_cortinas_semana['Seg'][p]['abre']
                                                            value=f"Fechará as {horarios_cortinas_semana['Seg'][p]['fecha']}, abrirá as {horarios_cortinas_semana['Seg'][p]['abre']}" if len(
                                                                horarios_cortinas_semana['Seg'][p][
                                                                    'abre']) < 6 else f"Fechará as {horarios_cortinas_semana['Seg'][p]['fecha']}, abrirá as {horarios_cortinas_semana['Seg'][p]['abre'][:5]}" + 'H' + f"{horarios_cortinas_semana['Seg'][p]['abre'][5:]}",
                                                            color=branco2,
                                                            size=12.5,
                                                        ),
                                                        ft.IconButton(icon=ft.icons.REMOVE, on_click=Remove,
                                                                      icon_color=branco2, content=ft.Text(value=f'{c}'),
                                                                      offset=ft.transform.Offset(1.5, 0) if len(
                                                                          horarios_cortinas_semana['Seg'][p][
                                                                              'abre']) < 6 else ft.transform.Offset(0.7,
                                                                                                                    0),
                                                                      )
                                                    ], )))
                list_horario_seg.update()
            # Terca
            if isinstance(horarios_cortinas_semana['Ter'], list):
                for p, c in enumerate(lista_botoes_ter):
                    list_horario_ter.controls.append(
                        ft.Container(bgcolor=verde1, height=60, border_radius=10, offset=ft.transform.Offset(-0.05, 0),
                                     content=ft.Row(width=100,
                                                    controls=[
                                                        ft.Text(
                                                            offset=ft.transform.Offset(0.03, 0),
                                                            value=f"Fechará as {horarios_cortinas_semana['Ter'][p]['fecha']}, abrirá as {horarios_cortinas_semana['Ter'][p]['abre']}" if len(
                                                                horarios_cortinas_semana['Ter'][p][
                                                                    'abre']) < 6 else f"Fechará as {horarios_cortinas_semana['Ter'][p]['fecha']}, abrirá as {horarios_cortinas_semana['Ter'][p]['abre'][:5]}" + 'H' + f"{horarios_cortinas_semana['Ter'][p]['abre'][5:]}",
                                                            color=branco2,
                                                            size=12.5,
                                                        ),
                                                        ft.IconButton(icon=ft.icons.REMOVE, on_click=Remove,
                                                                      icon_color=branco2,
                                                                      content=ft.Text(value=f'{c}'),
                                                                      offset=ft.transform.Offset(1.5, 0) if len(
                                                                          horarios_cortinas_semana['Ter'][p][
                                                                              'abre']) < 6 else ft.transform.Offset(0.7,
                                                                                                                    0),
                                                                      )
                                                    ], )))
                list_horario_ter.update()
            # Quarta
            if isinstance(horarios_cortinas_semana['Qua'], list):
                for p, c in enumerate(lista_botoes_qua):
                    list_horario_qua.controls.append(
                        ft.Container(bgcolor=verde1, height=60, border_radius=10,
                                     offset=ft.transform.Offset(-0.05, 0),
                                     content=ft.Row(width=100,
                                                    controls=[
                                                        ft.Text(
                                                            offset=ft.transform.Offset(0.03, 0),
                                                            value=f"Fechará as {horarios_cortinas_semana['Qua'][p]['fecha']}, abrirá as {horarios_cortinas_semana['Qua'][p]['abre']}" if len(
                                                                horarios_cortinas_semana['Qua'][p][
                                                                    'abre']) < 6 else f"Fechará as {horarios_cortinas_semana['Qua'][p]['fecha']}, abrirá as {horarios_cortinas_semana['Qua'][p]['abre'][:5]}" + 'H' + f"{horarios_cortinas_semana['Qua'][p]['abre'][5:]}",
                                                            color=branco2,
                                                            size=12.5,
                                                        ),
                                                        ft.IconButton(icon=ft.icons.REMOVE, on_click=Remove,
                                                                      icon_color=branco2,
                                                                      content=ft.Text(value=f'{c}'),
                                                                      offset=ft.transform.Offset(1.5, 0) if len(
                                                                          horarios_cortinas_semana['Qua'][p][
                                                                              'abre']) < 6 else ft.transform.Offset(0.7,
                                                                                                                    0),
                                                                      )
                                                    ], )))
                list_horario_qua.update()
            # Quinta
            if isinstance(horarios_cortinas_semana['Qui'], list):
                for p, c in enumerate(lista_botoes_qui):
                    list_horario_qui.controls.append(
                        ft.Container(bgcolor=verde1, height=60, border_radius=10, offset=ft.transform.Offset(-0.05, 0),
                                     content=ft.Row(width=100,
                                                    controls=[
                                                        ft.Text(
                                                            offset=ft.transform.Offset(0.03, 0),
                                                            value=f"Fechará as {horarios_cortinas_semana['Qui'][p]['fecha']}, abrirá as {horarios_cortinas_semana['Qui'][p]['abre']}" if len(
                                                                horarios_cortinas_semana['Qui'][p][
                                                                    'abre']) < 6 else f"Fechará as {horarios_cortinas_semana['Qui'][p]['fecha']}, abrirá as {horarios_cortinas_semana['Qui'][p]['abre'][:5]}" + 'H' + f"{horarios_cortinas_semana['Qui'][p]['abre'][5:]}",
                                                            color=branco2,
                                                            size=12.5,
                                                        ),
                                                        ft.IconButton(icon=ft.icons.REMOVE, on_click=Remove,
                                                                      icon_color=branco2,
                                                                      content=ft.Text(value=f'{c}'),
                                                                      offset=ft.transform.Offset(1.5, 0) if len(
                                                                          horarios_cortinas_semana['Qui'][p][
                                                                              'abre']) < 6 else ft.transform.Offset(0.7,
                                                                                                                    0),
                                                                      )
                                                    ], )))
                list_horario_qui.update()
            # Sexta
            if isinstance(horarios_cortinas_semana['Sex'], list):
                for p, c in enumerate(lista_botoes_sex):
                    list_horario_sex.controls.append(
                        ft.Container(bgcolor=verde1, height=60, border_radius=10, offset=ft.transform.Offset(-0.05, 0),
                                     content=ft.Row(width=100,
                                                    controls=[
                                                        ft.Text(
                                                            offset=ft.transform.Offset(0.03, 0),
                                                            value=f"Fechará as {horarios_cortinas_semana['Sex'][p]['fecha']}, abrirá as {horarios_cortinas_semana['Sex'][p]['abre']}" if len(
                                                                horarios_cortinas_semana['Sex'][p][
                                                                    'abre']) < 6 else f"Fechará as {horarios_cortinas_semana['Sex'][p]['fecha']}, abrirá as {horarios_cortinas_semana['Sex'][p]['abre'][:5]}" + 'H' + f"{horarios_cortinas_semana['Sex'][p]['abre'][5:]}",
                                                            color=branco2,
                                                            size=12.5,
                                                        ),
                                                        ft.IconButton(icon=ft.icons.REMOVE, on_click=Remove,
                                                                      icon_color=branco2,
                                                                      content=ft.Text(value=f'{c}'),
                                                                      offset=ft.transform.Offset(1.5, 0) if len(
                                                                          horarios_cortinas_semana['Sex'][p][
                                                                              'abre']) < 6 else ft.transform.Offset(0.7,
                                                                                                                    0),
                                                                      )
                                                    ], )))
                list_horario_sex.update()
            # Sabado
            if isinstance(horarios_cortinas_semana['Sab'], list):
                for p, c in enumerate(lista_botoes_sab):
                    list_horario_sab.controls.append(
                        ft.Container(bgcolor=verde1, height=60, border_radius=10, offset=ft.transform.Offset(-0.05, 0),
                                     content=ft.Row(width=100,
                                                    controls=[
                                                        ft.Text(
                                                            offset=ft.transform.Offset(0.03, 0),
                                                            value=f"Fechará as {horarios_cortinas_semana['Sab'][p]['fecha']}, abrirá as {horarios_cortinas_semana['Sab'][p]['abre']}" if len(
                                                                horarios_cortinas_semana['Sab'][p][
                                                                    'abre']) < 6 else f"Fechará as {horarios_cortinas_semana['Sab'][p]['fecha']}, abrirá as {horarios_cortinas_semana['Sab'][p]['abre'][:5]}" + 'H' + f"{horarios_cortinas_semana['Sab'][p]['abre'][5:]}",
                                                            color=branco2,
                                                            size=12.5,
                                                        ),
                                                        ft.IconButton(icon=ft.icons.REMOVE, on_click=Remove,
                                                                      icon_color=branco2,
                                                                      content=ft.Text(value=f'{c}'),
                                                                      offset=ft.transform.Offset(1.5, 0) if len(
                                                                          horarios_cortinas_semana['Sab'][p][
                                                                              'abre']) < 6 else ft.transform.Offset(0.7,
                                                                                                                    0),
                                                                      )
                                                    ], )))
                list_horario_sab.update()
            # Domingo
            if isinstance(horarios_cortinas_semana['Dom'], list):
                for p, c in enumerate(lista_botoes_dom):
                    list_horario_dom.controls.append(
                        ft.Container(bgcolor=verde1, height=60, border_radius=10, offset=ft.transform.Offset(-0.05, 0),
                                     content=ft.Row(width=100,
                                                    controls=[
                                                        ft.Text(
                                                            offset=ft.transform.Offset(0.03, 0),
                                                            value=f"Fechará as {horarios_cortinas_semana['Dom'][p]['fecha']}H, abrirá as {horarios_cortinas_semana['Dom'][p]['abre']}H" if len(
                                                                horarios_cortinas_semana['Dom'][p][
                                                                    'abre']) < 6 else f"Fechará as {horarios_cortinas_semana['Dom'][p]['fecha']}H, abrirá as {horarios_cortinas_semana['Dom'][p]['abre'][:5]}" + 'H' + f"{horarios_cortinas_semana['Dom'][p]['abre'][5:]}",
                                                            color=branco2,
                                                            size=12.5,
                                                        ),
                                                        ft.IconButton(icon=ft.icons.REMOVE, on_click=Remove,
                                                                      icon_color=branco2,
                                                                      content=ft.Text(value=f'{c}'),
                                                                      offset=ft.transform.Offset(1.5, 0) if len(
                                                                          horarios_cortinas_semana['Dom'][p][
                                                                              'abre']) < 6 else ft.transform.Offset(0.7,
                                                                                                                    0),
                                                                      )
                                                    ], )))
                list_horario_dom.update()
            count_cortinas = 1

    def proximo_dia(e):
        erro = False

        # if e.control.content.value == 'Sim':
        if Seg_cor_ativo:
            Text_field_abre = Text_field_abre_seg.value
            Text_field_fecha = Text_field_fecha_seg.value

        if Ter_cor_ativo:
            Text_field_abre = Text_field_abre_ter.value
            Text_field_fecha = Text_field_fecha_ter.value

        if Qua_cor_ativo:
            Text_field_abre = Text_field_abre_qua.value
            Text_field_fecha = Text_field_fecha_qua.value

        if Qui_cor_ativo:
            Text_field_abre = Text_field_abre_qui.value
            Text_field_fecha = Text_field_fecha_qui.value

        if Sex_cor_ativo:
            Text_field_abre = Text_field_abre_sex.value
            Text_field_fecha = Text_field_fecha_sex.value

        if Sab_cor_ativo:
            Text_field_abre = Text_field_abre_sab.value
            Text_field_fecha = Text_field_fecha_sab.value

        if Dom_cor_ativo:
            Text_field_abre = Text_field_abre_dom.value
            Text_field_fecha = Text_field_fecha_dom.value

        if e.control.content.value == 'Não':
            erro = True

        # TEXT FIELD ABRE
        # TRATAMENO DO ERRO INPUT COM MAIS DE 5 CARACTERES:
        if len(Text_field_abre) > 5:
            erro = True
        else:
            digit_1 = Text_field_abre[0] + Text_field_abre[1]
            if digit_1.find(':') != -1:
                digit_1 = '0' + digit_1
                digit_1 = digit_1.replace(':', '')
                try:
                    digit_2 = Text_field_abre[2] + Text_field_abre[3]
                except IndexError:
                    digit_2 = Text_field_abre[2] + '0'
            else:
                try:
                    digit_2 = Text_field_abre[3] + Text_field_abre[4]
                except IndexError:
                    digit_2 = Text_field_abre[3] + '0'
            # TRATAMENO DO ERRO DIGITOS MAIORES QUE 24 E 59:
        if int(digit_1) > 24 or int(digit_2) > 59:
            erro = True
        else:
            Text_field_abre = digit_1 + ':' + digit_2

            # TEXT FIELD FECHA
            # TRATAMENO DO ERRO DE INPUT TEM MAIS DE 5 CARACTERES:
        if len(Text_field_fecha) > 5:
            erro = True
        else:
            digit_1 = Text_field_fecha[0] + Text_field_fecha[1]
            if digit_1.find(':') != -1:
                digit_1 = '0' + digit_1
                digit_1 = digit_1.replace(':', '')
                try:
                    digit_2 = Text_field_fecha[2] + Text_field_fecha[3]
                except IndexError:
                    digit_2 = Text_field_fecha[2] + '0'
            else:
                try:
                    digit_2 = Text_field_fecha[3] + Text_field_fecha[4]
                except IndexError:
                    digit_2 = Text_field_fecha[3] + '0'
            # TRATAMENO DO ERRO HORARIOS MAIORES QUE 23H E 59MIN:
        if int(digit_1) > 23 or int(digit_2) > 59:
            erro = True
        else:
            Text_field_fecha = digit_1 + ':' + digit_2
            # TRATAMENO DO ERRO DA HORA DE FECHAR SER A MESMA DE ABRIR:
        if Text_field_fecha == Text_field_abre:
            erro = True
            # TRATAMENO DO ERRO CARACTERES NAS POSIÇÕES DOS NUMEROS:
            # ABRE
        if not Text_field_abre == '':
            for p, c in enumerate(Text_field_abre):
                if not c.isdecimal():
                    if not (c == ':' and p == 2) or c == '':
                        erro = True
                        break
        else:
            erro = True

            # FECHA
        if not Text_field_fecha == '':
            for p, c in enumerate(Text_field_fecha):
                if not c.isdecimal() or c == '':
                    if not (c == ':' and p == 2):
                        erro = True
                        break
        else:
            erro = True

        if erro:
            # VERIFICANDO QUAL DIA ESTA ATIVO PARA MANDA A MENSAGEM DE ERRO NO TEXT FIELD SELECIONADO
            if Seg_cor_ativo:
                Text_field_abre_seg.value = 'Erro.'
                Text_field_fecha_seg.value = 'Erro.'
                Text_field_abre_seg.update()
                Text_field_fecha_seg.update()
                page.update()
                print('Erro')
            if Ter_cor_ativo:
                Text_field_abre_ter.value = 'Erro.'
                Text_field_fecha_ter.value = 'Erro.'
                Text_field_abre_ter.update()
                Text_field_fecha_ter.update()
                page.update()
                print('Erro')
            if Qua_cor_ativo:
                Text_field_abre_qua.value = 'Erro.'
                Text_field_fecha_qua.value = 'Erro.'
                Text_field_abre_qua.update()
                Text_field_fecha_qua.update()
                page.update()
                print('Erro')
            if Qui_cor_ativo:
                Text_field_abre_qui.value = 'Erro.'
                Text_field_fecha_qui.value = 'Erro.'
                Text_field_abre_qui.update()
                Text_field_fecha_qui.update()
                page.update()
                print('Erro')
            if Sex_cor_ativo:
                Text_field_abre_sex.value = 'Erro.'
                Text_field_fecha_sex.value = 'Erro.'
                Text_field_abre_sex.update()
                Text_field_fecha_sex.update()
                page.update()
                print('Erro')
            if Sab_cor_ativo:
                Text_field_abre_sab.value = 'Erro.'
                Text_field_fecha_sab.value = 'Erro.'
                Text_field_abre_sab.update()
                Text_field_fecha_sab.update()
                page.update()
                print('Erro')
            if Dom_cor_ativo:
                Text_field_abre_dom.value = 'Erro.'
                Text_field_fecha_dom.value = 'Erro.'
                Text_field_abre_dom.update()
                Text_field_fecha_dom.update()
                page.update()
                print('Erro')

        if not erro:
            if Seg_cor_ativo:
                Text_field_abre = Text_field_abre + "(Ter)"
            if Ter_cor_ativo:
                Text_field_abre = Text_field_abre + "(Qua)"
            if Qua_cor_ativo:
                Text_field_abre = Text_field_abre + "(Qui)"
            if Qui_cor_ativo:
                Text_field_abre = Text_field_abre + "(Sex)"
            if Sex_cor_ativo:
                Text_field_abre = Text_field_abre + "(Sáb)"
            if Sab_cor_ativo:
                Text_field_abre = Text_field_abre + "(Dom)"
            if Dom_cor_ativo:
                Text_field_abre = Text_field_abre + "(Seg)"

            SalvarDados()
            RegistroCor(Text_field_abre=Text_field_abre, Text_field_fecha=Text_field_fecha)
        msg_proximo_dia.open = False
        page.update()

    # FUNÇÕES DAS SETAS, QUE AO SEREM ACIONADAS EXIBEM O CAMPO PARA DIGITAÇÃO DA HORA DE SEUS RESPECTIVOS DIAS
    # Segunda cortinas
    def Segunda(e):
        if 'Seg' in DiasSelecionados:
            nonlocal Seg_cor_ativo
            nonlocal Ter_cor_ativo
            nonlocal Qua_cor_ativo
            nonlocal Qui_cor_ativo
            nonlocal Sex_cor_ativo
            nonlocal Sab_cor_ativo
            nonlocal Dom_cor_ativo
            if e:
                Seg_cor_ativo = not Seg_cor_ativo
            if Seg_cor_ativo:
                Seg_cor.content.visible = True
                set_segunda.rotate.angle = 1.5
                Dom_cor.content.visible = False  # Desativando o content dos outros dias
                Ter_cor.content.visible = False
                Qua_cor.content.visible = False
                Qui_cor.content.visible = False
                Sex_cor.content.visible = False
                Sab_cor.content.visible = False
                Ter_cor_ativo = False  # Desativando a Flag de content ativo dos outros dias
                Qua_cor_ativo = False
                Qui_cor_ativo = False
                Sex_cor_ativo = False
                Sab_cor_ativo = False
                Dom_cor_ativo = False
                set_terca.rotate.angle = 0  # Voltando as outras setas para a posição normal
                set_quarta.rotate.angle = 0
                set_quinta.rotate.angle = 0
                set_sexta.rotate.angle = 0
                set_sabado.rotate.angle = 0
                set_domingo.rotate.angle = 0
            else:
                set_segunda.rotate.angle = 0
                Seg_cor.content.visible = False
        else:
            Seg_cor.content.visible = False
        set_segunda.update()
        SalvarDados()
        page.update()

    # Terça cortinas
    def Terca(e):
        if 'Ter' in DiasSelecionados:
            nonlocal Seg_cor_ativo
            nonlocal Ter_cor_ativo
            nonlocal Qua_cor_ativo
            nonlocal Qui_cor_ativo
            nonlocal Sex_cor_ativo
            nonlocal Sab_cor_ativo
            nonlocal Dom_cor_ativo
            Ter_cor_ativo = not Ter_cor_ativo
            if Ter_cor_ativo:
                Ter_cor.content.visible = True
                set_terca.rotate.angle = 1.5
                Seg_cor.content.visible = False  # Desativando o content dos outros dias
                Dom_cor.content.visible = False
                Qua_cor.content.visible = False
                Qui_cor.content.visible = False
                Sex_cor.content.visible = False
                Sab_cor.content.visible = False
                Seg_cor_ativo = False  # Desativando a Flag de content ativo dos outros dias
                Qua_cor_ativo = False
                Qui_cor_ativo = False
                Sex_cor_ativo = False
                Sab_cor_ativo = False
                Dom_cor_ativo = False
                set_segunda.rotate.angle = 0  # Voltando as outras setas para a posição normal
                set_quarta.rotate.angle = 0
                set_quinta.rotate.angle = 0
                set_sexta.rotate.angle = 0
                set_sabado.rotate.angle = 0
                set_domingo.rotate.angle = 0
            else:
                set_terca.rotate.angle = 0
                Ter_cor.content.visible = False
        else:
            Ter_cor.content.visible = False
        set_terca.update()
        SalvarDados()
        page.update()

    # Quarta cortinas
    def Quarta(e):
        if 'Qua' in DiasSelecionados:
            nonlocal Seg_cor_ativo
            nonlocal Ter_cor_ativo
            nonlocal Qua_cor_ativo
            nonlocal Qui_cor_ativo
            nonlocal Sex_cor_ativo
            nonlocal Sab_cor_ativo
            nonlocal Dom_cor_ativo
            Qua_cor_ativo = not Qua_cor_ativo
            if Qua_cor_ativo:
                Qua_cor.content.visible = True
                set_quarta.rotate.angle = 1.5
                Seg_cor.content.visible = False  # Desativando o content dos outros dias
                Ter_cor.content.visible = False
                Dom_cor.content.visible = False
                Qui_cor.content.visible = False
                Sex_cor.content.visible = False
                Sab_cor.content.visible = False
                Seg_cor_ativo = False  # Desativando a Flag de content ativo dos outros dias
                Ter_cor_ativo = False
                Qui_cor_ativo = False
                Sex_cor_ativo = False
                Sab_cor_ativo = False
                Dom_cor_ativo = False
                set_terca.rotate.angle = 0  # Voltando as outras setas para a posição normal
                set_segunda.rotate.angle = 0
                set_quinta.rotate.angle = 0
                set_sexta.rotate.angle = 0
                set_sabado.rotate.angle = 0
                set_domingo.rotate.angle = 0
            else:
                set_quarta.rotate.angle = 0
                Qua_cor.content.visible = False
        else:
            Qua_cor.content.visible = False
        set_quarta.update()
        SalvarDados()
        page.update()

    # Quinta cortinas
    def Quinta(e):
        if 'Qui' in DiasSelecionados:
            nonlocal Seg_cor_ativo
            nonlocal Ter_cor_ativo
            nonlocal Qua_cor_ativo
            nonlocal Qui_cor_ativo
            nonlocal Sex_cor_ativo
            nonlocal Sab_cor_ativo
            nonlocal Dom_cor_ativo
            Qui_cor_ativo = not Qui_cor_ativo
            if Qui_cor_ativo:
                Qui_cor.content.visible = True
                set_quinta.rotate.angle = 1.5
                Seg_cor.content.visible = False  # Desativando o content dos outros dias
                Ter_cor.content.visible = False
                Qua_cor.content.visible = False
                Dom_cor.content.visible = False
                Sex_cor.content.visible = False
                Sab_cor.content.visible = False
                Seg_cor_ativo = False  # Desativando a Flag de content ativo dos outros dias
                Ter_cor_ativo = False
                Qua_cor_ativo = False
                Sex_cor_ativo = False
                Sab_cor_ativo = False
                Dom_cor_ativo = False
                set_terca.rotate.angle = 0  # Voltando as outras setas para a posição normal
                set_quarta.rotate.angle = 0
                set_segunda.rotate.angle = 0
                set_sexta.rotate.angle = 0
                set_sabado.rotate.angle = 0
                set_domingo.rotate.angle = 0
            else:
                set_quinta.rotate.angle = 0
                Qui_cor.content.visible = False
        else:
            Qui_cor.content.visible = False
        set_quinta.update()
        SalvarDados()
        page.update()

    # Sexta cortinas
    def Sexta(e):
        if 'Sex' in DiasSelecionados:
            nonlocal Seg_cor_ativo
            nonlocal Ter_cor_ativo
            nonlocal Qua_cor_ativo
            nonlocal Qui_cor_ativo
            nonlocal Sex_cor_ativo
            nonlocal Sab_cor_ativo
            nonlocal Dom_cor_ativo
            Sex_cor_ativo = not Sex_cor_ativo
            if Sex_cor_ativo:
                Sex_cor.content.visible = True
                set_sexta.rotate.angle = 1.5
                Seg_cor.content.visible = False  # Desativando o content dos outros dias
                Ter_cor.content.visible = False
                Qua_cor.content.visible = False
                Qui_cor.content.visible = False
                Dom_cor.content.visible = False
                Sab_cor.content.visible = False
                Seg_cor_ativo = False  # Desativando a Flag de content ativo dos outros dias
                Ter_cor_ativo = False
                Qua_cor_ativo = False
                Qui_cor_ativo = False
                Sab_cor_ativo = False
                Dom_cor_ativo = False
                set_terca.rotate.angle = 0  # Voltando as outras setas para a posição normal
                set_quarta.rotate.angle = 0
                set_quinta.rotate.angle = 0
                set_segunda.rotate.angle = 0
                set_sabado.rotate.angle = 0
                set_domingo.rotate.angle = 0
            else:
                set_sexta.rotate.angle = 0
                Sex_cor.content.visible = False
        else:
            Sex_cor.content.visible = False
        set_sexta.update()
        SalvarDados()
        page.update()

    # Sabado cortinas
    def Sabado(e):
        if 'Sab' in DiasSelecionados:
            nonlocal Seg_cor_ativo
            nonlocal Ter_cor_ativo
            nonlocal Qua_cor_ativo
            nonlocal Qui_cor_ativo
            nonlocal Sex_cor_ativo
            nonlocal Sab_cor_ativo
            nonlocal Dom_cor_ativo
            Sab_cor_ativo = not Sab_cor_ativo
            if Sab_cor_ativo:
                Sab_cor.content.visible = True
                set_sabado.rotate.angle = 1.5
                Seg_cor.content.visible = False  # Desativando o content dos outros dias
                Ter_cor.content.visible = False
                Qua_cor.content.visible = False
                Qui_cor.content.visible = False
                Sex_cor.content.visible = False
                Dom_cor.content.visible = False
                Seg_cor_ativo = False  # Desativando a Flag de content ativo dos outros dias
                Ter_cor_ativo = False
                Qua_cor_ativo = False
                Qui_cor_ativo = False
                Sex_cor_ativo = False
                Dom_cor_ativo = False
                set_terca.rotate.angle = 0  # Voltando as outras setas para a posição normal
                set_quarta.rotate.angle = 0
                set_quinta.rotate.angle = 0
                set_sexta.rotate.angle = 0
                set_segunda.rotate.angle = 0
                set_domingo.rotate.angle = 0
            else:
                set_sabado.rotate.angle = 0
                Sab_cor.content.visible = False
        else:
            Sab_cor.content.visible = False
        set_sabado.update()
        SalvarDados()
        page.update()

    # Domingo cortinas
    def Domingo(e):
        if 'Dom' in DiasSelecionados:
            nonlocal Seg_cor_ativo
            nonlocal Ter_cor_ativo
            nonlocal Qua_cor_ativo
            nonlocal Qui_cor_ativo
            nonlocal Sex_cor_ativo
            nonlocal Sab_cor_ativo
            nonlocal Dom_cor_ativo
            Dom_cor_ativo = not Dom_cor_ativo
            if Dom_cor_ativo:
                Dom_cor.content.visible = True
                set_domingo.rotate.angle = 1.5
                Seg_cor.content.visible = False  # Desativando o content dos outros dias
                Ter_cor.content.visible = False
                Qua_cor.content.visible = False
                Qui_cor.content.visible = False
                Sex_cor.content.visible = False
                Sab_cor.content.visible = False
                Seg_cor_ativo = False  # Desativando a Flag de content ativo dos outros dias
                Ter_cor_ativo = False
                Qua_cor_ativo = False
                Qui_cor_ativo = False
                Sex_cor_ativo = False
                Sab_cor_ativo = False
                set_terca.rotate.angle = 0  # Voltando as outras setas para a posição normal
                set_quarta.rotate.angle = 0
                set_quinta.rotate.angle = 0
                set_sexta.rotate.angle = 0
                set_sabado.rotate.angle = 0
                set_segunda.rotate.angle = 0
            else:
                set_domingo.rotate.angle = 0
                Dom_cor.content.visible = False
        else:
            Dom_cor.content.visible = False
        set_domingo.update()
        SalvarDados()
        page.update()

    def MudarMostradores():
        nonlocal Cortina_ativa

        if Cortina_ativa:
            Mostrador2.name = ft.icons.RADIO_BUTTON_ON
            Mostrador1.name = ft.icons.RADIO_BUTTON_OFF
        else:
            Mostrador2.name = ft.icons.RADIO_BUTTON_OFF
            Mostrador1.name = ft.icons.RADIO_BUTTON_ON
        page.update()

    def MudarCor():
        nonlocal DiasSelecionados
        nonlocal DiasSelecionadosAli

        if 'Seg' in DiasSelecionados:
            Segunda_cor_icon.bgcolor = verde1
            Segunda_cor_icon.content.color = branco2
        else:
            Segunda_cor_icon.bgcolor = branco2
            Segunda_cor_icon.content.color = verde1
        if 'Ter' in DiasSelecionados:
            Terca_cor_icon.bgcolor = verde1
            Terca_cor_icon.content.color = branco2
        else:
            Terca_cor_icon.bgcolor = branco2
            Terca_cor_icon.content.color = verde1
        if 'Qua' in DiasSelecionados:
            Quarta_cor_icon.bgcolor = verde1
            Quarta_cor_icon.content.color = branco2
        else:
            Quarta_cor_icon.bgcolor = branco2
            Quarta_cor_icon.content.color = verde1
        if 'Qui' in DiasSelecionados:
            Quinta_cor_icon.bgcolor = verde1
            Quinta_cor_icon.content.color = branco2
        else:
            Quinta_cor_icon.bgcolor = branco2
            Quinta_cor_icon.content.color = verde1
        if 'Sex' in DiasSelecionados:
            Sexta_cor_icon.bgcolor = verde1
            Sexta_cor_icon.content.color = branco2
        else:
            Sexta_cor_icon.bgcolor = branco2
            Sexta_cor_icon.content.color = verde1
        if 'Sab' in DiasSelecionados:
            Sabado_cor_icon.bgcolor = verde1
            Sabado_cor_icon.content.color = branco2
        else:
            Sabado_cor_icon.bgcolor = branco2
            Sabado_cor_icon.content.color = verde1
        if 'Dom' in DiasSelecionados:
            Domingo_cor_icon.bgcolor = verde1
            Domingo_cor_icon.content.color = branco2
        else:
            Domingo_cor_icon.bgcolor = branco2
            Domingo_cor_icon.content.color = verde1

        # Alimentação

        if 'Seg' in DiasSelecionadosAli:
            Segunda_ali_icon.bgcolor = verde1
            Segunda_ali_icon.content.color = branco2
        else:
            Segunda_ali_icon.bgcolor = branco2
            Segunda_ali_icon.content.color = verde1
        if 'Ter' in DiasSelecionadosAli:
            Terca_ali_icon.bgcolor = verde1
            Terca_ali_icon.content.color = branco2
        else:
            Terca_ali_icon.bgcolor = branco2
            Terca_ali_icon.content.color = verde1
        if 'Qua' in DiasSelecionadosAli:
            Quarta_ali_icon.bgcolor = verde1
            Quarta_ali_icon.content.color = branco2
        else:
            Quarta_ali_icon.bgcolor = branco2
            Quarta_ali_icon.content.color = verde1
        if 'Qui' in DiasSelecionadosAli:
            Quinta_ali_icon.bgcolor = verde1
            Quinta_ali_icon.content.color = branco2
        else:
            Quinta_ali_icon.bgcolor = branco2
            Quinta_ali_icon.content.color = verde1
        if 'Sex' in DiasSelecionadosAli:
            Sexta_ali_icon.bgcolor = verde1
            Sexta_ali_icon.content.color = branco2
        else:
            Sexta_ali_icon.bgcolor = branco2
            Sexta_ali_icon.content.color = verde1
        if 'Sab' in DiasSelecionadosAli:
            Sabado_ali_icon.bgcolor = verde1
            Sabado_ali_icon.content.color = branco2
        else:
            Sabado_ali_icon.bgcolor = branco2
            Sabado_ali_icon.content.color = verde1
        if 'Dom' in DiasSelecionadosAli:
            Domingo_ali_icon.bgcolor = verde1
            Domingo_ali_icon.content.color = branco2
        else:
            Domingo_ali_icon.bgcolor = branco2
            Domingo_ali_icon.content.color = verde1
        page.update()
        SalvarDados()

    # Cortinas
    def DiaSelecionado_cor(e):
        nonlocal state_dias
        nonlocal DiasSelecionados
        print(f'funcao chamada {DiasSelecionados}')
        if e:
            for p, d in enumerate(DiasDaSemana):
                if e.control.content.value == d:
                    state_dias[d] = not state_dias[d]
                    print(state_dias)
            for k, v in state_dias.items():
                if v and k not in DiasSelecionados:
                    DiasSelecionados.append(k)
                elif k in DiasSelecionados and not v:
                    DiasSelecionados.remove(k)

            if 'Seg' not in DiasSelecionados:
                set_segunda.rotate.angle = 0  # Voltando as outras setas para a posição normal
                Seg_cor.content.visible = False
            if 'Ter' not in DiasSelecionados:
                set_terca.rotate.angle = 0  # Voltando as outras setas para a posição normal
                Ter_cor.content.visible = False
            if 'Qua' not in DiasSelecionados:
                set_quarta.rotate.angle = 0  # Voltando as outras setas para a posição normal
                Qua_cor.content.visible = False
            if 'Qui' not in DiasSelecionados:
                set_quinta.rotate.angle = 0  # Voltando as outras setas para a posição normal
                Qui_cor.content.visible = False
            if 'Sex' not in DiasSelecionados:
                set_sexta.rotate.angle = 0  # Voltando as outras setas para a posição normal
                Sex_cor.content.visible = False
            if 'Sab' not in DiasSelecionados:
                set_sabado.rotate.angle = 0  # Voltando as outras setas para a posição normal
                Sab_cor.content.visible = False
            if 'Dom' not in DiasSelecionados:
                set_domingo.rotate.angle = 0  # Voltando as outras setas para a posição normal
                Dom_cor.content.visible = False
            MudarCor()
            page.update()
            print(DiasSelecionados)
            Salvar_dados_no_firebase(__DiasSelecionadosCor=True)

    # ALIMENTAÇÃO
    def Alimentar(e):
        print("alimentando")
        nonlocal alimentar
        if not alimentar:
            pb.visible = True
            alimentar = True
            pb.update()
            for contador in range(0, 101):
                pb.value = contador * 0.01
                time.sleep(0.1)  # A barra estará completa em 10 segundos
                Seg_ali.content.visible = False
                Ter_ali.content.visible = False
                Qua_ali.content.visible = False
                Qui_ali.content.visible = False
                Sex_ali.content.visible = False
                Sab_ali.content.visible = False
                Dom_ali.content.visible = False
                page.update()
            pb.value = 0
            alimentar = False
            pb.visible = False
            localtime = time.localtime()
            dia_da_semana = DiasDaSemana[localtime.tm_wday]
            if localtime.tm_min + 1 == 60:
                minuto = '00'
                hora = str(localtime.tm_hour + 1)
            elif len(str(localtime.tm_min + 1)) == 1:
                minuto = '0' + str(localtime.tm_min + 1)
            else:
                minuto = str(localtime.tm_min + 1)
            if len(str(localtime.tm_hour)) == 1:
                hora = '0' + str(localtime.tm_hour)
            else:
                hora = str(localtime.tm_hour)
            horario_agora = hora + ":" + minuto
            horarios_alimentar_semana[dia_da_semana].append(horario_agora)
            Salvar_dados_no_firebase(__HorariosAlimentar=True)
            pb.update()
            del horarios_alimentar_semana[dia_da_semana][-1]
            print(horarios_alimentar_semana)
        SalvarDados()

        page.update()

    def FoodChange(e):
        nonlocal VelocidadePWM
        nonlocal Comida
        print(e.control.value)
        if e.control.value == 'Pequeno':
            Comida = 'Pequeno'
            VelocidadePWM = 0.05
        if e.control.value == 'medio':
            Comida = 'medio'
            VelocidadePWM = 0.075
        if e.control.value == 'Grande':
            Comida = 'Grande'
            VelocidadePWM = 0.1
        page.update()
        SalvarDados()
        Salvar_dados_no_firebase(__VelocidadePWM=True)

    def RestaurarComida(e):
        nonlocal Comida
        print('Restaurando comida')
        Mostradores.value = Comida
        page.update()

    def ExemplosPequeno(e):
        page.controls.clear()  # Limpa o conteúdo atual
        page.controls.append(alimentos_Pequeno)
        page.update()

    def ExemplosMedio(e):
        page.controls.clear()  # Limpa o conteúdo atual
        page.controls.append(alimentos_medio)
        page.update()

    def ExemplosGrande(e):
        page.controls.clear()  # Limpa o conteúdo atual
        page.controls.append(alimentos_Grande)
        page.update()

    def FecharExemplos(e):
        page.controls.clear()  # Limpa o conteúdo atual
        page.controls.append(alimentacao_content)
        page.update()

    def DiaSelecionado_ali(e):
        nonlocal state_dias_ali
        nonlocal DiasSelecionadosAli
        nonlocal DiasDaSemana

        for p, d in enumerate(DiasDaSemana):
            if e.control.content.value == d:
                state_dias_ali[d] = not state_dias_ali[d]
                print(state_dias_ali)
        for k, v in state_dias_ali.items():
            if v and k not in DiasSelecionadosAli:
                DiasSelecionadosAli.append(k)
            elif k in DiasSelecionadosAli and not v:
                DiasSelecionadosAli.remove(k)

        if 'Seg' not in DiasSelecionadosAli:
            set_segunda2.rotate.angle = 0  # Voltando as outras setas para a posição normal
            Seg_ali.content.visible = False
        if 'Ter' not in DiasSelecionadosAli:
            set_terca2.rotate.angle = 0  # Voltando as outras setas para a posição normal
            Ter_ali.content.visible = False
        if 'Qua' not in DiasSelecionadosAli:
            set_quarta2.rotate.angle = 0  # Voltando as outras setas para a posição normal
            Qua_ali.content.visible = False
        if 'Qui' not in DiasSelecionadosAli:
            set_quinta2.rotate.angle = 0  # Voltando as outras setas para a posição normal
            Qui_ali.content.visible = False
        if 'Sex' not in DiasSelecionadosAli:
            set_sexta2.rotate.angle = 0  # Voltando as outras setas para a posição normal
            Sex_ali.content.visible = False
        if 'Sab' not in DiasSelecionadosAli:
            set_sabado2.rotate.angle = 0  # Voltando as outras setas para a posição normal
            Sab_ali.content.visible = False
        if 'Dom' not in DiasSelecionadosAli:
            set_domingo2.rotate.angle = 0  # Voltando as outras setas para a posição normal
            Dom_ali.content.visible = False
        MudarCor()
        SalvarDados()
        Salvar_dados_no_firebase(__DiasSelecionadosAli=True)
        page.update()
        print(DiasSelecionadosAli)

    def RemoveAli(e):
        nonlocal i2
        nonlocal lista_botoes_seg2
        nonlocal lista_botoes_ter2
        nonlocal lista_botoes_qua2
        nonlocal lista_botoes_qui2
        nonlocal lista_botoes_sex2
        nonlocal lista_botoes_sab2
        nonlocal lista_botoes_dom2
        nonlocal horarios_alimentar_semana

        print(e.control.content.value)
        print(Seg_ali_ativo)
        if Seg_ali_ativo:
            for p, c in enumerate(lista_botoes_seg2):
                if c == int(e.control.content.value):
                    del list_horario_seg2.controls[p]
                    del lista_botoes_seg2[p]
                    del horarios_alimentar_semana['Seg'][p]
        if Ter_ali_ativo:
            for p, c in enumerate(lista_botoes_ter2):
                if c == int(e.control.content.value):
                    del list_horario_ter2.controls[p]
                    del lista_botoes_ter2[p]
                    del horarios_alimentar_semana['Ter'][p]
        if Qua_ali_ativo:
            for p, c in enumerate(lista_botoes_qua2):
                if c == int(e.control.content.value):
                    del list_horario_qua2.controls[p]
                    del lista_botoes_qua2[p]
                    del horarios_alimentar_semana['Qua'][p]
        if Qui_ali_ativo:
            for p, c in enumerate(lista_botoes_qui2):
                if c == int(e.control.content.value):
                    del list_horario_qui2.controls[p]
                    del lista_botoes_qui2[p]
                    del horarios_alimentar_semana['Qui'][p]
        if Sex_ali_ativo:
            for p, c in enumerate(lista_botoes_sex2):
                if c == int(e.control.content.value):
                    del list_horario_sex2.controls[p]
                    del lista_botoes_sex2[p]
                    del horarios_alimentar_semana['Sex'][p]
        if Sab_ali_ativo:
            for p, c in enumerate(lista_botoes_sab2):
                if c == int(e.control.content.value):
                    del list_horario_sab2.controls[p]
                    del lista_botoes_sab2[p]
                    del horarios_alimentar_semana['Sab'][p]
        if Dom_ali_ativo:
            for p, c in enumerate(lista_botoes_dom2):
                if c == int(e.control.content.value):
                    del list_horario_dom2.controls[p]
                    del lista_botoes_dom2[p]
                    del horarios_alimentar_semana['Dom'][p]
        print(horarios_alimentar_semana)
        SalvarDados()
        page.update()
        Salvar_dados_no_firebase(__HorariosAlimentar=True)
        pass

    def RegistroAli(e):
        nonlocal horario_alimentar
        nonlocal i2
        Text_field_alimentar = ''
        digit_1 = ''
        digit_2 = ''

        if Seg_ali_ativo:
            Text_field_alimentar = Text_field_alimentar_seg.value
        if Ter_ali_ativo:
            Text_field_alimentar = Text_field_alimentar_ter.value
        if Qua_ali_ativo:
            Text_field_alimentar = Text_field_alimentar_qua.value
        if Qui_ali_ativo:
            Text_field_alimentar = Text_field_alimentar_qui.value
        if Sex_ali_ativo:
            Text_field_alimentar = Text_field_alimentar_sex.value
        if Sab_ali_ativo:
            Text_field_alimentar = Text_field_alimentar_sab.value
        if Dom_ali_ativo:
            Text_field_alimentar = Text_field_alimentar_dom.value

        erro = False
        # TRATAMENTO DO ERRO INPUT MAIOR QUE 5 CARACTERES:

        for numero in Text_field_alimentar:
            if numero.isalpha():
                erro = True

        if not erro:
            if not len(Text_field_alimentar) > 5:
                digit_1 = Text_field_alimentar[0] + Text_field_alimentar[1]
                if digit_1.find(':') != -1:
                    digit_1 = '0' + digit_1
                    digit_1 = digit_1.replace(':', '')
                    try:
                        digit_2 = Text_field_alimentar[2] + Text_field_alimentar[3]
                    except IndexError:
                        digit_2 = Text_field_alimentar[2] + '0'
                else:
                    try:
                        digit_2 = Text_field_alimentar[3] + Text_field_alimentar[4]
                    except IndexError:
                        digit_2 = Text_field_alimentar[3] + '0'

                    # TRATAMENTO DO ERRO HORARIOS MAIORES QUE 23H E 59MIN
                    if int(digit_1) > 23 or int(digit_2) > 59:
                        erro = True
                Text_field_alimentar = digit_1 + ':' + digit_2
            else:
                erro = True

            # INPUT
            # TRATAMENTO DO ERRO INPUT VAZIO E DO ERRO CARACTERES NO LUGAR DE NUMEROS:
        if not Text_field_alimentar == '' and not erro:
            for p, c in enumerate(Text_field_alimentar):
                if not c.isdecimal():
                    if not (c == ':' and p == 2) or c == '':
                        erro = True
                        break
        else:
            erro = True

        if erro:
            if Seg_ali_ativo:
                Text_field_alimentar_seg.value = 'Erro.'
                page.update()
            if Ter_ali_ativo:
                Text_field_alimentar_ter.value = 'Erro.'
                page.update()
            if Qua_ali_ativo:
                Text_field_alimentar_qua.value = 'Erro.'
                page.update()
            if Qui_ali_ativo:
                Text_field_alimentar_qui.value = 'Erro.'
                page.update()
            if Sex_ali_ativo:
                Text_field_alimentar_sex.value = 'Erro.'
                page.update()
            if Sab_ali_ativo:
                Text_field_alimentar_sab.value = 'Erro.'
                page.update()
            if Dom_ali_ativo:
                Text_field_alimentar_dom.value = 'Erro.'
                page.update()
        if not erro:
            horario_alimentar = Text_field_alimentar
            print(horario_alimentar)
            i2 += 1
            if Seg_ali_ativo:
                horarios_alimentar_semana['Seg'].append(horario_alimentar)
                lista_botoes_seg2.append(i2)
                list_horario_seg2.controls.append(
                    ft.Container(bgcolor=verde1, height=60, border_radius=10, offset=ft.transform.Offset(-0.05, 0),
                                 content=ft.Row(width=100,
                                                controls=[
                                                    ft.Text(
                                                        offset=ft.transform.Offset(0.04, 0),
                                                        value=f'O alimentador ativará as {horario_alimentar}H.',
                                                        color=branco2),
                                                    ft.IconButton(icon=ft.icons.REMOVE,
                                                                  offset=ft.transform.Offset(1, 0), on_click=RemoveAli,
                                                                  icon_color=branco2, content=ft.Text(value=f'{i2}'))
                                                ], )))
                Text_field_alimentar_seg.value = ''
                Text_field_alimentar_seg.update()
            if Ter_ali_ativo:
                horarios_alimentar_semana['Ter'].append(horario_alimentar)
                lista_botoes_ter2.append(i2)
                list_horario_ter2.controls.append(
                    ft.Container(bgcolor=verde1, height=60, border_radius=10, offset=ft.transform.Offset(-0.05, 0),
                                 content=ft.Row(width=100,
                                                controls=[
                                                    ft.Text(
                                                        offset=ft.transform.Offset(0.04, 0),
                                                        value=f'O alimentador ativará as {horario_alimentar}H.',
                                                        color=branco2),
                                                    ft.IconButton(icon=ft.icons.REMOVE,
                                                                  offset=ft.transform.Offset(1, 0), on_click=RemoveAli,
                                                                  icon_color=branco2, content=ft.Text(value=f'{i2}'))
                                                ], )))
                Text_field_alimentar_ter.value = ''
                Text_field_alimentar_ter.update()
            if Qua_ali_ativo:
                horarios_alimentar_semana['Qua'].append(horario_alimentar)
                lista_botoes_qua2.append(i2)
                list_horario_qua2.controls.append(
                    ft.Container(bgcolor=verde1, height=60, border_radius=10, offset=ft.transform.Offset(-0.05, 0),
                                 content=ft.Row(width=100,
                                                controls=[
                                                    ft.Text(
                                                        offset=ft.transform.Offset(0.04, 0),
                                                        value=f'O alimentador ativará as {horario_alimentar}H.',
                                                        color=branco2),
                                                    ft.IconButton(icon=ft.icons.REMOVE,
                                                                  offset=ft.transform.Offset(1, 0), on_click=RemoveAli,
                                                                  icon_color=branco2, content=ft.Text(value=f'{i2}'))
                                                ], )))
                Text_field_alimentar_qua.value = ''
                Text_field_alimentar_qua.update()
            if Qui_ali_ativo:
                horarios_alimentar_semana['Qui'].append(horario_alimentar)
                lista_botoes_qui2.append(i2)
                list_horario_qui2.controls.append(
                    ft.Container(bgcolor=verde1, height=60, border_radius=10, offset=ft.transform.Offset(-0.05, 0),
                                 content=ft.Row(width=100,
                                                controls=[
                                                    ft.Text(
                                                        offset=ft.transform.Offset(0.04, 0),
                                                        value=f'O alimentador ativará as {horario_alimentar}H.',
                                                        color=branco2),
                                                    ft.IconButton(icon=ft.icons.REMOVE,
                                                                  offset=ft.transform.Offset(1, 0), on_click=RemoveAli,
                                                                  icon_color=branco2, content=ft.Text(value=f'{i2}'))
                                                ], )))
                Text_field_alimentar_qui.value = ''
                Text_field_alimentar_qui.update()
            if Sex_ali_ativo:
                horarios_alimentar_semana['Sex'].append(horario_alimentar)
                lista_botoes_sex2.append(i2)
                list_horario_sex2.controls.append(
                    ft.Container(bgcolor=verde1, height=60, border_radius=10, offset=ft.transform.Offset(-0.05, 0),
                                 content=ft.Row(width=100,
                                                controls=[
                                                    ft.Text(
                                                        offset=ft.transform.Offset(0.04, 0),
                                                        value=f'O alimentador ativará as {horario_alimentar}H.',
                                                        color=branco2),
                                                    ft.IconButton(icon=ft.icons.REMOVE,
                                                                  offset=ft.transform.Offset(1, 0), on_click=RemoveAli,
                                                                  icon_color=branco2, content=ft.Text(value=f'{i2}'))
                                                ], )))
                Text_field_alimentar_sex.value = ''
                Text_field_alimentar_sex.update()
            if Sab_ali_ativo:
                horarios_alimentar_semana['Sab'].append(horario_alimentar)
                lista_botoes_sab2.append(i2)
                list_horario_sab2.controls.append(
                    ft.Container(bgcolor=verde1, height=60, border_radius=10, offset=ft.transform.Offset(-0.05, 0),
                                 content=ft.Row(width=100,
                                                controls=[
                                                    ft.Text(
                                                        offset=ft.transform.Offset(0.04, 0),
                                                        value=f'O alimentador ativará as {horario_alimentar}H.',
                                                        color=branco2),
                                                    ft.IconButton(icon=ft.icons.REMOVE,
                                                                  offset=ft.transform.Offset(1, 0), on_click=RemoveAli,
                                                                  icon_color=branco2, content=ft.Text(value=f'{i2}'))
                                                ], )))
                Text_field_alimentar_sab.value = ''
                Text_field_alimentar_sab.update()
            if Dom_ali_ativo:
                horarios_alimentar_semana['Dom'].append(horario_alimentar)
                lista_botoes_dom2.append(i2)
                list_horario_dom2.controls.append(
                    ft.Container(bgcolor=verde1, height=60, border_radius=10, offset=ft.transform.Offset(-0.05, 0),
                                 content=ft.Row(width=100,
                                                controls=[
                                                    ft.Text(
                                                        offset=ft.transform.Offset(0.04, 0),
                                                        value=f"O alimentador ativará as {horario_alimentar}H.",
                                                        color=branco2),
                                                    ft.IconButton(icon=ft.icons.REMOVE,
                                                                  offset=ft.transform.Offset(1, 0), on_click=RemoveAli,
                                                                  icon_color=branco2, content=ft.Text(value=f'{i2}'))
                                                ], )))
                Text_field_alimentar_dom.value = ''
                Text_field_alimentar_dom.update()
        print(horarios_alimentar_semana)
        SalvarDados()
        page.update()
        Salvar_dados_no_firebase(__HorariosAlimentar=True)

    def RestaurarHorarioAlimentar(e=False):
        print('Função chamada')
        nonlocal horarios_alimentar_semana
        nonlocal lista_botoes_seg2
        nonlocal lista_botoes_ter2
        nonlocal lista_botoes_qua2
        nonlocal lista_botoes_qui2
        nonlocal lista_botoes_sex2
        nonlocal lista_botoes_sab2
        nonlocal lista_botoes_dom2
        nonlocal count_alimentar
        # Segunda
        if not e or count_alimentar == 0:
            if isinstance(horarios_alimentar_semana['Seg'], list):
                for p, c in enumerate(lista_botoes_seg2):
                    list_horario_seg2.controls.append(
                        ft.Container(bgcolor=verde1, height=60, border_radius=10, offset=ft.transform.Offset(-0.05, 0),
                                     content=ft.Row(width=100,
                                                    controls=[
                                                        ft.Text(
                                                            offset=ft.transform.Offset(0.04, 0),
                                                            value=f"O alimentador ativará as {horarios_alimentar_semana['Seg'][p]}H.",
                                                            color=branco2),
                                                        ft.IconButton(icon=ft.icons.REMOVE,
                                                                      offset=ft.transform.Offset(1, 0),
                                                                      on_click=RemoveAli, icon_color=branco2,
                                                                      content=ft.Text(value=f'{c}'))
                                                    ], )))
                list_horario_seg2.update()
            # Terca
            if isinstance(horarios_alimentar_semana['Ter'], list):
                for p, c in enumerate(lista_botoes_ter2):
                    list_horario_ter2.controls.append(
                        ft.Container(bgcolor=verde1, height=60, border_radius=10, offset=ft.transform.Offset(-0.05, 0),
                                     content=ft.Row(width=100,
                                                    controls=[
                                                        ft.Text(
                                                            offset=ft.transform.Offset(0.04, 0),
                                                            value=f"O alimentador Ativará as {horarios_alimentar_semana['Ter'][p]}H.",
                                                            color=branco2),
                                                        ft.IconButton(icon=ft.icons.REMOVE,
                                                                      offset=ft.transform.Offset(1, 0),
                                                                      on_click=RemoveAli, icon_color=branco2,
                                                                      content=ft.Text(value=f'{c}'))
                                                    ], )))
                list_horario_ter2.update()
            # Quarta
            if isinstance(horarios_alimentar_semana['Qua'], list):
                for p, c in enumerate(lista_botoes_qua2):
                    list_horario_qua2.controls.append(
                        ft.Container(bgcolor=verde1, height=60, border_radius=10, offset=ft.transform.Offset(-0.05, 0),
                                     content=ft.Row(width=100,
                                                    controls=[
                                                        ft.Text(
                                                            offset=ft.transform.Offset(0.04, 0),
                                                            value=f"O alimentador Ativará as {horarios_alimentar_semana['Qua'][p]}H.",
                                                            color=branco2),
                                                        ft.IconButton(icon=ft.icons.REMOVE,
                                                                      offset=ft.transform.Offset(1, 0),
                                                                      on_click=RemoveAli, icon_color=branco2,
                                                                      content=ft.Text(value=f'{c}'))
                                                    ], )))
                list_horario_qua2.update()
            # Quinta
            if isinstance(horarios_alimentar_semana['Qui'], list):
                for p, c in enumerate(lista_botoes_qui2):
                    list_horario_qui2.controls.append(
                        ft.Container(bgcolor=verde1, height=60, border_radius=10, offset=ft.transform.Offset(-0.05, 0),
                                     content=ft.Row(width=100,
                                                    controls=[
                                                        ft.Text(
                                                            offset=ft.transform.Offset(0.04, 0),
                                                            value=f"O alimentador Ativará as {horarios_alimentar_semana['Qui'][p]}H.",
                                                            color=branco2),
                                                        ft.IconButton(icon=ft.icons.REMOVE,
                                                                      offset=ft.transform.Offset(1, 0),
                                                                      on_click=RemoveAli, icon_color=branco2,
                                                                      content=ft.Text(value=f'{c}'))
                                                    ], )))
                list_horario_qui2.update()
            # Sexta
            if isinstance(horarios_alimentar_semana['Sex'], list):
                for p, c in enumerate(lista_botoes_sex2):
                    list_horario_sex2.controls.append(
                        ft.Container(bgcolor=verde1, height=60, border_radius=10, offset=ft.transform.Offset(-0.05, 0),
                                     content=ft.Row(width=100,
                                                    controls=[
                                                        ft.Text(
                                                            offset=ft.transform.Offset(0.04, 0),
                                                            value=f"O alimentador Ativará as {horarios_alimentar_semana['Sex'][p]}H.",
                                                            color=branco2),
                                                        ft.IconButton(icon=ft.icons.REMOVE,
                                                                      offset=ft.transform.Offset(1, 0),
                                                                      on_click=RemoveAli, icon_color=branco2,
                                                                      content=ft.Text(value=f'{c}'))
                                                    ], )))
                list_horario_sex2.update()
            # Sabado
            if isinstance(horarios_alimentar_semana['Sab'], list):
                for p, c in enumerate(lista_botoes_sab2):
                    list_horario_sab2.controls.append(
                        ft.Container(bgcolor=verde1, height=60, border_radius=10, offset=ft.transform.Offset(-0.05, 0),
                                     content=ft.Row(width=100,
                                                    controls=[
                                                        ft.Text(
                                                            offset=ft.transform.Offset(0.04, 0),
                                                            value=f"O alimentador Ativará as {horarios_alimentar_semana['Sab'][p]}H.",
                                                            color=branco2),
                                                        ft.IconButton(icon=ft.icons.REMOVE,
                                                                      offset=ft.transform.Offset(1, 0),
                                                                      on_click=RemoveAli, icon_color=branco2,
                                                                      content=ft.Text(value=f'{c}'))
                                                    ], )))
                list_horario_sab2.update()
            # Domingo
            if isinstance(horarios_alimentar_semana['Dom'], list):
                for p, c in enumerate(lista_botoes_dom2):
                    list_horario_dom2.controls.append(
                        ft.Container(bgcolor=verde1, height=60, border_radius=10, offset=ft.transform.Offset(-0.05, 0),
                                     content=ft.Row(width=100,
                                                    controls=[
                                                        ft.Text(
                                                            offset=ft.transform.Offset(0.04, 0),
                                                            value=f"O alimentador Ativará as {horarios_alimentar_semana['Dom'][p]}H.",
                                                            color=branco2),
                                                        ft.IconButton(icon=ft.icons.REMOVE,
                                                                      offset=ft.transform.Offset(1, 0),
                                                                      on_click=RemoveAli, icon_color=branco2,
                                                                      content=ft.Text(value=f'{c}'))
                                                    ], )))
                list_horario_dom2.update()
            count_alimentar = 1

    # Segunda ALIMENTAÇÃO
    def Segunda2(e):
        if 'Seg' in DiasSelecionadosAli:
            nonlocal Seg_ali_ativo
            nonlocal Ter_ali_ativo
            nonlocal Qua_ali_ativo
            nonlocal Qui_ali_ativo
            nonlocal Sex_ali_ativo
            nonlocal Sab_ali_ativo
            nonlocal Dom_ali_ativo
            Seg_ali_ativo = not Seg_ali_ativo
            if Seg_ali_ativo:
                Seg_ali.content.visible = True
                set_segunda2.rotate.angle = 1.5
                Dom_ali.content.visible = False  # Desativando o content dos outros dias
                Ter_ali.content.visible = False
                Qua_ali.content.visible = False
                Qui_ali.content.visible = False
                Sex_ali.content.visible = False
                Sab_ali.content.visible = False
                Ter_ali_ativo = False  # Desativando a Flag de content ativo dos outros dias
                Qua_ali_ativo = False
                Qui_ali_ativo = False
                Sex_ali_ativo = False
                Sab_ali_ativo = False
                Dom_ali_ativo = False
                set_terca2.rotate.angle = 0  # Voltando as outras setas para a posição normal
                set_quarta2.rotate.angle = 0
                set_quinta2.rotate.angle = 0
                set_sexta2.rotate.angle = 0
                set_sabado2.rotate.angle = 0
                set_domingo2.rotate.angle = 0
            else:
                set_segunda2.rotate.angle = 0
                Seg_ali.content.visible = False
        else:
            Seg_ali.content.visible = False
        set_segunda2.update()
        SalvarDados()
        page.update()

    # Terça Alimentação
    def Terca2(e):
        if 'Ter' in DiasSelecionadosAli:
            nonlocal Seg_ali_ativo
            nonlocal Ter_ali_ativo
            nonlocal Qua_ali_ativo
            nonlocal Qui_ali_ativo
            nonlocal Sex_ali_ativo
            nonlocal Sab_ali_ativo
            nonlocal Dom_ali_ativo
            Ter_ali_ativo = not Ter_ali_ativo
            if Ter_ali_ativo:
                Ter_ali.content.visible = True
                set_terca2.rotate.angle = 1.5
                Seg_ali.content.visible = False  # Desativando o content dos outros dias
                Dom_ali.content.visible = False
                Qua_ali.content.visible = False
                Qui_ali.content.visible = False
                Sex_ali.content.visible = False
                Sab_ali.content.visible = False
                Seg_ali_ativo = False  # Desativando a Flag de content ativo dos outros dias
                Qua_ali_ativo = False
                Qui_ali_ativo = False
                Sex_ali_ativo = False
                Sab_ali_ativo = False
                Dom_ali_ativo = False
                set_segunda2.rotate.angle = 0  # Voltando as outras setas para a posição normal
                set_quarta2.rotate.angle = 0
                set_quinta2.rotate.angle = 0
                set_sexta2.rotate.angle = 0
                set_sabado2.rotate.angle = 0
                set_domingo2.rotate.angle = 0
            else:
                set_terca2.rotate.angle = 0
                Ter_ali.content.visible = False
        else:
            Ter_ali.content.visible = False
        set_terca2.update()
        SalvarDados()
        page.update()

    # Quarta ALimentaçãp
    def Quarta2(e):
        if 'Qua' in DiasSelecionadosAli:
            nonlocal Seg_ali_ativo
            nonlocal Ter_ali_ativo
            nonlocal Qua_ali_ativo
            nonlocal Qui_ali_ativo
            nonlocal Sex_ali_ativo
            nonlocal Sab_ali_ativo
            nonlocal Dom_ali_ativo
            Qua_ali_ativo = not Qua_ali_ativo
            if Qua_ali_ativo:
                Qua_ali.content.visible = True
                set_quarta2.rotate.angle = 1.5
                Seg_ali.content.visible = False  # Desativando o content dos outros dias
                Ter_ali.content.visible = False
                Dom_ali.content.visible = False
                Qui_ali.content.visible = False
                Sex_ali.content.visible = False
                Sab_ali.content.visible = False
                Seg_ali_ativo = False  # Desativando a Flag de content ativo dos outros dias
                Ter_ali_ativo = False
                Qui_ali_ativo = False
                Sex_ali_ativo = False
                Sab_ali_ativo = False
                Dom_ali_ativo = False
                set_terca2.rotate.angle = 0  # Voltando as outras setas para a posição normal
                set_segunda2.rotate.angle = 0
                set_quinta2.rotate.angle = 0
                set_sexta2.rotate.angle = 0
                set_sabado2.rotate.angle = 0
                set_domingo2.rotate.angle = 0
            else:
                set_quarta2.rotate.angle = 0
                Qua_ali.content.visible = False
        else:
            Qua_ali.content.visible = False
        set_quarta2.update()
        SalvarDados()
        page.update()

    # Quinta Alimentação
    def Quinta2(e):
        if 'Qui' in DiasSelecionadosAli:
            nonlocal Seg_ali_ativo
            nonlocal Ter_ali_ativo
            nonlocal Qua_ali_ativo
            nonlocal Qui_ali_ativo
            nonlocal Sex_ali_ativo
            nonlocal Sab_ali_ativo
            nonlocal Dom_ali_ativo
            Qui_ali_ativo = not Qui_ali_ativo
            if Qui_ali_ativo:
                Qui_ali.content.visible = True
                set_quinta2.rotate.angle = 1.5
                Seg_ali.content.visible = False  # Desativando o content dos outros dias
                Ter_ali.content.visible = False
                Qua_ali.content.visible = False
                Dom_ali.content.visible = False
                Sex_ali.content.visible = False
                Sab_ali.content.visible = False
                Seg_ali_ativo = False  # Desativando a Flag de content ativo dos outros dias
                Ter_ali_ativo = False
                Qua_ali_ativo = False
                Sex_ali_ativo = False
                Sab_ali_ativo = False
                Dom_ali_ativo = False
                set_terca2.rotate.angle = 0  # Voltando as outras setas para a posição normal
                set_quarta2.rotate.angle = 0
                set_segunda2.rotate.angle = 0
                set_sexta2.rotate.angle = 0
                set_sabado2.rotate.angle = 0
                set_domingo2.rotate.angle = 0
            else:
                set_quinta2.rotate.angle = 0
                Qui_ali.content.visible = False
        else:
            Qui_ali.content.visible = False
        set_quinta2.update()
        SalvarDados()
        page.update()

    # Sexta alimentação
    def Sexta2(e):
        if 'Sex' in DiasSelecionadosAli:
            nonlocal Seg_ali_ativo
            nonlocal Ter_ali_ativo
            nonlocal Qua_ali_ativo
            nonlocal Qui_ali_ativo
            nonlocal Sex_ali_ativo
            nonlocal Sab_ali_ativo
            nonlocal Dom_ali_ativo
            Sex_ali_ativo = not Sex_ali_ativo
            if Sex_ali_ativo:
                Sex_ali.content.visible = True
                set_sexta2.rotate.angle = 1.5
                Seg_ali.content.visible = False  # Desativando o content dos outros dias
                Ter_ali.content.visible = False
                Qua_ali.content.visible = False
                Qui_ali.content.visible = False
                Dom_ali.content.visible = False
                Sab_ali.content.visible = False
                Seg_ali_ativo = False  # Desativando a Flag de content ativo dos outros dias
                Ter_ali_ativo = False
                Qua_ali_ativo = False
                Qui_ali_ativo = False
                Sab_ali_ativo = False
                Dom_ali_ativo = False
                set_terca2.rotate.angle = 0  # Voltando as outras setas para a posição normal
                set_quarta2.rotate.angle = 0
                set_quinta2.rotate.angle = 0
                set_segunda2.rotate.angle = 0
                set_sabado2.rotate.angle = 0
                set_domingo2.rotate.angle = 0
            else:
                set_sexta2.rotate.angle = 0
                Sex_ali.content.visible = False
        else:
            Sex_ali.content.visible = False
        set_sexta2.update()
        SalvarDados()
        page.update()

    # Sabado Alimentação
    def Sabado2(e):
        if 'Sab' in DiasSelecionadosAli:
            nonlocal Seg_ali_ativo
            nonlocal Ter_ali_ativo
            nonlocal Qua_ali_ativo
            nonlocal Qui_ali_ativo
            nonlocal Sex_ali_ativo
            nonlocal Sab_ali_ativo
            nonlocal Dom_ali_ativo
            Sab_ali_ativo = not Sab_ali_ativo
            if Sab_ali_ativo:
                Sab_ali.content.visible = True
                set_sabado2.rotate.angle = 1.5
                Seg_ali.content.visible = False  # Desativando o content dos outros dias
                Ter_ali.content.visible = False
                Qua_ali.content.visible = False
                Qui_ali.content.visible = False
                Sex_ali.content.visible = False
                Dom_ali.content.visible = False
                Seg_ali_ativo = False  # Desativando a Flag de content ativo dos outros dias
                Ter_ali_ativo = False
                Qua_ali_ativo = False
                Qui_ali_ativo = False
                Sex_ali_ativo = False
                Dom_ali_ativo = False
                set_terca2.rotate.angle = 0  # Voltando as outras setas para a posição normal
                set_quarta2.rotate.angle = 0
                set_quinta2.rotate.angle = 0
                set_sexta2.rotate.angle = 0
                set_segunda2.rotate.angle = 0
                set_domingo2.rotate.angle = 0
            else:
                set_sabado2.rotate.angle = 0
                Sab_ali.content.visible = False
        else:
            Sab_ali.content.visible = False
        set_sabado2.update()
        SalvarDados()
        page.update()

    # Domingo Alimentação
    def Domingo2(e):
        if 'Dom' in DiasSelecionadosAli:
            nonlocal Seg_ali_ativo
            nonlocal Ter_ali_ativo
            nonlocal Qua_ali_ativo
            nonlocal Qui_ali_ativo
            nonlocal Sex_ali_ativo
            nonlocal Sab_ali_ativo
            nonlocal Dom_ali_ativo
            Dom_ali_ativo = not Dom_ali_ativo
            if Dom_ali_ativo:
                Dom_ali.content.visible = True
                set_domingo2.rotate.angle = 1.5
                Seg_ali.content.visible = False  # Desativando o content dos outros dias
                Ter_ali.content.visible = False
                Qua_ali.content.visible = False
                Qui_ali.content.visible = False
                Sex_ali.content.visible = False
                Sab_ali.content.visible = False
                Seg_ali_ativo = False  # Desativando a Flag de content ativo dos outros dias
                Ter_ali_ativo = False
                Qua_ali_ativo = False
                Qui_ali_ativo = False
                Sex_ali_ativo = False
                Sab_ali_ativo = False
                set_terca2.rotate.angle = 0  # Voltando as outras setas para a posição normal
                set_quarta2.rotate.angle = 0
                set_quinta2.rotate.angle = 0
                set_sexta2.rotate.angle = 0
                set_sabado2.rotate.angle = 0
                set_segunda2.rotate.angle = 0
            else:
                set_domingo2.rotate.angle = 0
                Dom_ali.content.visible = False
        else:
            Dom_ali.content.visible = False
        set_domingo2.update()
        SalvarDados()
        page.update()

    # CLIMA
    def adiciona_termometro(e):
        nonlocal Temp_selec
        # Verificando entrada de dados:
        value = Text_field_temperatura.value
        try:
            value = float(value)
            if value <= 27:
                value = float(value)
                Text_field_temperatura.value = ''
                nonlocal aquecer
                aquecer = True
                Temp_selec = value
                ContainerEsquentando.visible = True
                text_termometro.value = f'Esquentando a gaiola até {value:.1f}°C'
                Salvar_dados_no_firebase(__Aquecedor=True)
                SalvarDados()
            else:
                Text_field_temperatura.value = 'Erro'
        except ValueError:
            Text_field_temperatura.value = 'Erro'

        SalvarDados()
        Salvar_dados_no_firebase(__Aquecedor=True)
        page.update()

    def Restaurar_termometro(e):
        if e.control.selected_index == 1:
            nonlocal aquecer
            if aquecer:
                print('restaurando')
                nonlocal Temp_selec
                value = Temp_selec
                text_termometro.value = f'Esquentando a gaiola até {value:.1f}°C'
                ContainerEsquentando.visible = True
                Salvar_dados_no_firebase(__Aquecedor=True)
                SalvarDados()
                page.update()

    def retira_termometro(e):
        nonlocal aquecer
        aquecer = False
        ContainerEsquentando.visible = False
        page.update()
        SalvarDados()
        Salvar_dados_no_firebase(__Aquecedor=True)

    # BANCO DE DADOS
    def SalvarDados():
        nonlocal Comida
        nonlocal aquecer
        print("Salvando dados")
        print(horarios_cortinas_semana)
        conteudo_arquivo = []
        with open('banco_de_dados.txt',
                  'w') as arq:  # APAGANDO OS DADOS DO BANCO DE DADOS PARA A ENTRADA DE NOVOS DADOS
            pass
        arq = open('banco_de_dados.txt', 'w')
        # * A organização do banco de dados se dara da seguinte forma, cada linha do arquivo txt correspondera a uma varial, pode ser ela string, dicionario, booleana, lista etc..
        # * A cada 1 minuto essa função sera chamada para fazer o salvamento dos dados, ao ser chamado os dados antigos serão apagado e os novos serão escritos.
        # * Sempre que o aplicativo for iniciado a primeira coisa que ele ira fazer é ler este arquivo txt e copiar os dados para as variaveis utilizadas durante o funcionamento
        # * do aplictivo.
        # * Assim nao acontecerá do usuario perder todos as rotinas que ele programou toda vez que fechar o aplicativo.
        # *
        # * Agora irei informar a posição das variaveis do aplicativo no banco de dados: !IMPORTANTE!
        # * [line01] = state                         #booleana
        # * [line02] = Seg_cor_ativo                 #booleana
        # * [line03] = Ter_cor_ativo                 #booleana
        # * [line04] = Qua_cor_ativo                 #booleana
        # * [line05] = Qui_cor_ativo                 #booleana
        # * [line06] = Sex_cor_ativo                 #booleana
        # * [line07] = Sab_cor_ativo                 #booleana
        # * [line08] = Dom_cor_ativo                 #booleana
        # * [line09] = state_dias                    #dicionário
        # * [line10] = horario_cortinas_semana       #dicionário
        # * [line11] = DiasSelecionados              #lista
        # * [line12] = lista_botoes_seg              #lista
        # * [line13] = lista_botoes_ter              #lista
        # * [line14] = lista_botoes_qua              #lista
        # * [line15] = lista_botoes_qui              #lista
        # * [line16] = lista_botoes_sex              #lista
        # * [line17] = lista_botoes_sab              #lista
        # * [line18] = lista_botoes_dom              #lista
        # * [line19] = i                             #inteiro
        # * [line20] = Seg_ali_ativo                 #booleana
        # * [line21] = Ter_ali_ativo                 #booleana
        # * [line22] = Qua_ali_ativo                 #booleana
        # * [line23] = Qui_ali_ativo                 #booleana
        # * [line24] = Sex_ali_ativo                 #booleana
        # * [line25] = Sab_ali_ativo                 #booleana
        # * [line26] = Dom_ali_ativo                 #booleana
        # * [line27] = state_dias_ali                #dicionário
        # * [line28] = horarios_alimentar_semana     #dicionário
        # * [line29] = i2                            #inteiro
        # * [line30] = DiasSelecionadosAli           #lista
        # * [line31] = lista_botoes_seg2             #lista
        # * [line32] = lista_botoes_ter2             #lista
        # * [line33] = lista_botoes_qua2             #lista
        # * [line34] = lista_botoes_qui2             #lista
        # * [line35] = lista_botoes_sex2             #lista
        # * [line36] = lista_botoes_sab2             #lista
        # * [line37] = lista_botoes_dom2             #lista
        # * [line38] = VelocidadePWM                 #float
        # * [line39] = Comida_Selecionada            #string
        # * Agora irei escrever as variaveis mencionadas acima no arquivo txt, na mesma ordem da lista a cima, usando a bliblioteca 'json', essa biblioteca permite nós
        # * transformarmos uma string em uma lista, dicionario inteiro etc... e vice versa, como o arquivo txt nos retorna uma string nós precisamos utilizar essa biblioteca.
        # * É necessario adicionar uma quebra de linhas para que cada variavel fique em uma linha
        arq.write(json.dumps(state))  # 1
        arq.write('\n')
        arq.write(json.dumps(Seg_cor_ativo))  # 2
        arq.write('\n')
        arq.write(json.dumps(Ter_cor_ativo))  # 3
        arq.write('\n')
        arq.write(json.dumps(Qua_cor_ativo))  # 4
        arq.write('\n')
        arq.write(json.dumps(Qui_cor_ativo))  # 5
        arq.write('\n')
        arq.write(json.dumps(Sex_cor_ativo))  # 6
        arq.write('\n')
        arq.write(json.dumps(Sab_cor_ativo))  # 7
        arq.write('\n')
        arq.write(json.dumps(Dom_cor_ativo))  # 8
        arq.write('\n')
        arq.write(json.dumps(state_dias))  # 9
        arq.write('\n')
        arq.write(json.dumps(horarios_cortinas_semana))  # 10
        arq.write('\n')
        arq.write(json.dumps(DiasSelecionados))  # 11
        arq.write('\n')
        arq.write(json.dumps(lista_botoes_seg))  # 12
        arq.write('\n')
        arq.write(json.dumps(lista_botoes_ter))  # 13
        arq.write('\n')
        arq.write(json.dumps(lista_botoes_qua))  # 14
        arq.write('\n')
        arq.write(json.dumps(lista_botoes_qui))  # 15
        arq.write('\n')
        arq.write(json.dumps(lista_botoes_sex))  # 16
        arq.write('\n')
        arq.write(json.dumps(lista_botoes_sab))  # 17
        arq.write('\n')
        arq.write(json.dumps(lista_botoes_dom))  # 18
        arq.write('\n')
        arq.write(json.dumps(i))  # 19
        arq.write('\n')
        arq.write(json.dumps(Seg_ali_ativo))  # 20
        arq.write('\n')
        arq.write(json.dumps(Ter_ali_ativo))  # 21
        arq.write('\n')
        arq.write(json.dumps(Qua_ali_ativo))  # 22
        arq.write('\n')
        arq.write(json.dumps(Qui_ali_ativo))  # 23
        arq.write('\n')
        arq.write(json.dumps(Sex_ali_ativo))  # 24
        arq.write('\n')
        arq.write(json.dumps(Sab_ali_ativo))  # 25
        arq.write('\n')
        arq.write(json.dumps(Dom_ali_ativo))  # 26
        arq.write('\n')
        arq.write(json.dumps(state_dias_ali))  # 27
        arq.write('\n')
        arq.write(json.dumps(horarios_alimentar_semana))  # 28
        arq.write('\n')
        arq.write(json.dumps(i2))  # 29
        arq.write('\n')
        arq.write(json.dumps(DiasSelecionadosAli))  # 30
        arq.write('\n')
        arq.write(json.dumps(lista_botoes_seg2))  # 31
        arq.write('\n')
        arq.write(json.dumps(lista_botoes_ter2))  # 32
        arq.write('\n')
        arq.write(json.dumps(lista_botoes_qua2))  # 33
        arq.write('\n')
        arq.write(json.dumps(lista_botoes_qui2))  # 34
        arq.write('\n')
        arq.write(json.dumps(lista_botoes_sex2))  # 35
        arq.write('\n')
        arq.write(json.dumps(lista_botoes_sab2))  # 36
        arq.write('\n')
        arq.write(json.dumps(lista_botoes_dom2))  # 37
        arq.write('\n')
        arq.write(json.dumps(VelocidadePWM))  # 38
        arq.write('\n')
        arq.write(json.dumps(Comida))  # 39
        arq.write('\n')
        arq.write(json.dumps(aquecer))  # 40
        arq.write('\n')
        arq.write(json.dumps(Temp_selec))  # 41
        arq.close()
        # Agora irei ler o arquivo todo e coloca-lo em uma lista usando a função readlines.
        # arq = open('banco_de_dados.txt', 'r')
        # conteudo_arquivo = arq.readlines()
        pass

    def LerDados():
        print('Lendo dados')
        # Cortinas
        nonlocal state
        nonlocal state_dias
        nonlocal horarios_cortinas_semana
        nonlocal DiasSelecionados
        nonlocal lista_botoes_seg
        nonlocal lista_botoes_ter
        nonlocal lista_botoes_qua
        nonlocal lista_botoes_qui
        nonlocal lista_botoes_sex
        nonlocal lista_botoes_sab
        nonlocal lista_botoes_dom
        # Alimentação
        nonlocal state_dias_ali
        nonlocal horarios_alimentar_semana
        nonlocal DiasSelecionadosAli
        nonlocal lista_botoes_seg2
        nonlocal lista_botoes_ter2
        nonlocal lista_botoes_qua2
        nonlocal lista_botoes_qui2
        nonlocal lista_botoes_sex2
        nonlocal lista_botoes_sab2
        nonlocal lista_botoes_dom2
        nonlocal VelocidadePWM
        nonlocal Comida
        nonlocal aquecer
        nonlocal Temp_selec

        conteudo_arq = []
        arq = open('banco_de_dados.txt', 'r')

        conteudo_arq = arq.readlines()
        # Cortinas
        state = conteudo_arq[0]
        state = json.loads(state)
        state_dias = conteudo_arq[8]
        state_dias = json.loads(state_dias)
        horarios_cortinas_semana = conteudo_arq[9]
        horarios_cortinas_semana = json.loads(horarios_cortinas_semana)
        print(horarios_cortinas_semana, type(horarios_cortinas_semana))
        DiasSelecionados = conteudo_arq[10]
        DiasSelecionados = json.loads(DiasSelecionados)
        lista_botoes_seg = conteudo_arq[11]
        lista_botoes_seg = json.loads(lista_botoes_seg)
        lista_botoes_ter = conteudo_arq[12]
        lista_botoes_ter = json.loads(lista_botoes_ter)
        lista_botoes_qua = conteudo_arq[13]
        lista_botoes_qua = json.loads(lista_botoes_qua)
        lista_botoes_qui = conteudo_arq[14]
        lista_botoes_qui = json.loads(lista_botoes_qui)
        lista_botoes_sex = conteudo_arq[15]
        lista_botoes_sex = json.loads(lista_botoes_sex)
        lista_botoes_sab = conteudo_arq[16]
        lista_botoes_sab = json.loads(lista_botoes_sab)
        lista_botoes_dom = conteudo_arq[17]
        lista_botoes_dom = json.loads(lista_botoes_dom)
        # Alimentação
        state_dias_ali = conteudo_arq[26]
        state_dias_ali = json.loads(state_dias_ali)
        horarios_alimentar_semana = conteudo_arq[27]
        horarios_alimentar_semana = json.loads(horarios_alimentar_semana)
        DiasSelecionadosAli = conteudo_arq[29]
        DiasSelecionadosAli = json.loads(DiasSelecionadosAli)
        lista_botoes_seg2 = conteudo_arq[30]
        lista_botoes_seg2 = json.loads(lista_botoes_seg2)
        lista_botoes_ter2 = conteudo_arq[31]
        lista_botoes_ter2 = json.loads(lista_botoes_ter2)
        lista_botoes_qua2 = conteudo_arq[32]
        lista_botoes_qua2 = json.loads(lista_botoes_qua2)
        lista_botoes_qui2 = conteudo_arq[33]
        lista_botoes_qui2 = json.loads(lista_botoes_qui2)
        lista_botoes_sex2 = conteudo_arq[34]
        lista_botoes_sex2 = json.loads(lista_botoes_sex2)
        lista_botoes_sab2 = conteudo_arq[35]
        lista_botoes_sab2 = json.loads(lista_botoes_sab2)
        lista_botoes_dom2 = conteudo_arq[36]
        lista_botoes_dom2 = json.loads(lista_botoes_dom2)
        VelocidadePWM = conteudo_arq[37]
        VelocidadePWM = json.loads(VelocidadePWM)
        Comida = conteudo_arq[38]
        Comida = json.loads(Comida)
        aquecer = conteudo_arq[39]
        aquecer = json.loads(aquecer)
        Temp_selec = conteudo_arq[40]
        Temp_selec = json.loads(Temp_selec)

    LerDados()

    def Salvar_dados_no_firebase(__DiasSelecionadosAli=False, __DiasSelecionadosCor=False, __HorariosAlimentar=False,
                                 __HorariosCortinas=False, __VelocidadePWM=False, __Aquecedor=False):
        nonlocal state_dias_ali  # DiasSelecionadosAli
        nonlocal state_dias  # DiasSelecionados
        nonlocal horarios_cortinas_semana
        nonlocal horarios_alimentar_semana
        nonlocal VelocidadePWM
        nonlocal aquecer
        nonlocal Temp_selec

        dict_VelocidadePWM = {'Velocidade': ''}
        dict_StateCortina = {'Cortinas': ''}
        dict_Aquecedor = {'Acionado': bool, 'Temp_selec': float}
        print('Salvando dados no firebase')

        if __DiasSelecionadosAli:  # ATUALIZANDO OS DIAS SELECIONADOS DA ALIMENTAÇÃO
            data_DiasSelecionadosAli = json.dumps(state_dias_ali)
            requisição = requests.patch(
                url="https://gaia-f6d06-default-rtdb.firebaseio.com/Dados/DiasSelecionadosAlimenta%C3%A7%C3%A3o.json",
                data=data_DiasSelecionadosAli)
            print(requisição.json())

        if __DiasSelecionadosCor:  # ATUALIZANDO OS DIAS SELECIONADAS DAS CORTINAS
            data_DiasSelecionadosCor = json.dumps(state_dias)
            requisição = requests.patch(
                url="https://gaia-f6d06-default-rtdb.firebaseio.com/Dados/DiasSelecionadosCortinas.json",
                data=data_DiasSelecionadosCor)
            print(requisição.json())

        if __HorariosAlimentar:  # ATUALIZANDO OS HORARIOS DA ALIMENTAÇÃO
            data_horarios_alimentar_semana = json.dumps(horarios_alimentar_semana)
            requisição = requests.patch(
                url="https://gaia-f6d06-default-rtdb.firebaseio.com/Dados/HorariosAlimentar.json",
                data=data_horarios_alimentar_semana)
            print(requisição)

        if __HorariosCortinas:  # ATUALIZANDO OS HORARIOS DAS CORTINAS
            data_horarios_cortinas_semana = json.dumps(horarios_cortinas_semana)
            requisição = requests.patch(
                url="https://gaia-f6d06-default-rtdb.firebaseio.com/Dados/HorariosCortinas.json",
                data=data_horarios_cortinas_semana)
            print(requisição)

        if __VelocidadePWM:  # ATUALIZANDO A VELOCIDADE DO ALIMENTADOR
            dict_VelocidadePWM['Velocidade'] = VelocidadePWM
            data_VelocidadePWM = json.dumps(dict_VelocidadePWM)
            requisição = requests.patch(url="https://gaia-f6d06-default-rtdb.firebaseio.com/Dados/VelocidadePWM.json",
                                        data=data_VelocidadePWM)
            print(requisição)

        if __Aquecedor:
            dict_Aquecedor['Acionado'] = aquecer
            dict_Aquecedor['Temp_selec'] = Temp_selec
            data_Aquecedor = json.dumps(dict_Aquecedor)
            requisição = requests.patch(url='https://gaia-f6d06-default-rtdb.firebaseio.com/Dados/Aquecedor.json',
                                        data=data_Aquecedor)
            print(requisição)
        pass

    # LIST VIEW DOS HORARIOS DOS DIAS
    Text_field_abre_seg = ft.TextField(label='A cortina abrirá as:', hint_text='ex:22:30', width=150, color=verde2,
                                       border_color=verde2, cursor_color=verde2, value='')
    Text_field_fecha_seg = ft.TextField(label='A cortina fechará as:', hint_text='ex:06:30', width=150, color=verde2,
                                        border_color=verde2, cursor_color=verde2, value='')
    # CADA DIA TERÁ O SEU PROPRIO TEXT FIELD NA ENTRADA DE DADOS, ISSO FOI FEITO PARA QUE SEJA POSSIVEL EXIBIR A MENSAGEM DE ERRO EM CADA UM DOS TEXT FIELDS, CASO CONTRARIO
    # SERIA IMPOSSIVEL EXIBIR A MENSAGEM E CADA DIA
    Text_field_abre_ter = ft.TextField(label='A cortina abrirá as:', hint_text='ex:22:30', width=150, color=verde2,
                                       border_color=verde2, cursor_color=verde2, value='')
    Text_field_fecha_ter = ft.TextField(label='A cortina fechará as:', hint_text='ex:06:30', width=150, color=verde2,
                                        border_color=verde2, cursor_color=verde2, value='')

    Text_field_abre_qua = ft.TextField(label='A cortina abrirá as:', hint_text='ex:22:30', width=150, color=verde2,
                                       border_color=verde2, cursor_color=verde2, value='')
    Text_field_fecha_qua = ft.TextField(label='A cortina fechará as:', hint_text='ex:06:30', width=150, color=verde2,
                                        border_color=verde2, cursor_color=verde2, value='')

    Text_field_abre_qui = ft.TextField(label='A cortina abrirá as:', hint_text='ex:22:30', width=150, color=verde2,
                                       border_color=verde2, cursor_color=verde2, value='')
    Text_field_fecha_qui = ft.TextField(label='A cortina fechará as:', hint_text='ex:06:30', width=150, color=verde2,
                                        border_color=verde2, cursor_color=verde2, value='')

    Text_field_abre_sex = ft.TextField(label='A cortina abrirá as:', hint_text='ex:22:30', width=150, color=verde2,
                                       border_color=verde2, cursor_color=verde2, value='')
    Text_field_fecha_sex = ft.TextField(label='A cortina fechará as:', hint_text='ex:06:30', width=150, color=verde2,
                                        border_color=verde2, cursor_color=verde2, value='')

    Text_field_abre_sab = ft.TextField(label='A cortina abrirá as:', hint_text='ex:22:30', width=150, color=verde2,
                                       border_color=verde2, cursor_color=verde2, value='')
    Text_field_fecha_sab = ft.TextField(label='A cortina fechará as:', hint_text='ex:06:30', width=150, color=verde2,
                                        border_color=verde2, cursor_color=verde2, value='')

    Text_field_abre_dom = ft.TextField(label='A cortina abrirá as:', hint_text='ex:22:30', width=150, color=verde2,
                                       border_color=verde2, cursor_color=verde2, value='')
    Text_field_fecha_dom = ft.TextField(label='A cortina fechará as:', hint_text='ex:06:30', width=150, color=verde2,
                                        border_color=verde2, cursor_color=verde2, value='')

    adicionar_horarioCor = ft.ElevatedButton(icon=ft.icons.ADD, text="Adicionar", color=branco2, bgcolor=verde1,
                                             on_click=adicionar_cor, icon_color=branco2,
                                             style=ft.ButtonStyle(color=branco2))

    list_horario_seg = ft.ListView(
        expand=1,
        spacing=10,
        padding=20,
        auto_scroll=True,
        width=450,
    )
    list_horario_ter = ft.ListView(
        expand=1,
        spacing=10,
        padding=20,
        auto_scroll=True,
        width=450,
    )
    list_horario_qua = ft.ListView(
        expand=1,
        spacing=10,
        padding=20,
        auto_scroll=True,
        width=450,
    )
    list_horario_qui = ft.ListView(
        expand=1,
        spacing=10,
        padding=20,
        auto_scroll=True,
        width=450,
    )
    list_horario_sex = ft.ListView(
        expand=1,
        spacing=10,
        padding=20,
        auto_scroll=True,
        width=450,
    )
    list_horario_sab = ft.ListView(
        expand=1,
        spacing=10,
        padding=20,
        auto_scroll=True,
        width=450,
    )
    list_horario_dom = ft.ListView(
        expand=1,
        spacing=10,
        padding=20,
        auto_scroll=True,
        width=450,
    )

    # CONTANERS DOS DIAS
    # Segunda
    Seg_cor = ft.Container(
        offset=ft.transform.Offset(0, -0.55),
        content=ft.Container(bgcolor=branco2,
                             border_radius=ft.border_radius.all(20),
                             visible=False,
                             width=400,
                             height=400,
                             content=ft.Column(
                                 spacing=1,
                                 horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                 offset=ft.transform.Offset(0.05, 0.08),
                                 controls=[
                                     ft.Row(controls=[
                                         ft.Container(border_radius=100, offset=ft.transform.Offset(0.12, -0.5),
                                                      alignment=ft.alignment.center, bgcolor=verde1, width=250,
                                                      height=40,
                                                      content=ft.Text(value="Segunda-feira", color=branco2, size=20))]),
                                     ft.Row(controls=[Text_field_fecha_seg, Text_field_abre_seg, ]),
                                     ft.Row(controls=[adicionar_horarioCor], offset=ft.transform.Offset(0.25, 0.25)),
                                     list_horario_seg,
                                 ]
                             )
                             ),
    )
    # Terça
    Ter_cor = ft.Container(
        offset=ft.transform.Offset(0, -0.615),
        border_radius=ft.border_radius.all(20),
        content=ft.Container(bgcolor=branco2,
                             border_radius=ft.border_radius.all(20),
                             visible=False,
                             width=400,
                             height=400,
                             content=ft.Column(
                                 spacing=1,
                                 horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                 offset=ft.transform.Offset(0.05, 0.08),
                                 controls=[
                                     ft.Row(controls=[
                                         ft.Container(border_radius=100, offset=ft.transform.Offset(0.12, -0.5),
                                                      alignment=ft.alignment.center, bgcolor=verde1, width=250,
                                                      height=40,
                                                      content=ft.Text(value="Terça-feira", color=branco2, size=20))]),
                                     ft.Row(controls=[Text_field_fecha_ter, Text_field_abre_ter, ]),
                                     ft.Row(controls=[adicionar_horarioCor], offset=ft.transform.Offset(0.25, 0.25)),
                                     list_horario_ter,
                                 ]
                             )
                             ),
    )
    # Quarta
    Qua_cor = ft.Container(
        offset=ft.transform.Offset(0, -0.680),
        content=ft.Container(bgcolor=branco2,
                             border_radius=ft.border_radius.all(20),
                             visible=False,
                             width=400,
                             height=400,
                             content=ft.Column(
                                 spacing=1,
                                 horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                 offset=ft.transform.Offset(0.05, 0.08),
                                 controls=[
                                     ft.Row(controls=[
                                         ft.Container(border_radius=100, offset=ft.transform.Offset(0.12, -0.5),
                                                      alignment=ft.alignment.center, bgcolor=verde1, width=250,
                                                      height=40,
                                                      content=ft.Text(value="Quarta-feira", color=branco2, size=20))]),
                                     ft.Row(controls=[Text_field_fecha_qua, Text_field_abre_qua, ]),
                                     ft.Row(controls=[adicionar_horarioCor], offset=ft.transform.Offset(0.25, 0.25)),
                                     list_horario_qua,
                                 ]
                             )
                             ),
    )
    # Quinta
    Qui_cor = ft.Container(
        offset=ft.transform.Offset(0, -0.745),
        content=ft.Container(bgcolor=branco2,
                             border_radius=ft.border_radius.all(20),
                             visible=False,
                             width=400,
                             height=400,
                             content=ft.Column(
                                 spacing=1,
                                 horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                 offset=ft.transform.Offset(0.05, 0.08),
                                 controls=[
                                     ft.Row(controls=[
                                         ft.Container(border_radius=100, offset=ft.transform.Offset(0.12, -0.5),
                                                      alignment=ft.alignment.center, bgcolor=verde1, width=250,
                                                      height=40,
                                                      content=ft.Text(value="Quinta-feira", color=branco2, size=20))]),
                                     ft.Row(controls=[Text_field_fecha_qui, Text_field_abre_qui, ]),
                                     ft.Row(controls=[adicionar_horarioCor], offset=ft.transform.Offset(0.25, 0.25)),
                                     list_horario_qui,
                                 ]
                             )
                             ),
    )
    # Sexta
    Sex_cor = ft.Container(
        offset=ft.transform.Offset(0, -0.810),
        content=ft.Container(bgcolor=branco2,
                             border_radius=ft.border_radius.all(20),
                             visible=False,
                             width=400,
                             height=400,
                             content=ft.Column(
                                 spacing=1,
                                 horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                 offset=ft.transform.Offset(0.05, 0.08),
                                 controls=[
                                     ft.Row(controls=[
                                         ft.Container(border_radius=100, offset=ft.transform.Offset(0.12, -0.5),
                                                      alignment=ft.alignment.center, bgcolor=verde1, width=250,
                                                      height=40,
                                                      content=ft.Text(value="Sexta-feira", color=branco2, size=20))]),
                                     ft.Row(controls=[Text_field_fecha_sex, Text_field_abre_sex, ]),
                                     ft.Row(controls=[adicionar_horarioCor], offset=ft.transform.Offset(0.25, 0.25)),
                                     list_horario_sex,
                                 ]
                             )
                             ),
    )
    # Sabado
    Sab_cor = ft.Container(
        offset=ft.transform.Offset(0, -0.875),
        content=ft.Container(bgcolor=branco2,
                             border_radius=ft.border_radius.all(20),
                             visible=False,
                             width=400,
                             height=400,
                             content=ft.Column(
                                 spacing=1,
                                 horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                 offset=ft.transform.Offset(0.05, 0.08),
                                 controls=[
                                     ft.Row(controls=[
                                         ft.Container(border_radius=100, offset=ft.transform.Offset(0.12, -0.5),
                                                      alignment=ft.alignment.center, bgcolor=verde1, width=250,
                                                      height=40,
                                                      content=ft.Text(value="Sábado", color=branco2, size=20))]),
                                     ft.Row(controls=[Text_field_fecha_sab, Text_field_abre_sab, ]),
                                     ft.Row(controls=[adicionar_horarioCor], offset=ft.transform.Offset(0.25, 0.25)),
                                     list_horario_sab,
                                 ]
                             )
                             ),
    )
    # Domingo
    Dom_cor = ft.Container(
        offset=ft.transform.Offset(0, -0.940),
        content=ft.Container(bgcolor=branco2,
                             border_radius=ft.border_radius.all(20),
                             visible=False,
                             width=400,
                             height=400,
                             content=ft.Column(
                                 spacing=1,
                                 horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                 offset=ft.transform.Offset(0.05, 0.08),
                                 controls=[
                                     ft.Row(controls=[
                                         ft.Container(border_radius=100, offset=ft.transform.Offset(0.12, -0.5),
                                                      alignment=ft.alignment.center, bgcolor=verde1, width=250,
                                                      height=40,
                                                      content=ft.Text(value="Domingo", color=branco2, size=20))]),
                                     ft.Row(controls=[Text_field_fecha_dom, Text_field_abre_dom, ]),
                                     ft.Row(controls=[adicionar_horarioCor], offset=ft.transform.Offset(0.25, 0.25)),
                                     list_horario_dom,
                                 ]
                             )
                             ),
    )

    # PROXIMO DIA
    msg_proximo_dia = ft.AlertDialog(
        #bgcolor=verde1,
        modal=True,
        content=ft.Text(value="Você quer abrir a cortina no próximo dia?"),
        actions=[
            ft.ElevatedButton(text="Sim", bgcolor=branco2, on_click=proximo_dia,
                              content=ft.Text(value=f"Sim", color=verde2, bgcolor=branco2)),
            ft.ElevatedButton(text="Não", bgcolor=branco2, on_click=proximo_dia,
                              content=ft.Text(value="Não", color=verde2, bgcolor=branco2)),
        ]
    )

    Segunda_cor_icon = ft.Container(border_radius=100, height=60, width=60, alignment=ft.alignment.center,
                                on_click=DiaSelecionado_cor, bgcolor=branco2,
                                content=ft.Text(value="Seg", color=verde2, size=18))
    Terca_cor_icon = ft.Container(border_radius=100, height=60, width=60, alignment=ft.alignment.center,
                              on_click=DiaSelecionado_cor, bgcolor=branco2,
                              content=ft.Text(value="Ter", color=verde2, size=18))
    Quarta_cor_icon = ft.Container(border_radius=100, height=60, width=60, alignment=ft.alignment.center,
                               on_click=DiaSelecionado_cor, bgcolor=branco2,
                               content=ft.Text(value="Qua", color=verde2, size=18))
    Quinta_cor_icon = ft.Container(border_radius=100, height=60, width=60, alignment=ft.alignment.center,
                               on_click=DiaSelecionado_cor, bgcolor=branco2,
                               content=ft.Text(value="Qui", color=verde2, size=18))
    Sexta_cor_icon = ft.Container(border_radius=100, height=60, width=60, alignment=ft.alignment.center,
                              on_click=DiaSelecionado_cor, bgcolor=branco2,
                              content=ft.Text(value="Sex", color=verde2, size=18))
    Sabado_cor_icon = ft.Container(border_radius=100, height=60, width=60, alignment=ft.alignment.center,
                               on_click=DiaSelecionado_cor, bgcolor=branco2,
                               content=ft.Text(value="Sab", color=verde2, size=18))
    Domingo_cor_icon = ft.Container(border_radius=100, height=60, width=60, alignment=ft.alignment.center,
                                on_click=DiaSelecionado_cor, bgcolor=branco2,
                                content=ft.Text(value="Dom", color=verde2, size=18))
    # Dias da semana cortinas
    dias_da_semana1 = ft.Row(
        offset=ft.transform.Offset(-0.14, 0),  # (-0.16, 0),
        scale=0.75,
        auto_scroll=True,
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            Segunda_cor_icon,
            Terca_cor_icon,
            Quarta_cor_icon,
            Quinta_cor_icon,
            Sexta_cor_icon,
        ],
    )
    dias_da_semana2 = ft.Row(
        offset=ft.transform.Offset(0.36, -1.42),  # (-0.16, 0),
        scale=0.75,
        auto_scroll=True,
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            Sabado_cor_icon,
            Domingo_cor_icon,
        ],
    )

    # SETAS DOS DIAS DA SEMANA CORTINAS:
    set_segunda = ft.IconButton(icon=ft.icons.ARROW_RIGHT, icon_color=verde1, on_click=Segunda,
                                animate_offset=ft.animation.Animation(duration=700), animate_opacity=100,
                                rotate=ft.transform.Rotate(angle=0, alignment=ft.alignment.center))
    set_terca = ft.IconButton(icon=ft.icons.ARROW_RIGHT, icon_color=verde1, on_click=Terca,
                              animate_offset=ft.animation.Animation(duration=700), animate_opacity=100,
                              rotate=ft.transform.Rotate(angle=0, alignment=ft.alignment.center))
    set_quarta = ft.IconButton(icon=ft.icons.ARROW_RIGHT, icon_color=verde1, on_click=Quarta,
                               animate_offset=ft.animation.Animation(duration=700), animate_opacity=100,
                               rotate=ft.transform.Rotate(angle=0, alignment=ft.alignment.center))
    set_quinta = ft.IconButton(icon=ft.icons.ARROW_RIGHT, icon_color=verde1, on_click=Quinta,
                               animate_offset=ft.animation.Animation(duration=700), animate_opacity=100,
                               rotate=ft.transform.Rotate(angle=0, alignment=ft.alignment.center))
    set_sexta = ft.IconButton(icon=ft.icons.ARROW_RIGHT, icon_color=verde1, on_click=Sexta,
                              animate_offset=ft.animation.Animation(duration=700), animate_opacity=100,
                              rotate=ft.transform.Rotate(angle=0, alignment=ft.alignment.center))
    set_sabado = ft.IconButton(icon=ft.icons.ARROW_RIGHT, icon_color=verde1, on_click=Sabado,
                               animate_offset=ft.animation.Animation(duration=700), animate_opacity=100,
                               rotate=ft.transform.Rotate(angle=0, alignment=ft.alignment.center))
    set_domingo = ft.IconButton(icon=ft.icons.ARROW_RIGHT, icon_color=verde1, on_click=Domingo,
                                animate_offset=ft.animation.Animation(duration=700), animate_opacity=100,
                                rotate=ft.transform.Rotate(angle=0, alignment=ft.alignment.center))

    setas_cor1 = ft.Row(
        scale=0.75,
        offset=ft.transform.Offset(-0.21, -2.6),
        spacing=23,
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            set_segunda,
            set_terca,
            set_quarta,
            set_quinta,
        ],
    )
    setas_cor2 = ft.Row(
        scale=0.75,
        offset=ft.transform.Offset(0.3, -4.13),
        spacing=23,
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            set_sexta,
            set_sabado,
            set_domingo,
        ],
    )

    Mostrador1 = ft.Icon(
        name=ft.icons.RADIO_BUTTON_OFF if Cortina_ativa else ft.icons.RADIO_BUTTON_ON,
        size=20,
        color=verde2,
    )
    # EXIBIÇÃO DO ESTADO DA CORTINA DA GAIOLA
    Texto1_cortina = ft.Container(
        width=400,
        height=50,
        border_radius=ft.border_radius.all(20),
        bgcolor=branco2,
        content=ft.Row(
            spacing=150,
            controls=[
                ft.Text("Cortinas abaixadas", size=20, color=verde2, offset=ft.transform.Offset(0.1, 0)),
                Mostrador1,
            ]
        )
    )

    Mostrador2 = ft.Icon(
        name=ft.icons.RADIO_BUTTON_ON if Cortina_ativa else ft.icons.RADIO_BUTTON_OFF,
        color=verde2,
        size=20,
    )

    Texto2_cortina = ft.Container(
        width=400,
        height=50,
        border_radius=ft.border_radius.all(20),
        bgcolor=branco2,
        content=ft.Row(
            spacing=165,
            controls=[
                ft.Text("Cortinas levantas", size=20, color=verde2, offset=ft.transform.Offset(0.1, 0)),
                Mostrador2,
            ]
        )
    )
    # LINHA DESENHADA
    LinhaVerde = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[ft.Container(
            width=350,
            height=1,
            bgcolor=verde2,
        ), ]
    )

    # ALIMENTAÇÃO
    # LINHA 1 ALIMENTAÇÃO
    # BOTÃO DE ALIMENTAÇÃO COM ANIMAÇÃO
    botao_alimentar = ft.IconButton(icon=ft.icons.FASTFOOD_OUTLINED, icon_size=30, icon_color=verde2, on_click=Alimentar)  # FOOD_BANK

    pb = ft.ProgressRing(height=40, width=40, color=verde2, bgcolor=branco2, value=0, visible=False, offset=ft.transform.Offset(7.7, -19.6))

    line1_ali = ft.Container(
        border_radius=ft.border_radius.all(10),
        bgcolor=branco2,
        shadow=ft.BoxShadow(
            color=branco2,
            blur_style=ft.ShadowBlurStyle.NORMAL,
        ),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=110,
            controls=[
            ft.Text('Acionar alimentador', color=verde2, size=20), botao_alimentar
            ]
        )
    )
    # SELEÇÃO DAS COMIDAS
    # Pequeno
    line2_ali = ft.Container(
        height=45,
        border_radius=ft.border_radius.all(10),
        bgcolor=branco2,
        shadow=ft.BoxShadow(
            color=branco2,
            blur_style=ft.ShadowBlurStyle.NORMAL,
        ),
        content=ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[
            ft.Text('Selecione o tamanho do grão', color=verde2, size=20, text_align=ft.TextAlign.CENTER),
                ]
           )
    )

    alimentos_Pequeno = ft.Container(content=ft.GridView(
        expand=True,
        runs_count=3,
        width=450,
        max_extent=150,
        child_aspect_ratio=1.0,
        spacing=5,
        run_spacing=5,
        visible=True,
        auto_scroll=True,
    )
    )
    for p, l in enumerate(LinkImagensComida['Pequeno']):
        alimentos_Pequeno.content.controls.append(
            ft.Stack([
                ft.Image(
                    width=150,
                    height=150,
                    src=l,
                    fit=ft.ImageFit.NONE,
                    repeat=ft.ImageRepeat.NO_REPEAT,
                    border_radius=ft.border_radius.all(10),
                ),
                ft.Row(controls=[
                    ft.TextButton(text=NomeAlimentos['Pequeno'][p], scale=0.8,
                                  style=ft.ButtonStyle(bgcolor=verde1, color=branco2))
                ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ])
        )

    # Médio
    alimentos_medio = ft.Container(
        content=ft.GridView(
        expand=True,
        runs_count=3,
        width=450,
        max_extent=150,
        child_aspect_ratio=1.0,
        spacing=5,
        run_spacing=5,
        visible=True,
        auto_scroll=True,
        )
    )
    for p, l in enumerate(LinkImagensComida['Médio']):
        alimentos_medio.content.controls.append(
            ft.Stack([
                ft.Image(
                    width=150,
                    height=150,
                    src=l,
                    fit=ft.ImageFit.NONE,
                    repeat=ft.ImageRepeat.NO_REPEAT,
                    border_radius=ft.border_radius.all(10),
                ),
                ft.Row(controls=[
                    ft.TextButton(text=NomeAlimentos['Médio'][p], scale=0.8,
                                  style=ft.ButtonStyle(bgcolor=verde1, color=branco2))
                ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ])
        )

    # Grande
    alimentos_Grande = ft.Container(content=ft.GridView(
        expand=True,
        runs_count=3,
        width=450,
        max_extent=150,
        child_aspect_ratio=1.0,
        spacing=5,
        run_spacing=5,
        visible=True,
        auto_scroll=True,
    )
    )
    for p, l in enumerate(LinkImagensComida['Grande']):
        alimentos_Grande.content.controls.append(
            ft.Stack([
                ft.Image(
                    width=150,
                    height=150,
                    src=l,
                    fit=ft.ImageFit.NONE,
                    repeat=ft.ImageRepeat.NO_REPEAT,
                    border_radius=ft.border_radius.all(10),
                ),
                ft.Row(controls=[
                    ft.TextButton(text=NomeAlimentos['Grande'][p], scale=0.8,
                                  style=ft.ButtonStyle(bgcolor=verde1, color=branco2))
                ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ])
        )

    Mostradores = ft.RadioGroup(on_change=FoodChange, content=ft.Column(
        controls=[ft.Radio(value="Pequeno", label="Pequeno", fill_color=verde2),
                  ft.Radio(value="medio", label="Médio", fill_color=verde2),
                  ft.Radio(value="Grande", label="Grande", fill_color=verde2, )]))

    botao_exemplos_Pequeno = ft.TextButton(text='Exemplos', on_click=ExemplosPequeno, icon=ft.icons.ARROW_DROP_DOWN,
                                        icon_color=branco2, style=ft.ButtonStyle(color=branco2, bgcolor=verde2))
    botao_exemplos_medio = ft.TextButton(text='Exemplos', on_click=ExemplosMedio, icon=ft.icons.ARROW_DROP_DOWN,
                                         icon_color=branco2, style=ft.ButtonStyle(color=branco2, bgcolor=verde2))
    botao_exemplos_Grande = ft.TextButton(text='Exemplos', on_click=ExemplosGrande, icon=ft.icons.ARROW_DROP_DOWN,
                                         icon_color=branco2, style=ft.ButtonStyle(color=branco2, bgcolor=verde2))

    botao_fechar_exemplos = ft.TextButton(text='Fechar', icon=ft.icons.CLOSE_SHARP, icon_color=branco2,
                                          on_click=FecharExemplos,
                                          style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10),
                                                               bgcolor=verde1, color=branco2))

    alimentos_Pequeno.content.controls.append(botao_fechar_exemplos)
    alimentos_medio.content.controls.append(botao_fechar_exemplos)
    alimentos_Grande.content.controls.append(botao_fechar_exemplos)

    Selecao_do_tipo_comida = ft.Row(
        spacing=125,
        controls=[
            Mostradores,
            ft.Column(controls=[botao_exemplos_Pequeno, botao_exemplos_medio, botao_exemplos_Grande])
        ]
    )

    adicionar_horarioAli = ft.IconButton(icon=ft.icons.ADD, on_click=RegistroAli, icon_color=verde2)
    # TEXT FIELD DOS DIAS DA ALIMENTAÇÃO

    Text_field_alimentar_seg = ft.TextField(label='Alimentar as:', hint_text='ex:22:30', width=150, color=verde2,
                                            border_color=verde2, cursor_color=verde2, value='')
    Text_field_alimentar_ter = ft.TextField(label='Alimentar as:', hint_text='ex:22:30', width=150, color=verde2,
                                            border_color=verde2, cursor_color=verde2, value='')
    Text_field_alimentar_qua = ft.TextField(label='Alimentar as:', hint_text='ex:09:30', width=150, color=verde2,
                                            border_color=verde2, cursor_color=verde2, value='')
    Text_field_alimentar_qui = ft.TextField(label='Alimentar as:', hint_text='ex:09:30', width=150, color=verde2,
                                            border_color=verde2, cursor_color=verde2, value='')
    Text_field_alimentar_sex = ft.TextField(label='Alimentar as:', hint_text='ex:09:30', width=150, color=verde2,
                                            border_color=verde2, cursor_color=verde2, value='')
    Text_field_alimentar_sab = ft.TextField(label='Alimentar as:', hint_text='ex:09:30', width=150, color=verde2,
                                            border_color=verde2, cursor_color=verde2, value='')
    Text_field_alimentar_dom = ft.TextField(label='Alimentar as:', hint_text='ex:09:30', width=150, color=verde2,
                                            border_color=verde2, cursor_color=verde2, value='')

    # Icons dos dias da semana alimentação
    Segunda_ali_icon = ft.Container(border_radius=100, height=60, width=60, alignment=ft.alignment.center,
                                    on_click=DiaSelecionado_ali, bgcolor=branco2,
                                    content=ft.Text(value="Seg", color=verde2, size=18, ))
    Terca_ali_icon = ft.Container(border_radius=100, height=60, width=60, alignment=ft.alignment.center,
                                  on_click=DiaSelecionado_ali, bgcolor=branco2,
                                  content=ft.Text(value="Ter", color=verde2, size=18))
    Quarta_ali_icon = ft.Container(border_radius=100, height=60, width=60, alignment=ft.alignment.center,
                                   on_click=DiaSelecionado_ali, bgcolor=branco2,
                                   content=ft.Text(value="Qua", color=verde2, size=18))
    Quinta_ali_icon = ft.Container(border_radius=100, height=60, width=60, alignment=ft.alignment.center,
                                   on_click=DiaSelecionado_ali, bgcolor=branco2,
                                   content=ft.Text(value="Qui", color=verde2, size=18))
    Sexta_ali_icon = ft.Container(border_radius=100, height=60, width=60, alignment=ft.alignment.center,
                                  on_click=DiaSelecionado_ali, bgcolor=branco2,
                                  content=ft.Text(value="Sex", color=verde2, size=18))
    Sabado_ali_icon = ft.Container(border_radius=100, height=60, width=60, alignment=ft.alignment.center,
                                   on_click=DiaSelecionado_ali, bgcolor=branco2,
                                   content=ft.Text(value="Sab", color=verde2, size=18))
    Domingo_ali_icon = ft.Container(border_radius=100, height=60, width=60, alignment=ft.alignment.center,
                                    on_click=DiaSelecionado_ali, bgcolor=branco2,
                                    content=ft.Text(value="Dom", color=verde2, size=18))

    # Dias da semana alimentação
    dias_da_semana_ali1 = ft.Row(
        spacing=5,
        auto_scroll=True,
        scale=0.75,
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            Segunda_ali_icon,
            Terca_ali_icon,
            Quarta_ali_icon,
            Quinta_ali_icon,
            Sexta_ali_icon,
        ],
        offset=ft.transform.Offset(-0.16, 0)
    )
    dias_da_semana_ali2 = ft.Row(
        spacing=5,
        auto_scroll=True,
        scale=0.75,
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            Sabado_ali_icon,
            Domingo_ali_icon,
        ],
        offset=ft.transform.Offset(0.312, -1.43)
    )

    # lista de horarios
    list_horario_seg2 = ft.ListView(
        expand=1,
        spacing=10,
        padding=20,
        auto_scroll=True,
        width=450,
    )
    list_horario_ter2 = ft.ListView(
        expand=1,
        spacing=10,
        padding=20,
        auto_scroll=True,
        width=450,
    )
    list_horario_qua2 = ft.ListView(
        expand=1,
        spacing=10,
        padding=20,
        auto_scroll=True,
        width=450,
    )
    list_horario_qui2 = ft.ListView(
        expand=1,
        spacing=10,
        padding=20,
        auto_scroll=True,
        width=450,
    )
    list_horario_sex2 = ft.ListView(
        expand=1,
        spacing=10,
        padding=20,
        auto_scroll=True,
        width=450,
    )
    list_horario_sab2 = ft.ListView(
        expand=1,
        spacing=10,
        padding=20,
        auto_scroll=True,
        width=450,
    )
    list_horario_dom2 = ft.ListView(
        expand=1,
        spacing=10,
        padding=20,
        auto_scroll=True,
        width=450,
    )

    # Segunda
    Seg_ali = ft.Container(
        offset=ft.transform.Offset(0, -0.4),
        border_radius=ft.border_radius.all(20),
        content=ft.Container(bgcolor=branco2,
                             border_radius=ft.border_radius.all(20),
                             visible=False,
                             width=400,
                             height=400,
                             content=ft.Column(
                                 spacing=1,
                                 horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                 offset=ft.transform.Offset(0.05, 0.08),
                                 controls=[
                                     ft.Row(controls=[
                                         ft.Container(border_radius=100, offset=ft.transform.Offset(0.12, -0.5),
                                                      alignment=ft.alignment.center, bgcolor=verde1, width=250,
                                                      height=40,
                                                      content=ft.Text(value="Segunda-feira", color=branco2, size=20))]),
                                     ft.Row(alignment=ft.MainAxisAlignment.CENTER,
                                            controls=[Text_field_alimentar_seg, adicionar_horarioAli]),
                                     list_horario_seg2,
                                 ]
                             )
                             ),
    )
    # terca
    Ter_ali = ft.Container(
        offset=ft.transform.Offset(0, -0.465),
        border_radius=ft.border_radius.all(20),
        content=ft.Container(bgcolor=branco2,
                             border_radius=ft.border_radius.all(20),
                             visible=False,
                             width=400,
                             height=400,
                             content=ft.Column(
                                 spacing=1,
                                 horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                 offset=ft.transform.Offset(0.05, 0.08),
                                 controls=[
                                     ft.Row(controls=[
                                         ft.Container(border_radius=100, offset=ft.transform.Offset(0.12, -0.5),
                                                      alignment=ft.alignment.center, bgcolor=verde1, width=250,
                                                      height=40,
                                                      content=ft.Text(value="Terça-feira", color=branco2, size=20))]),
                                     ft.Row(alignment=ft.MainAxisAlignment.CENTER,
                                            controls=[Text_field_alimentar_ter, adicionar_horarioAli]),
                                     list_horario_ter2,
                                 ]
                             )
                             ),
    )
    # Quarta
    # Segunda
    Qua_ali = ft.Container(
        offset=ft.transform.Offset(0, -0.530),
        border_radius=ft.border_radius.all(20),
        content=ft.Container(bgcolor=branco2,
                             border_radius=ft.border_radius.all(20),
                             visible=False,
                             width=400,
                             height=400,
                             content=ft.Column(
                                 spacing=1,
                                 horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                 offset=ft.transform.Offset(0.05, 0.08),
                                 controls=[
                                     ft.Row(controls=[
                                         ft.Container(border_radius=100, offset=ft.transform.Offset(0.12, -0.5),
                                                      alignment=ft.alignment.center, bgcolor=verde1, width=250,
                                                      height=40,
                                                      content=ft.Text(value="Quarta-feira", color=branco2, size=20))]),
                                     ft.Row(alignment=ft.MainAxisAlignment.CENTER,
                                            controls=[Text_field_alimentar_qua, adicionar_horarioAli]),
                                     list_horario_qua2,
                                 ]
                             )
                             ),
    )
    # Quinta
    Qui_ali = ft.Container(
        offset=ft.transform.Offset(0, -0.595),
        border_radius=ft.border_radius.all(20),
        content=ft.Container(bgcolor=branco2,
                             border_radius=ft.border_radius.all(20),
                             visible=False,
                             width=400,
                             height=400,
                             content=ft.Column(
                                 spacing=1,
                                 horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                 offset=ft.transform.Offset(0.05, 0.08),
                                 controls=[
                                     ft.Row(controls=[
                                         ft.Container(border_radius=100, offset=ft.transform.Offset(0.12, -0.5),
                                                      alignment=ft.alignment.center, bgcolor=verde1, width=250,
                                                      height=40,
                                                      content=ft.Text(value="Quinta-feira", color=branco2, size=20))]),
                                     ft.Row(alignment=ft.MainAxisAlignment.CENTER,
                                            controls=[Text_field_alimentar_qui, adicionar_horarioAli]),
                                     list_horario_qui2,
                                 ]
                             )
                             ),
    )
    # Sexta
    Sex_ali = ft.Container(
        offset=ft.transform.Offset(0, -0.660),
        border_radius=ft.border_radius.all(20),
        content=ft.Container(bgcolor=branco2,
                             border_radius=ft.border_radius.all(20),
                             visible=False,
                             width=400,
                             height=400,
                             content=ft.Column(
                                 spacing=1,
                                 horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                 offset=ft.transform.Offset(0.05, 0.08),
                                 controls=[
                                     ft.Row(controls=[
                                         ft.Container(border_radius=100, offset=ft.transform.Offset(0.12, -0.5),
                                                      alignment=ft.alignment.center, bgcolor=verde1, width=250,
                                                      height=40,
                                                      content=ft.Text(value="Sexta-feira", color=branco2, size=20))]),
                                     ft.Row(alignment=ft.MainAxisAlignment.CENTER,
                                            controls=[Text_field_alimentar_sex, adicionar_horarioAli]),
                                     list_horario_sex2,
                                 ]
                             )
                             ),
    )
    # Sabado
    Sab_ali = ft.Container(
        offset=ft.transform.Offset(0, -0.725),
        border_radius=ft.border_radius.all(20),
        content=ft.Container(bgcolor=branco2,
                             border_radius=ft.border_radius.all(20),
                             visible=False,
                             width=400,
                             height=400,
                             content=ft.Column(
                                 spacing=1,
                                 horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                 offset=ft.transform.Offset(0.05, 0.08),
                                 controls=[
                                     ft.Row(controls=[
                                         ft.Container(border_radius=100, offset=ft.transform.Offset(0.12, -0.5),
                                                      alignment=ft.alignment.center, bgcolor=verde1, width=250,
                                                      height=40,
                                                      content=ft.Text(value="Sábado", color=branco2, size=20))]),
                                     ft.Row(alignment=ft.MainAxisAlignment.CENTER,
                                            controls=[Text_field_alimentar_sab, adicionar_horarioAli]),
                                     list_horario_sab2, ]
                             )
                             ),
    )
    # Domingo
    Dom_ali = ft.Container(
        offset=ft.transform.Offset(0, -0.790),
        border_radius=ft.border_radius.all(20),
        content=ft.Container(bgcolor=branco2,
                             border_radius=ft.border_radius.all(20),
                             visible=False,
                             width=400,
                             height=400,
                             content=ft.Column(
                                 spacing=1,
                                 horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                 offset=ft.transform.Offset(0.05, 0.08),
                                 controls=[
                                     ft.Row(controls=[
                                         ft.Container(border_radius=100, offset=ft.transform.Offset(0.12, -0.5),
                                                      alignment=ft.alignment.center, bgcolor=verde1, width=250,
                                                      height=40,
                                                      content=ft.Text(value="Domingo", color=branco2, size=20))]),
                                     ft.Row(alignment=ft.MainAxisAlignment.CENTER,
                                            controls=[Text_field_alimentar_dom, adicionar_horarioAli]),
                                     list_horario_dom2,
                                 ]
                             )
                             ),
    )

    # SETAS DOS DIAS DA SEMANA ALIMENTAÇÃO:
    set_segunda2 = ft.IconButton(icon=ft.icons.ARROW_RIGHT, icon_color=verde1, on_click=Segunda2,
                                 animate_offset=ft.animation.Animation(duration=700), animate_opacity=100,
                                 rotate=ft.transform.Rotate(angle=0, alignment=ft.alignment.center))
    set_terca2 = ft.IconButton(icon=ft.icons.ARROW_RIGHT, icon_color=verde1, on_click=Terca2,
                               animate_offset=ft.animation.Animation(duration=700), animate_opacity=100,
                               rotate=ft.transform.Rotate(angle=0, alignment=ft.alignment.center))
    set_quarta2 = ft.IconButton(icon=ft.icons.ARROW_RIGHT, icon_color=verde1, on_click=Quarta2,
                                animate_offset=ft.animation.Animation(duration=700), animate_opacity=100,
                                rotate=ft.transform.Rotate(angle=0, alignment=ft.alignment.center))
    set_quinta2 = ft.IconButton(icon=ft.icons.ARROW_RIGHT, icon_color=verde1, on_click=Quinta2,
                                animate_offset=ft.animation.Animation(duration=700), animate_opacity=100,
                                rotate=ft.transform.Rotate(angle=0, alignment=ft.alignment.center))
    set_sexta2 = ft.IconButton(icon=ft.icons.ARROW_RIGHT, icon_color=verde1, on_click=Sexta2,
                               animate_offset=ft.animation.Animation(duration=700), animate_opacity=100,
                               rotate=ft.transform.Rotate(angle=0, alignment=ft.alignment.center))
    set_sabado2 = ft.IconButton(icon=ft.icons.ARROW_RIGHT, icon_color=verde1, on_click=Sabado2,
                                animate_offset=ft.animation.Animation(duration=700), animate_opacity=100,
                                rotate=ft.transform.Rotate(angle=0, alignment=ft.alignment.center))
    set_domingo2 = ft.IconButton(icon=ft.icons.ARROW_RIGHT, icon_color=verde1, on_click=Domingo2,
                                 animate_offset=ft.animation.Animation(duration=700), animate_opacity=100,
                                 rotate=ft.transform.Rotate(angle=0, alignment=ft.alignment.center))

    setas2 = ft.Row(
        offset=ft.transform.Offset(-0.025, -2.6),
        spacing=1.7,
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            set_segunda2,
            set_terca2,
            set_quarta2,
            set_quinta2,
            set_sexta2,
            set_sabado2,
            set_domingo2,
        ],
    )

    # CLIMA

    icon_aquecer = ft.Icon(name=ft.icons.SUNNY, color=branco2, size=50, visible=True,
                           offset=ft.transform.Offset(0, 0))
    text_termometro = ft.Text(value='Aquecendo a gaiola', color=branco2, bgcolor=verde1, size=18, visible=True,
                              offset=ft.transform.Offset(0.05, 0))

    botao_parar_aquecimento = ft.ElevatedButton(text='Parar aquecimento', height=30, width=200, color=verde1,
                                                bgcolor=branco2, on_click=retira_termometro,
                                                offset=ft.transform.Offset(0.25, -0.1), visible=True)
    Text_field_temperatura = ft.TextField(border_radius=15, width=250, border_color=verde1, label='Ex:20.5',
                                          helper_text='Temperatura máxima 27°', color=verde2, cursor_color=verde2)
    Send_button = ft.IconButton(icon=ft.icons.SEND_SHARP, icon_size=35, offset=ft.transform.Offset(0, -0.2),
                                on_click=adiciona_termometro, icon_color=verde2)

    TF_temp = ft.Text(value='0', size=30, color='#ff8800', offset=ft.transform.Offset(-1.7, 0))
    TF_umidade = ft.Text(value='0', size=30, color='#0096c7', offset=ft.transform.Offset(-1.7, 0))

    ProgressRingTemp = ft.ProgressRing(width=130, height=130, color='#ff8800', bgcolor=branco2, stroke_width=13)
    ProgressRingUmid = ft.ProgressRing(width=130, height=130, color='#0096c7', bgcolor=branco2, stroke_width=13)

    IconTemp = ft.ElevatedButton(icon=ft.icons.THERMOSTAT, text='Temperatura', color=branco2,
                                 bgcolor='#ff8800', offset=ft.transform.Offset(0, 0.2))
    IconUmid = ft.ElevatedButton(icon=ft.icons.CLOUD, text='Umidade', color=branco2, bgcolor='#0096c7',
                                 offset=ft.transform.Offset(0, -0.2))

    temperatura = ft.Column(
        spacing=35,
        controls=[
            IconTemp,
            ft.Row(controls=[ProgressRingTemp, TF_temp], offset=ft.transform.Offset(0.31, 0)),
            LinhaVerde,
            IconUmid,
            ft.Row(controls=[ProgressRingUmid, TF_umidade], offset=ft.transform.Offset(0.31, -0.3)),
        ]
    )

    ContainerEsquentando = ft.Container(
        padding=5,
        bgcolor=verde1,
        border_radius=15,
        visible=False,
        content=ft.Column(
            spacing=10,
            controls=[ft.Row(
                spacing=0,
                controls=[icon_aquecer, ft.Column(controls=[text_termometro, botao_parar_aquecimento])],
            ),
            ]
        )
    )

    InputTemp = ft.Column(
        spacing=35,
        controls=[
            ft.Text("Digite a temperatura desejada", color=verde2, size=20, text_align=ft.alignment.top_center),
            ft.Row(
                controls=[Text_field_temperatura, Send_button],
            ),
            LinhaVerde,
            ContainerEsquentando,
        ],
    )

    # CLIMA
    clima_content = ft.Tabs(
        label_color=verde2,
        indicator_color=verde2,
        selected_index=0,
        expand=1,
        animation_duration=300,
        on_change=Restaurar_termometro,
        tabs=[
            ft.Tab(
                text='Medições',
                content=temperatura,
            ),
            ft.Tab(
                text='Aquecimento',
                content=InputTemp,
            ),
        ]
    )

    # MONITORAMENTO

    line1_mon = ft.Container(
        height=45,
        border_radius=ft.border_radius.all(10),
        bgcolor=branco2,
        shadow=ft.BoxShadow(
            color=branco2,
            blur_style=ft.ShadowBlurStyle.NORMAL,
        ),
        content=ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[
            ft.Text('Monitoramento', color=verde2, size=20),
                ]
           )
    )


    img1 = ft.Container(
        visible=True,
        content=ft.Image(
        src=f"https://firebasestorage.googleapis.com/v0/b/gaia-f6d06.appspot.com/o/LiveImage.jpg?alt=media&token=314018f0-4e53-478c-9dc7-2209e4a99e61",
        width=365,
        height=365,

        fit=ft.ImageFit.CONTAIN,
        )
    )

    img2 = ft.Container(
        visible=False,
        content=ft.Image(
        src=f"https://firebasestorage.googleapis.com/v0/b/gaia-f6d06.appspot.com/o/LiveImage.jpg?alt=media&token=314018f0-4e53-478c-9dc7-2209e4a99e61",
        width=365,
        height=365,

        fit=ft.ImageFit.CONTAIN,
        offset=ft.transform.Offset(-1.03,0)
        )
    )

    # ALIMENTAÇÃO
    alimentacao_content = ft.Container(
        expand=True,
        bgcolor=branco1,
        content=ft.Column(
            controls=[
                line1_ali,
                line2_ali,
                Selecao_do_tipo_comida,
                LinhaVerde,
                dias_da_semana_ali1,
                dias_da_semana_ali2,
                setas2,
                Seg_ali,
                Ter_ali,
                Qua_ali,
                Qui_ali,
                Sex_ali,
                Sab_ali,
                Dom_ali,
                pb,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=26,
            scroll=ft.ScrollMode.AUTO
        ),
    )
    # MONITORAMENTO
    monitoramento_content = ft.Column(
        controls=[
            line1_mon,
            ft.Row(controls=[img1, img2]),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=50,
    )

    # Cortinas
    cortinas_content = ft.Column(
        controls=[
            Texto1_cortina,
            Texto2_cortina,
            LinhaVerde,
            dias_da_semana1,
            dias_da_semana2,
            setas_cor1,
            setas_cor2,
            Seg_cor,
            Ter_cor,
            Qua_cor,
            Qui_cor,
            Sex_cor,
            Sab_cor,
            Dom_cor,

        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=26,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
    # SAFE-AREA
    ft.SafeArea(
        content=cortinas_content
    )
    ft.SafeArea(
        content=alimentacao_content
    )
    ft.SafeArea(
        content=clima_content
    )
    ft.SafeArea(
        content=monitoramento_content
    )

    def change_page(e):
        selected_index = int(e.control.selected_index)
        page.controls.clear()  # Limpa o conteúdo atual
        if selected_index == 0:
            page.controls.append(alimentacao_content)
            MudarCor()
            RestaurarComida(e=True)
            RestaurarHorarioAlimentar(e=True)
        elif selected_index == 1:
            page.controls.append(clima_content)
        elif selected_index == 2:
            page.controls.append(monitoramento_content)
        elif selected_index == 3:
            page.controls.append(cortinas_content)
            LerDados()
            MudarCor()
            RestaurarHorarioCortinas(e=True)
            Lendo_Firebase(Now=True)
        page.update()

    page.navigation_bar = ft.CupertinoNavigationBar(
        bgcolor=verde1,
        inactive_color=branco2,
        active_color=ft.colors.BLACK,
        on_change=change_page,
        destinations=[
            ft.NavigationDestination(icon=ft.icons.FOOD_BANK_SHARP, label="Alimentação"),
            ft.NavigationDestination(icon=ft.icons.CLOUD, label="Clima"),
            ft.NavigationDestination(icon=ft.icons.CAMERA_ALT, label="Monitoramento"),
            ft.NavigationDestination(icon=ft.icons.CURTAINS_ROUNDED, label="Cortinas"),
        ],
    )

    # Inicia na página inicial (Monitoramento)
    page.controls.append(alimentacao_content)

    MudarCor()
    RestaurarHorarioAlimentar(e=True)
    RestaurarComida(e=True)

    page.update()


ft.app(main)