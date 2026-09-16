import pygame
import sys
import os
import math
import random

pygame.init()

try:
    pygame.mixer.init()
except:
    pass

LARGURA = 1100
ALTURA = 700

tela = pygame.display.set_mode((LARGURA, ALTURA))

pygame.display.set_caption(
    "Detetive Sanitário"
)

clock = pygame.time.Clock()

FPS = 60

BRANCO = (255, 255, 255)
PRETO = (20, 20, 20)

CINZA = (170, 170, 170)
CINZA_ESCURO = (70, 70, 70)

VERDE = (55, 180, 90)
VERDE_CLARO = (120, 220, 140)

VERMELHO = (210, 60, 60)
VERMELHO_CLARO = (245, 130, 130)

AZUL = (55, 120, 210)
AZUL_ESCURO = (35, 75, 145)

AMARELO = (240, 200, 60)

BEGE = (239, 233, 216)

MARROM = (130, 80, 40)

ROXO = (105, 75, 165)

fonte_pequena = pygame.font.Font(None, 24)
fonte = pygame.font.Font(None, 30)
fonte_media = pygame.font.Font(None, 36)
fonte_titulo = pygame.font.Font(None, 52)
fonte_grande = pygame.font.Font(None, 72)

PASTA_ASSETS = "assets"


def caminho(nome):
    return os.path.join(
        PASTA_ASSETS,
        nome
    )


def carregar_imagem(nome, tamanho=None):
    try:
        imagem = pygame.image.load(
            caminho(nome)
        ).convert_alpha()

        if tamanho:
            imagem = pygame.transform.smoothscale(
                imagem,
                tamanho
            )

        return imagem

    except:
        return None


def carregar_som(nome):
    try:
        return pygame.mixer.Sound(
            caminho(nome)
        )

    except:
        return None


imagem_cozinha = carregar_imagem(
    "cozinha.png",
    (1100, 700)
)

imagem_fiscal = carregar_imagem(
    "fiscal.png",
    (120, 160)
)

imagem_lupa = carregar_imagem(
    "cursor.png",
    (50, 50)
)

imagem_tabua = carregar_imagem(
    "tabua.png",
    (120, 60)
)

imagem_lixeira = carregar_imagem(
    "lixeira.png",
    (80, 100)
)

imagem_alimento = carregar_imagem(
    "alimento.png",
    (100, 70)
)

som_clique = carregar_som(
    "clique.wav"
)

som_correto = carregar_som(
    "correto.wav"
)

som_errado = carregar_som(
    "errado.wav"
)

som_final = carregar_som(
    "final.wav"
)


def tocar_som(som):
    if som:
        som.play()


try:
    pygame.mixer.music.load(
        caminho("musica_menu.wav")
    )

    pygame.mixer.music.set_volume(
        0.25
    )

except:
    pass


estado = "menu"

vidas = 3
pontuacao = 0
inspecoes_realizadas = 0
item_selecionado = None
mensagem = ""
mensagem_cor = BRANCO
tempo_mensagem = 0
tempo_resultado = 0
resposta_escolhida = None
mouse_sobre_item = None

situacoes = [

    {
        "id": 1,
        "nome": "Lixeira",
        "rect": pygame.Rect(
            760, 440, 80, 100
        ),
        "imagem": imagem_lixeira,
        "texto":
        "Você encontrou um recipiente de lixo na área de "
        "manipulação. Ele possui tampa, mas precisa ser "
        "aberto manualmente.",
        "resposta": 2,
        "justificativa":
        "Na área de manipulação de alimentos, os resíduos "
        "devem ser acondicionados em recipientes com tampa "
        "acionada por pedal, evitando contato manual.",
        "base":
        "CVS 3/2026 — Artigo 129."
    },

    {
        "id": 2,
        "nome": "Janela",
        "rect": pygame.Rect(
            180, 120, 130, 150
        ),
        "imagem": None,
        "texto":
        "A janela possui acabamento liso, está ajustada ao "
        "batente e possui tela milimétrica removível para "
        "facilitar a limpeza.",
        "resposta": 1,
        "justificativa":
        "Janelas e outras aberturas devem possuir acabamento "
        "adequado, ser de fácil limpeza e contar com telas "
        "milimétricas removíveis.",
        "base":
        "CVS 3/2026 — Artigo 160."
    },

    {
        "id": 3,
        "nome": "Piso",
        "rect": pygame.Rect(
            420, 540, 180, 80
        ),
        "imagem": None,
        "texto":
        "Durante a inspeção, você observa que o piso apresenta "
        "uma trinca próxima à área de manipulação.",
        "resposta": 2,
        "justificativa":
        "O piso deve permanecer íntegro, sem trincas, "
        "vazamentos ou infiltrações.",
        "base":
        "CVS 3/2026 — Artigo 153."
    },

    {
        "id": 4,
        "nome": "Parede",
        "rect": pygame.Rect(
            500, 120, 150, 180
        ),
        "imagem": None,
        "texto":
        "A parede apresenta uma pequena área com umidade "
        "e sinais de bolor.",
        "resposta": 2,
        "justificativa":
        "Paredes, divisórias, tetos e forros devem ser livres "
        "de umidade, bolores, infiltrações, rachaduras e "
        "outras irregularidades.",
        "base":
        "CVS 3/2026 — Artigo 157."
    },

    {
        "id": 5,
        "nome": "Porta",
        "rect": pygame.Rect(
            900, 170, 120, 230
        ),
        "imagem": None,
        "texto":
        "A porta de entrada da área de manipulação não possui "
        "mecanismo de fechamento automático.",
        "resposta": 2,
        "justificativa":
        "Portas de entrada para áreas de armazenamento e "
        "manipulação devem possuir mecanismos de fechamento "
        "automático e proteção contra vetores e pragas.",
        "base":
        "CVS 3/2026 — Artigo 158."
    },

    {
        "id": 6,
        "nome": "Botijão de gás",
        "rect": pygame.Rect(
            40, 410, 120, 120
        ),
        "imagem": None,
        "texto":
        "O botijão de gás está armazenado em uma área exclusiva, "
        "ventilada e protegida contra o acesso de pessoas não "
        "autorizadas.",
        "resposta": 1,
        "justificativa":
        "A área destinada ao armazenamento de botijões de GLP "
        "deve ser exclusiva, ventilada e protegida contra "
        "acesso não autorizado.",
        "base":
        "CVS 3/2026 — Artigo 133."
    },

    {
        "id": 7,
        "nome": "Fiação elétrica",
        "rect": pygame.Rect(
            350, 100, 100, 180
        ),
        "imagem": None,
        "texto":
        "Você observa uma fiação elétrica solta passando sobre "
        "a zona de manipulação de alimentos.",
        "resposta": 2,
        "justificativa":
        "Não é permitida fiação elétrica solta sobre a zona "
        "de manipulação de alimentos.",
        "base":
        "Portaria 326/1997 — item 5.3.17."
    },

    {
        "id": 8,
        "nome": "Armazenamento",
        "rect": pygame.Rect(
            680, 160, 150, 160
        ),
        "imagem": None,
        "texto":
        "Os produtos estão organizados de maneira a permitir "
        "espaço suficiente para circulação, limpeza e realização "
        "adequada das operações.",
        "resposta": 1,
        "justificativa":
        "Devem existir espaços suficientes para atender "
        "adequadamente a todas as operações realizadas no "
        "estabelecimento.",
        "base":
        "Portaria 326/1997 — item 5.3.2."
    },

    {
        "id": 9,
        "nome": "Estrutura elevada",
        "rect": pygame.Rect(
            500, 300, 160, 70
        ),
        "imagem": None,
        "texto":
        "Existe uma estrutura elevada sobre a área de "
        "manipulação que apresenta condensação e possibilidade "
        "de gotejamento sobre os alimentos.",
        "resposta": 2,
        "justificativa":
        "Estruturas e acessórios elevados devem evitar "
        "contaminação direta ou indireta dos alimentos por "
        "gotejamento ou condensação.",
        "base":
        "Portaria 326/1997 — item 5.3.8."
    },

    {
        "id": 10,
        "nome": "Banheiro",
        "rect": pygame.Rect(
            930, 430, 100, 100
        ),
        "imagem": None,
        "texto":
        "O banheiro possui acesso direto para a área onde "
        "os alimentos são manipulados.",
        "resposta": 2,
        "justificativa":
        "Banheiros, lavabos e vestiários devem estar completamente "
        "separados dos locais de manipulação e não possuir acesso "
        "direto ou comunicação com essas áreas.",
        "base":
        "Portaria 326/1997 — item 5.3.10."
    },

    {
        "id": 11,
        "nome": "Ventilação",
        "rect": pygame.Rect(
            300, 300, 100, 100
        ),
        "imagem": None,
        "texto":
        "A ventilação da cozinha é adequada e mantém o ambiente "
        "livre de fumaça, gases, partículas e condensação que "
        "possam comprometer a qualidade dos alimentos.",
        "resposta": 1,
        "justificativa":
        "A ventilação deve garantir renovação do ar e manter "
        "o ambiente livre de elementos que possam comprometer "
        "a qualidade higiênico-sanitária dos alimentos.",
        "base":
        "RDC 216/2004 — item 4.1.10."
    },

    {
        "id": 12,
        "nome": "Caixa de gordura",
        "rect": pygame.Rect(
            80, 540, 120, 80
        ),
        "imagem": None,
        "texto":
        "Durante a inspeção, você verifica que a caixa de gordura "
        "está localizada dentro da área de preparação de alimentos.",
        "resposta": 2,
        "justificativa":
        "Caixas de gordura e de esgoto devem estar localizadas "
        "fora das áreas de preparação e armazenamento de alimentos.",
        "base":
        "RDC 216/2004 — item 4.1.6."
    },

    {
        "id": 13,
        "nome": "Equipamentos",
        "rect": pygame.Rect(
            650, 350, 120, 80
        ),
        "imagem": None,
        "texto":
        "Os equipamentos e móveis estão organizados de acordo "
        "com o fluxo operacional, facilitando o acesso e a "
        "eficiência das operações.",
        "resposta": 1,
        "justificativa":
        "A disposição dos equipamentos e móveis deve seguir "
        "o fluxo operacional, garantindo segurança dos alimentos "
        "e facilitando as operações.",
        "base":
        "CVS 3/2026 — Artigo 147."
    },

    {
        "id": 14,
        "nome": "Obra",
        "rect": pygame.Rect(
            850, 80, 180, 100
        ),
        "imagem": None,
        "texto":
        "Uma pequena obra está acontecendo no estabelecimento. "
        "A área em reforma está completamente isolada das áreas "
        "de manipulação e armazenamento e os alimentos estão "
        "devidamente protegidos.",
        "resposta": 1,
        "justificativa":
        "Obras durante o funcionamento são permitidas desde que "
        "haja completo isolamento da área em reforma e proteção "
        "dos alimentos, equipamentos, utensílios e embalagens.",
        "base":
        "CVS 3/2026 — Artigo 139."
    },

    {
        "id": 15,
        "nome": "Armazenamento de lixo",
        "rect": pygame.Rect(
            850, 540, 150, 80
        ),
        "imagem": None,
        "texto":
        "Os resíduos estão armazenados de maneira que permite "
        "o ingresso de pragas e pode favorecer a contaminação "
        "dos alimentos.",
        "resposta": 2,
        "justificativa":
        "O armazenamento de lixo e materiais não comestíveis "
        "deve impedir o ingresso de pragas e evitar contaminações.",
        "base":
        "Portaria 326/1997 — item 5.3.19."
    }

]


def texto(
    mensagem,
    x,
    y,
    cor=PRETO,
    fonte_usada=fonte,
    centro=False
):

    imagem = fonte_usada.render(
        mensagem,
        True,
        cor
    )

    if centro:
        x -= imagem.get_width() // 2

    tela.blit(
        imagem,
        (x, y)
    )


def desenhar_texto_quebrado(
    mensagem,
    rect,
    fonte_usada,
    cor,
    espaco=5
):

    palavras = mensagem.split(" ")

    linhas = []

    linha_atual = ""

    for palavra in palavras:

        teste = linha_atual

        if teste:
            teste += " "

        teste += palavra

        if fonte_usada.size(teste)[0] <= rect.width:

            linha_atual = teste

        else:

            linhas.append(
                linha_atual
            )

            linha_atual = palavra

    if linha_atual:

        linhas.append(
            linha_atual
        )

    y = rect.y

    for linha in linhas:

        texto(
            linha,
            rect.x,
            y,
            cor,
            fonte_usada
        )

        y += fonte_usada.get_height() + espaco


def botao(
    mensagem,
    rect,
    cor,
    cor_texto=BRANCO
):

    mouse = pygame.mouse.get_pos()

    cor_atual = cor

    if rect.collidepoint(mouse):

        cor_atual = tuple(
            min(c + 20, 255)
            for c in cor
        )

    pygame.draw.rect(
        tela,
        cor_atual,
        rect,
        border_radius=12
    )

    texto(
        mensagem,
        rect.centerx,
        rect.centery - 15,
        cor_texto,
        fonte,
        True
    )


def desenhar_menu():

    tela.fill(BEGE)

    pygame.draw.rect(
        tela,
        AZUL_ESCURO,
        (0, 0, LARGURA, 15)
    )

    pygame.draw.rect(
        tela,
        AZUL_ESCURO,
        (0, ALTURA - 15, LARGURA, 15)
    )

    texto(
        "DETETIVE",
        LARGURA // 2,
        100,
        PRETO,
        fonte_grande,
        True
    )

    texto(
        "SANITÁRIO",
        LARGURA // 2,
        175,
        AZUL,
        fonte_grande,
        True
    )

    if imagem_fiscal:

        tela.blit(
            imagem_fiscal,
            (
                LARGURA // 2 - 60,
                260
            )
        )

    else:

        pygame.draw.circle(
            tela,
            BEGE,
            (LARGURA // 2, 300),
            40
        )

        pygame.draw.rect(
            tela,
            AZUL,
            (
                LARGURA // 2 - 40,
                340,
                80,
                100
            ),
            border_radius=10
        )

    botao_jogar = pygame.Rect(
        350,
        480,
        400,
        65
    )

    botao(
        "INICIAR INSPEÇÃO",
        botao_jogar,
        VERDE
    )

    texto(
        "Encontre e classifique as situações da cozinha.",
        LARGURA // 2,
        590,
        CINZA_ESCURO,
        fonte,
        True
    )


def desenhar_instrucoes():

    tela.fill(BEGE)

    texto(
        "COMO JOGAR",
        LARGURA // 2,
        60,
        AZUL,
        fonte_titulo,
        True
    )

    instrucoes = [
        "Você acabou de entrar em uma cozinha para",
        "realizar uma inspeção sanitária.",
        "",
        "Clique nos elementos da cozinha para investigá-los.",
        "",
        "Depois classifique cada situação:",
        "",
        "1 - Conforme",
        "2 - Não conforme",
        "3 - Não observado",
        "4 - Não aplicável",
        "",
        "Você possui 3 vidas.",
        "Errou uma classificação? Perde uma vida.",
        "",
        "Encontre e analise todas as situações."
    ]

    y = 130

    for linha in instrucoes:

        texto(
            linha,
            LARGURA // 2,
            y,
            PRETO,
            fonte,
            True
        )

        y += 28

    botao_continuar = pygame.Rect(
        400,
        590,
        300,
        55
    )

    botao(
        "ENTENDI!",
        botao_continuar,
        VERDE
    )


def desenhar_cozinha():

    if imagem_cozinha:

        tela.blit(
            imagem_cozinha,
            (0, 0)
        )

    else:

        tela.fill(BEGE)

        pygame.draw.rect(
            tela,
            (245, 240, 225),
            (0, 0, 1100, 530)
        )

        pygame.draw.rect(
            tela,
            (185, 185, 180),
            (0, 530, 1100, 170)
        )

        pygame.draw.rect(
            tela,
            MARROM,
            (60, 370, 850, 55)
        )

        pygame.draw.rect(
            tela,
            (150, 100, 60),
            (60, 425, 850, 105)
        )

        pygame.draw.rect(
            tela,
            CINZA,
            (300, 375, 130, 50)
        )

        pygame.draw.rect(
            tela,
            BRANCO,
            (320, 385, 90, 30)
        )

        pygame.draw.rect(
            tela,
            CINZA_ESCURO,
            (520, 330, 150, 95)
        )

        pygame.draw.circle(
            tela,
            PRETO,
            (560, 360),
            18
        )

        pygame.draw.circle(
            tela,
            PRETO,
            (630, 360),
            18
        )

        pygame.draw.rect(
            tela,
            BRANCO,
            (930, 150, 120, 270)
        )

        pygame.draw.line(
            tela,
            CINZA,
            (930, 270),
            (1050, 270),
            3
        )

        pygame.draw.rect(
            tela,
            AZUL,
            (180, 120, 130, 150),
            5
        )

        pygame.draw.line(
            tela,
            AZUL,
            (245, 120),
            (245, 270),
            4
        )

        pygame.draw.line(
            tela,
            AZUL,
            (180, 195),
            (310, 195),
            4
        )

        pygame.draw.rect(
            tela,
            MARROM,
            (900, 170, 120, 250)
        )

        pygame.draw.rect(
            tela,
            BRANCO,
            (50, 430, 70, 100),
            border_radius=15
        )

        pygame.draw.rect(
            tela,
            MARROM,
            (680, 160, 150, 15)
        )

        pygame.draw.rect(
            tela,
            MARROM,
            (680, 240, 150, 15)
        )

    mouse = pygame.mouse.get_pos()

    mouse_sobre_item = None

    for item in situacoes:

        if item["id"] in inspecoes_concluidas:

            pygame.draw.rect(
                tela,
                VERDE,
                item["rect"].inflate(8, 8),
                3,
                border_radius=5
            )

            continue

        if item["rect"].collidepoint(mouse):

            mouse_sobre_item = item

            pulsacao = int(
                4 + 2 * math.sin(
                    pygame.time.get_ticks() / 150
                )
            )

            destaque = item[
                "rect"
            ].inflate(
                pulsacao,
                pulsacao
            )

            pygame.draw.rect(
                tela,
                AMARELO,
                destaque,
                4,
                border_radius=8
            )

    if imagem_tabua:

        tela.blit(
            imagem_tabua,
            (120, 330)
        )

    else:

        pygame.draw.rect(
            tela,
            MARROM,
            (120, 330, 120, 60)
        )

    if imagem_alimento:

        tela.blit(
            imagem_alimento,
            (450, 285)
        )

    else:

        pygame.draw.rect(
            tela,
            AMARELO,
            (450, 285, 100, 70)
        )

    pygame.draw.rect(
        tela,
        PRETO,
        (0, 0, LARGURA, 65)
    )

    texto(
        "DETETIVE SANITÁRIO",
        25,
        18,
        BRANCO,
        fonte
    )

    texto(
        f"VIDAS: {vidas}",
        470,
        18,
        VERMELHO,
        fonte
    )

    texto(
        f"PONTOS: {pontuacao}",
        620,
        18,
        AMARELO,
        fonte
    )

    texto(
        f"INSPEÇÕES: {inspecoes_realizadas}/{len(situacoes)}",
        800,
        18,
        BRANCO,
        fonte_pequena
    )

    if mouse_sobre_item:

        caixa = pygame.Rect(
            mouse[0] + 15,
            mouse[1] + 15,
            190,
            40
        )

        if caixa.right > LARGURA:

            caixa.x = mouse[0] - 205

        pygame.draw.rect(
            tela,
            PRETO,
            caixa,
            border_radius=8
        )

        texto(
            "🔎 INSPECIONAR",
            caixa.x + 15,
            caixa.y + 10,
            BRANCO,
            fonte_pequena
        )


inspecoes_concluidas = set()


def desenhar_pergunta(item):

    desenhar_cozinha()

    sombra = pygame.Surface(
        (LARGURA, ALTURA)
    )

    sombra.set_alpha(185)

    sombra.fill(PRETO)

    tela.blit(
        sombra,
        (0, 0)
    )

    caixa = pygame.Rect(
        100,
        70,
        900,
        560
    )

    pygame.draw.rect(
        tela,
        BRANCO,
        caixa,
        border_radius=18
    )

    pygame.draw.rect(
        tela,
        AZUL,
        caixa,
        5,
        border_radius=18
    )

    texto(
        "🔎 SITUAÇÃO ENCONTRADA",
        550,
        105,
        AZUL,
        fonte_titulo,
        True
    )

    area_texto = pygame.Rect(
        150,
        175,
        800,
        100
    )

    desenhar_texto_quebrado(
        item["texto"],
        area_texto,
        fonte,
        PRETO
    )

    opcoes = [
        "1 — Conforme",
        "2 — Não conforme",
        "3 — Não observado",
        "4 — Não aplicável"
    ]

    y = 310

    for opcao in opcoes:

        texto(
            opcao,
            180,
            y,
            PRETO,
            fonte_media
        )

        y += 55

    texto(
        "Digite o número da classificação:",
        180,
        535,
        AZUL_ESCURO,
        fonte
    )


def desenhar_resultado():

    tela.fill(BEGE)

    if resposta_escolhida == item_selecionado["resposta"]:

        cor = VERDE

        titulo = "✓ CORRETO!"

        texto_titulo = titulo

    else:

        cor = VERMELHO

        texto_titulo = "✕ CLASSIFICAÇÃO INCORRETA"

    texto(
        texto_titulo,
        LARGURA // 2,
        70,
        cor,
        fonte_titulo,
        True
    )

    if item_selecionado["resposta"] == 1:
        resposta_correta = "CONFORME"

    elif item_selecionado["resposta"] == 2:
        resposta_correta = "NÃO CONFORME"

    elif item_selecionado["resposta"] == 3:
        resposta_correta = "NÃO OBSERVADO"

    else:
        resposta_correta = "NÃO APLICÁVEL"

    texto(
        f"Classificação correta: {resposta_correta}",
        LARGURA // 2,
        150,
        PRETO,
        fonte_media,
        True
    )

    texto(
        "JUSTIFICATIVA",
        LARGURA // 2,
        220,
        AZUL,
        fonte_titulo,
        True
    )

    area = pygame.Rect(
        150,
        275,
        800,
        120
    )

    desenhar_texto_quebrado(
        item_selecionado["justificativa"],
        area,
        fonte,
        PRETO
    )

    pygame.draw.rect(
        tela,
        AZUL_ESCURO,
        (150, 430, 800, 75),
        border_radius=10
    )

    texto(
        item_selecionado["base"],
        LARGURA // 2,
        455,
        BRANCO,
        fonte,
        True
    )

    texto(
        "Clique para continuar",
        LARGURA // 2,
        565,
        CINZA_ESCURO,
        fonte,
        True
    )


def desenhar_final():

    tela.fill(BEGE)

    escala = 1 + (
        0.02 *
        math.sin(
            pygame.time.get_ticks() / 200
        )
    )

    if vidas > 0:

        texto(
            "INSPEÇÃO",
            LARGURA // 2,
            100,
            PRETO,
            fonte_grande,
            True
        )

        texto(
            "CONCLUÍDA!",
            LARGURA // 2,
            180,
            VERDE,
            fonte_grande,
            True
        )

        texto(
            "RESTAURANTE ABERTO",
            LARGURA // 2,
            285,
            VERDE,
            fonte_titulo,
            True
        )

        texto(
            f"Pontuação final: {pontuacao}",
            LARGURA // 2,
            355,
            PRETO,
            fonte_media,
            True
        )

        texto(
            f"Vidas restantes: {vidas}",
            LARGURA // 2,
            400,
            PRETO,
            fonte,
            True
        )

    else:

        texto(
            "INSPEÇÃO",
            LARGURA // 2,
            100,
            PRETO,
            fonte_grande,
            True
        )

        texto(
            "INTERROMPIDA",
            LARGURA // 2,
            180,
            VERMELHO,
            fonte_grande,
            True
        )

        texto(
            "RESTAURANTE FECHADO",
            LARGURA // 2,
            285,
            VERMELHO,
            fonte_titulo,
            True
        )

        texto(
            "Você perdeu todas as suas vidas.",
            LARGURA // 2,
            355,
            PRETO,
            fonte_media,
            True
        )

        texto(
            f"Pontuação: {pontuacao}",
            LARGURA // 2,
            400,
            PRETO,
            fonte,
            True
        )

    botao_novo = pygame.Rect(
        350,
        500,
        400,
        65
    )

    botao(
        "NOVA INSPEÇÃO",
        botao_novo,
        AZUL
    )


def desenhar_cursor():

    pos = pygame.mouse.get_pos()

    if imagem_lupa:

        tela.blit(
            imagem_lupa,
            (
                pos[0] - 10,
                pos[1] - 10
            )
        )

    else:

        pygame.draw.circle(
            tela,
            AMARELO,
            pos,
            16,
            3
        )

        pygame.draw.line(
            tela,
            AMARELO,
            (
                pos[0] - 22,
                pos[1]
            ),
            (
                pos[0] + 22,
                pos[1]
            ),
            3
        )

        pygame.draw.line(
            tela,
            AMARELO,
            (
                pos[0],
                pos[1] - 22
            ),
            (
                pos[0],
                pos[1] + 22
            ),
            3
        )


def resetar_jogo():

    global vidas
    global pontuacao
    global inspecoes_realizadas
    global item_selecionado
    global resposta_escolhida
    global mensagem

    vidas = 3

    pontuacao = 0

    inspecoes_realizadas = 0

    item_selecionado = None

    resposta_escolhida = None

    mensagem = ""

    inspecoes_concluidas.clear()


rodando = True

pygame.mouse.set_visible(False)


while rodando:

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:

            rodando = False

        if estado == "menu":

            if evento.type == pygame.MOUSEBUTTONDOWN:

                pos = evento.pos

                botao_jogar = pygame.Rect(
                    350,
                    480,
                    400,
                    65
                )

                if botao_jogar.collidepoint(pos):

                    tocar_som(som_clique)

                    estado = "instrucoes"

        elif estado == "instrucoes":

            if evento.type == pygame.MOUSEBUTTONDOWN:

                pos = evento.pos

                botao_continuar = pygame.Rect(
                    400,
                    590,
                    300,
                    55
                )

                if botao_continuar.collidepoint(pos):

                    tocar_som(som_clique)

                    resetar_jogo()

                    estado = "jogo"

        elif estado == "jogo":

            if evento.type == pygame.MOUSEBUTTONDOWN:

                pos = evento.pos

                for item in situacoes:

                    if item["id"] in inspecoes_concluidas:
                        continue

                    if item["rect"].collidepoint(pos):

                        tocar_som(
                            som_clique
                        )

                        item_selecionado = item

                        estado = "pergunta"

                        break

        elif estado == "pergunta":

            if evento.type == pygame.KEYDOWN:

                resposta = None

                if evento.key == pygame.K_1:
                    resposta = 1

                elif evento.key == pygame.K_2:
                    resposta = 2

                elif evento.key == pygame.K_3:
                    resposta = 3

                elif evento.key == pygame.K_4:
                    resposta = 4

                if resposta is not None:

                    resposta_escolhida = resposta

                    inspecoes_realizadas += 1

                    inspecoes_concluidas.add(
                        item_selecionado["id"]
                    )

                    if (
                        resposta
                        ==
                        item_selecionado["resposta"]
                    ):

                        tocar_som(
                            som_correto
                        )

                        pontuacao += 100

                    else:

                        tocar_som(
                            som_errado
                        )

                        vidas -= 1

                    estado = "resultado"

                    tempo_resultado = (
                        pygame.time.get_ticks()
                    )

        elif estado == "resultado":

            if evento.type == pygame.MOUSEBUTTONDOWN:

                if vidas <= 0:

                    tocar_som(
                        som_final
                    )

                    estado = "final"

                elif (
                    inspecoes_realizadas
                    >=
                    len(situacoes)
                ):

                    tocar_som(
                        som_final
                    )

                    estado = "final"

                else:

                    estado = "jogo"

        elif estado == "final":

            if evento.type == pygame.MOUSEBUTTONDOWN:

                pos = evento.pos

                botao_novo = pygame.Rect(
                    350,
                    500,
                    400,
                    65
                )

                if botao_novo.collidepoint(pos):

                    tocar_som(
                        som_clique
                    )

                    resetar_jogo()

                    estado = "jogo"

        if evento.type == pygame.KEYDOWN:

            if evento.key == pygame.K_ESCAPE:

                rodando = False

    if estado == "menu":

        desenhar_menu()

    elif estado == "instrucoes":

        desenhar_instrucoes()

    elif estado == "jogo":

        desenhar_cozinha()

    elif estado == "pergunta":

        desenhar_pergunta(
            item_selecionado
        )

    elif estado == "resultado":

        desenhar_resultado()

    elif estado == "final":

        desenhar_final()

    desenhar_cursor()

    pygame.display.flip()

    clock.tick(FPS)


pygame.quit()

sys.exit()