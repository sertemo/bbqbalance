import flet as ft
from typing import Callable

from some_func import CUADRILLA, LISTA_COLORES_AVATAR

COLOR_LETRA = '#41474c'

def get_color_sync(nombre:str) -> str:
    lista_nombres = []
    for item in CUADRILLA.items():
        lista_nombres.append(item[0])
        lista_nombres.append(item[1])
    
    dict_persona_color = {}
    for name, color in zip(lista_nombres, LISTA_COLORES_AVATAR):
        dict_persona_color[name] = color

    return dict_persona_color[nombre]
   
class RotuloTexto(ft.UserControl):
    def __init__(self, 
                 texto, 
                 tamaño:int=40, 
                 color_borde:ft.colors=ft.colors.BLUE_700, 
                 color_interior:ft.colors=ft.colors.GREY_300):        
        super().__init__()
        self.texto = texto
        self.tamaño = tamaño
        self.color_borde = color_borde
        self.color_interior = color_interior

    def build(self):
        return ft.Stack(
            [
                ft.Text(
                    spans=[
                        ft.TextSpan(
                            self.texto,
                            ft.TextStyle(
                                size=self.tamaño,
                                weight=ft.FontWeight.BOLD,
                                foreground=ft.Paint(
                                    color=self.color_borde,
                                    stroke_width=4,
                                    stroke_join=ft.StrokeJoin.ROUND,
                                    style=ft.PaintingStyle.STROKE,
                                ),
                            ),
                        ),
                    ],
                ),
                ft.Text(
                    spans=[
                        ft.TextSpan(
                            self.texto,
                            ft.TextStyle(
                                size=self.tamaño,
                                weight=ft.FontWeight.BOLD,
                                color=self.color_interior,
                            ),
                        ),
                    ],
                ),
            ]
        )
    
class LineaParticipante(ft.UserControl):
    def __init__(self, nombre:str, concepto:str, importe:float, delete_func:Callable=None):
        super().__init__()
        self.nombre = nombre
        self.concepto = concepto
        self.importe = str(importe) + " €"
        self.delete_func = delete_func
        self.color_fondo = get_color_sync(nombre)

    def build(self) -> ft.Row:
        return ft.Row(
                [   ft.Container(
                        ft.Stack(
                            [
                                ft.CircleAvatar(
                                    content=ft.Icon(ft.icons.PERSON),
                                    color='#c2b6a8',
                                    bgcolor=self.color_fondo ,#'#af987e',
                                    #expand=True,
                                    right=30,
                                    top=8,
                                    scale=1.4
                                    ),
                                ft.Container(RotuloTexto(self.nombre, 15, COLOR_LETRA, ft.colors.WHITE60), bottom=2, left=40)
                            ],
                        ),
                        width=100,
                        height=60,
                    ),
                    
                    ft.Container(
                        RotuloTexto(self.concepto, 25, '#feefdd', '#41474c'),
                        expand=True,
                        alignment=ft.alignment.center,
                        border_radius=20,
                        padding=5,
                    ),
                    ft.Container(
                        RotuloTexto(self.importe, 25, '#41474c', '#f0975f', ),
                        width=400,
                        alignment=ft.alignment.center,
                        expand=True,
                        border_radius=20,
                        padding=5,
                    ),
                    ft.ElevatedButton(
                        key=self.nombre,
                        content=ft.Icon(name=ft.icons.DELETE, expand=True, size=30,),                        
                        color='#931f1f', 
                        bgcolor='#d85243',
                        on_click=self.delete_func
                        )
                ],
                expand=True,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            )
