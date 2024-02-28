import random
from typing import Literal
from icecream import ic

CUADRILLA = {
    'Marion': 'Olivier',
    'Leire': 'Sergio',
    'Nora': 'Jon',
    'Naiara': 'Jorge',
    'Marta': 'Andrés',
    'Estela': 'Odei',
    'Idoia': 'Eneko',
    'Oihane': 'Bruno'
}

LISTA_COLORES = [
    '#0da68c',
    '#24b568',
    '#6fc45c',
    '#ced42f',
    '#6c9600',
    '#26A69A',
    '#4CAF50',
    '#7CB342',
    '#C0CA33',
    '#FDD835',
    '#FFB300',
    '#FF9800',
    '#FB8C00',
    '#F4511E',
    '#ced42f',
    '#7CB342',
]
LISTA_COLORES_AVATAR = [
    '#263238',
    '#37474F',
    '#455A64',
    '#546E7A',
    '#607D8B',
    '#5C6BC0',
    '#3949AB',
    '#283593',
    '#1A237E',
    '#880E4F',
    '#AD1457',
    '#C2185B',
    '#D81B60',
    '#E91E63',
    '#455A64',
    '#283593',
]


async def lista_cuadrilla() -> list[str]:
    lista_nombres = []
    for mujer, hombre in CUADRILLA.items():
        lista_nombres.append(mujer)
        lista_nombres.append(hombre)
    return sorted(lista_nombres)


async def crear_dict_persona_color(tipo:Literal["avatar", "grafico"]='grafico') -> dict:
    lista = LISTA_COLORES if tipo == 'grafico' else LISTA_COLORES_AVATAR
    persona_color_dict = {}
    lista_nombres = await lista_cuadrilla()
    for nombre, color in zip(lista_nombres, lista):
        persona_color_dict[nombre] = color

    return persona_color_dict

#! No se usa
def generar_color_aleatorio():
    return '#{:02x}{:02x}{:02x}'.format(random.randint(100, 255), 
                                       random.randint(100, 255), 
                                       random.randint(100, 255))

async def get_color_async(nombre:str, tipo:Literal["avatar", "grafico"]='grafico') -> str:
    """Devuelve el color asociado a la persona

    Parameters
    ----------
    nombre : str
        _description_

    Returns
    -------
    str
        _description_
    """
    persona_color_dict = await crear_dict_persona_color(tipo)
    return persona_color_dict[nombre]

class Switch:
    def __init__(self, initial_state:bool=True) -> None:
        self.state = initial_state

    def accionar(self) -> None:
        self.state = not self.state
