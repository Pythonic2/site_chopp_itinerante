import os
import django

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')  # Altere 'core' para o nome correto do seu projeto
django.setup()

from main.models import ImagemEvento  # Ajuste o caminho para o modelo correto

# Mapeamento dos antigos IDs para os novos IDs
evento_id_mapping = {
    9: 9,
    23: 10,
    13: 11,
    15: 12,
    21: 13,
    22: 14,
    7: 15,
}

# Lista com os dados de imagens e eventos
imagens_eventos = [
    {"image": "eventos/IMG_6804.jpeg", "evento_id": 23},
    {"image": "eventos/IMG_6796.jpeg", "evento_id": 23},
    {"image": "eventos/IMG_6802.jpeg", "evento_id": 23},
    {"image": "eventos/IMG_6801.jpeg", "evento_id": 23},
    {"image": "eventos/IMG_6807.jpeg", "evento_id": 23},
    {"image": "eventos/IMG_6810.jpeg", "evento_id": 23},
    {"image": "eventos/IMG_6816.jpeg", "evento_id": 23},
    {"image": "eventos/IMG_6916.jpeg", "evento_id": 23},
    {"image": "eventos/IMG_5566.jpeg", "evento_id": 7},
    {"image": "eventos/IMG_5564_OEgwG4m.jpeg", "evento_id": 7},
    {"image": "eventos/IMG_5579.jpeg", "evento_id": 7},
    {"image": "eventos/12BF40F6-3332-456B-82B3-632E0DE862D3.jpeg", "evento_id": 7},
    {"image": "eventos/BA57E010-41BE-4067-87E3-B4AA520DFCF6.jpeg", "evento_id": 7},
    {"image": "eventos/82090845-8939-4dc2-8c11-a20e2778b316_UVzxOCd.jpeg", "evento_id": 7},
    {"image": "eventos/7B92832D-EB11-43B2-959D-8A429BB2D38C.jpeg", "evento_id": 7},
    {"image": "eventos/9526d2ee-f4e3-441e-a41f-dff5627b1d96_MZcR9xE.jpeg", "evento_id": 7},
    {"image": "eventos/A370457B-D56A-44E9-8E62-95A3D265E429.jpeg", "evento_id": 9},
    {"image": "eventos/IMG_5734.jpeg", "evento_id": 9},
    {"image": "eventos/IMG_5750.jpeg", "evento_id": 9},
    {"image": "eventos/IMG_5754.jpeg", "evento_id": 9},
    {"image": "eventos/IMG_5756.jpeg", "evento_id": 9},
    {"image": "eventos/IMG_5760.jpeg", "evento_id": 9},
    {"image": "eventos/IMG_5765.jpeg", "evento_id": 9},
    {"image": "eventos/IMG_5766.jpeg", "evento_id": 9},
    {"image": "eventos/IMG_5797.jpeg", "evento_id": 9},
    {"image": "eventos/b28f1f84-93f2-440b-bf86-6ffdd7d7c709.jpeg", "evento_id": 9},
    {"image": "eventos/IMG_5829.jpeg", "evento_id": 9},
    {"image": "eventos/141d5a9f-db4f-4718-89f8-29352689f8a4.jpeg", "evento_id": 9},
    {"image": "eventos/IMG_5830.jpeg", "evento_id": 9},
    {"image": "eventos/E9241114-F4A5-4DB7-8846-E7531737C7BB.jpeg", "evento_id": 9},
    {"image": "eventos/IMG_6740.jpeg", "evento_id": 9},
    {"image": "eventos/IMG_6752.jpeg", "evento_id": 9},
    {"image": "eventos/IMG_6359.jpeg", "evento_id": 13},
    {"image": "eventos/IMG_6361.jpeg", "evento_id": 13},
    {"image": "eventos/IMG_6356.jpeg", "evento_id": 13},
    {"image": "eventos/IMG_6365.jpeg", "evento_id": 13},
    {"image": "eventos/IMG_6369.jpeg", "evento_id": 13},
    {"image": "eventos/IMG_6378.jpeg", "evento_id": 13},
    {"image": "eventos/IMG_6380.jpeg", "evento_id": 13},
    {"image": "eventos/IMG_6385.jpeg", "evento_id": 13},
    {"image": "eventos/IMG_6388.jpeg", "evento_id": 13},
    {"image": "eventos/IMG_6391.jpeg", "evento_id": 13},
    {"image": "eventos/IMG_6410.jpeg", "evento_id": 13},
    {"image": "eventos/IMG_6525.jpeg", "evento_id": 15},
    {"image": "eventos/IMG_6524.jpeg", "evento_id": 15},
    # ... (continua a lista)
]

# Atualizar os evento_id de acordo com o mapeamento
for imagem_evento in imagens_eventos:
    if imagem_evento['evento_id'] in evento_id_mapping:
        imagem_evento['evento_id'] = evento_id_mapping[imagem_evento['evento_id']]

# Inserir os dados no banco de dados
for imagem_evento in imagens_eventos:
    nova_imagem_evento = ImagemEvento(
        imagem=imagem_evento['image'],
        evento_id=imagem_evento['evento_id']
    )
    nova_imagem_evento.save()

print("Imagens cadastradas com sucesso.")
