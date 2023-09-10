from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as django_login
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from app_frutas_sys.models import ItemPedido
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from app_frutas_sys.models import Pedido
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.template.loader import get_template
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.platypus import Paragraph,Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle




styles = getSampleStyleSheet()





def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            django_login(request, user)
            messages.success(request, 'Login bem-sucedido.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuário ou senha incorretos. Tente novamente.')

    return render(request, 'usuarios/login.html')

@login_required
def dashboard(request):
    pedidos_dashboard = Pedido.objects.all()
    return render(request, 'usuarios/dashboard.html', {'pedidos_dashboard': pedidos_dashboard})

def criar_pedido(request):
    if request.method == 'POST':
        pedido = Pedido.objects.create()  # Crie um novo pedido

        tipos_itens = request.POST.getlist('tipo_item[]')
        quantidades_itens = request.POST.getlist('quantidade_item[]')

        for i in range(len(tipos_itens)):
            tipo_item = tipos_itens[i]
            quantidade_item = quantidades_itens[i]

            item_pedido = ItemPedido.objects.create(
                pedido=pedido,
                tipo=tipo_item,
                quantidade=quantidade_item
            )

        return render(request, 'sucesso.html', {'pedido': pedido, 'itens_pedido': pedido.itempedido_set.all()})
    
    return render(request, 'criar_pedido.html')
@login_required
def formulario_criar_pedido(request):
    return render(request, 'criar_pedido.html')


@login_required
def adicionar_pedido_dashboard(request, pedido_id):
    try:
        pedido = Pedido.objects.get(pk=pedido_id)

        # Obtenha a data atual
        data_atual = datetime.now().date()

        # Crie um objeto PedidoDashboard com base no pedido concluído e preencha a data
        pedido_dashboard = pedido(nome_pedido=pedido.nome, status='Concluído')

        pedido_dashboard.save()
        
        messages.success(request, 'Pedido adicionado ao dashboard com sucesso.')

        # Após adicionar o pedido ao dashboard, você pode redirecionar o usuário de volta à página do dashboard.
        return redirect('dashboard')
    except Pedido.DoesNotExist:
        messages.error(request, 'Pedido não encontrado.')
        return redirect('dashboard')


@login_required
def ver_pedido_detalhes(request, pedido_id):
    pedido = Pedido.objects.get(id=pedido_id)
    itens = ItemPedido.objects.filter(pedido=pedido)

    context = {
        'pedido': pedido,
        'itens': itens,
    }

    return render(request, 'ver_pedido_detalhes.html', context)

def concluir_pedido(request, pedido_id):
    if request.method == "POST" and request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
        pedido_id = request.POST.get("pedido_id")

        try:
            pedido = Pedido.objects.get(id=pedido_id)
            pedido.status = "Concluído"
            pedido.save()
            return redirect('sucesso')  # Redirecionar para a página 'sucesso'
        except Pedido.DoesNotExist:
            return render(request, 'sucesso.html')

    else:
        return render(request, 'sucessomod.html')

def apagar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    
    # Certifique-se de adicionar verificações de permissão ou lógica de exclusão personalizada aqui

    pedido.delete()

    return JsonResponse({"success": True})




def gerar_pdf_pedido(pedido):
    # Crie um objeto PDF
    response = HttpResponse(content_type='application/pdf')
    pdf_filename = f"PEDIDO_{pedido.data_pedido.strftime('%Y%m%d')}_ID_{pedido.id}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{pdf_filename}"'
    doc = SimpleDocTemplate(response, pagesize=landscape(letter))

    # Crie uma lista vazia para armazenar o conteúdo do PDF
    elements = []

    estilo_titulo = ParagraphStyle(name='TituloStyle', fontSize=16, alignment=1, spaceAfter=12)

    

    styles = getSampleStyleSheet()
    titulo = f"PEDIDO Nº {pedido.id} CRIADO NO DIA {pedido.data_pedido.strftime('%d/%m/%Y')}"
    titulo_para = Paragraph(titulo, estilo_titulo)
    elements.append(titulo_para)
    elements.append(Spacer(1, 12))




    # Crie uma tabela de cabeçalho personalizada
    cabecalho = Table([['QUANTIDADE', 'FRUTAS', 'QUANTIDADE', 'VERDURAS']], colWidths=[100, 150, 100, 150])
    cabecalho.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkorange),  # Cor de fundo do cabeçalho
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Cor do texto do cabeçalho
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),  # Alinhamento do texto no cabeçalho
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(cabecalho)

    lista_de_frutas = [
        "ABACATE", "AMEIXA FRESCA", "AMEIXA SECA", "ABACAXI", "CAQUI", "CÔCO", "GOIABA", "LARANJA",
        "LIMÃO", "MAÇÃ VERDE", "MAÇÃ ARGENTINA", "MAÇÃ 120", "MAÇÃ 180", "MANGA TOMI", "MANGA ESPADA",
        "MAMÃO FORMOSA", "MANGA PALMER", "MAMÃO HAVAI", "MARACUJÁ", "MELÃO AMARELO", "MELÃO REI", "MORANGO",
        "PASSAS", "PÊRA PORTUGUESA", "PÊRA ARGENTINA", "POKAN", "UVA ITÁLIA", "UVA RUBI", "UVA VITÓRIA",
        "RAMBUTAN", "BANANA / TERRA", "BANANA/ PRATA", "MELANCIA","MAÇA ARGENTINA"
    ]
    frutas = []
    verduras = []

    for item in pedido.itempedido_set.all():
        if item.tipo in lista_de_frutas:
            frutas.append([str(item.quantidade), item.tipo])
        else:
            verduras.append([str(item.quantidade), item.tipo])

    # Crie a tabela com as colunas "QUANTIDADE/FRUTA/QUANTIDADE/VERDURA"
    detalhes_frutas_verduras = []
    max_len = max(len(frutas), len(verduras))
    for i in range(max_len):
        row = []
        if i < len(frutas):
            row.extend(frutas[i])
        else:
            row.extend(["", ""])  # Preencha com células em branco se não houver fruta correspondente
        if i < len(verduras):
            row.extend(verduras[i])
        else:
            row.extend(["", ""])  # Preencha com células em branco se não houver verdura correspondente
        detalhes_frutas_verduras.append(row)

    # Crie a tabela com a estrutura "QUANTIDADE/FRUTA/QUANTIDADE/VERDURA"
    table_frutas_verduras = Table(detalhes_frutas_verduras, colWidths=[100, 150, 100, 150])
    table_frutas_verduras.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.orange),  # Cor de fundo do cabeçalho
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Cor do texto do cabeçalho
        ('BACKGROUND', (0, 1), (-1, -1), colors.orange),  # Cor de fundo das linhas restantes (mesma cor do cabeçalho)
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(table_frutas_verduras)


    # Crie o PDF
    doc.build(elements)
    
    return response






def sucesso(request):
    return render(request, 'sucesso.html')














def download_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    pdf_response = gerar_pdf_pedido(pedido)
    return pdf_response







def adicionar_item_pedido(request, pedido_id):
    if request.method == 'POST':
        tipo_item = request.POST.get('tipo_item')
        quantidade_item = request.POST.get('quantidade_item')

        # Recupere o pedido com base no ID
        pedido = Pedido.objects.get(pk=pedido_id)

        # Crie um novo item do pedido e associe-o ao pedido
        item_pedido = ItemPedido.objects.create(
            pedido=pedido,
            tipo=tipo_item,
            quantidade=quantidade_item
        )

        # Redirecione de volta para a página de modificação do pedido
        return redirect('modificar_pedido', pedido_id=pedido_id)

    # Se a solicitação não for POST, você pode renderizar um template vazio ou uma mensagem.
    # Adapte isso de acordo com suas necessidades.
    return render(request, 'mod.html')  # Substitua 'empty_template.html' pelo template desejado.

# Crie uma view para remover um item do pedido
def remover_item_pedido(request, pedido_id, item_id):
    item_pedido = ItemPedido.objects.get(pk=item_id)
    item_pedido.delete()
    return redirect('modificar_pedido', pedido_id=pedido_id)



def modificar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id)

    # Aqui você pode adicionar a lógica para obter os itens do pedido, se necessário

    return render(request, 'mod.html', {'pedido': pedido})
