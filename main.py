import flet as ft
from some_func import (
    lista_cuadrilla,
    get_color_async,
    Switch
)
from icecream import ic
from pathlib import Path

import asyncio
from backend.balance import (
    Barbecue, 
    Transaction, 
    )

from flet_models import (
    RotuloTexto,
    LineaParticipante,
)

# flet pack main.py --icon "assets/img/logo limpiado.png" --add-data "assets;assets" --product-name BBQBalance --file-description "Aplicacion para hacer ajustes entre los papis y mamis de la cuadrilla cuando se hacen barbacoas"

WIN_HEIGHT:int = 1000
WIN_WIDTH:int = 1200
COLORES_GRADIENTE:list = ['#c53c2f', '#f0975f', '#feefdd']
COLOR_LETRA = '#41474c'
COLOR_VERDE = '#61b36f'
COLOR_BLANCO = '#feefdd'
SPRITE_PATH = Path('/img/sprites')
SPRITE_LIST = [f'fuego{i}.png' for i in range(1,4)]

switch = Switch()

async def get_list_dropdown() -> list[ft.dropdown.Option]:
    cuadri:list = await lista_cuadrilla()
    return [ft.dropdown.Option(nombre) for nombre in cuadri]


async def main(page: ft.Page):

    page.fonts = {
        "Kanit": "https://raw.githubusercontent.com/google/fonts/master/ofl/kanit/Kanit-Bold.ttf",
        "Open Sans Bold": "fonts/OpenSans-ExtraBold.ttf",
        "Open Sans": "",
        "Nunito": "fonts/Nunito[wght].ttf"
    }
    page.title = "BBQ Balance"
    page.theme = ft.Theme(font_family="Open Sans Bold")
    page.bgcolor = '#ffefe0'
    page.window_width = WIN_WIDTH
    page.window_height = WIN_HEIGHT
    page.window_resizable = False

    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Instanciamos la clase Barbacoa
    bbq = Barbecue()

    # Parte de resumenes y gráficos
    async def create_pie_sections(bbq:Barbecue) -> list[ft.PieChartSection]:
        lista_chart = []
        for participante, porcentaje in bbq.participants_initial_expenses_perc.items():
            lista_chart.append(
                ft.PieChartSection(
                    porcentaje,
                    title=f"{participante}\n{porcentaje:.1%}",
                    radius=80,
                    border_side=ft.BorderSide(width=2, color=ft.colors.WHITE60),
                    color=await get_color_async(participante),
                    title_style=ft.TextStyle(color=ft.colors.WHITE60)
                )
            )
        return lista_chart
    
    async def create_barchartgroup(bbq:Barbecue) -> list[ft.BarChartGroup]:
        lista_chart = []
        color_deudor_rojo = '#c53c2f'
        color_acreedor_verde = '#61b36f'
        for x, (participante, diferencia) in enumerate(bbq.participants_differences.items()):
            lista_chart.append(
                ft.BarChartGroup(
                    x,
                    bar_rods=[
                        ft.BarChartRod(
                            border_side=ft.BorderSide(1, color=COLOR_LETRA) ,
                            from_y=0,
                            to_y=diferencia,
                            width=20,
                            color=color_deudor_rojo if diferencia < 0 else color_acreedor_verde,
                            tooltip=round(diferencia, 1),
                            border_radius=3
                        )
                    ]
                )
            )
        return lista_chart
    
    async def create_barchart_axis(bbq:Barbecue) -> ft.ChartAxis:
        axis_object = ft.ChartAxis(labels_size=40)

        for x, (participante, diferencia) in enumerate(bbq.participants_differences.items()):
            axis_object.labels.append(
                ft.ChartAxisLabel(
                    value=x,
                    label=ft.Container(ft.Text(participante[:3], color='#41474c', size=10), padding=5)
                )
            )
        
        return axis_object

    media_gasto = ft.Text(color=COLOR_LETRA, size=16)
    total_gasto = ft.Text(color=COLOR_LETRA, size=16)
    num_participantes = ft.Text(color=COLOR_LETRA, size=16)

    normal_radius = 80
    hover_radius = 100
    normal_title_style = ft.TextStyle(
        size=16, color=ft.colors.WHITE60, weight=ft.FontWeight.BOLD
    )
    hover_title_style = ft.TextStyle(
        size=22,
        weight=ft.FontWeight.BOLD,
        shadow=ft.BoxShadow(blur_radius=2, color=ft.colors.BLACK54),
        color=ft.colors.WHITE60,
    )

    async def on_chart_event(e: ft.PieChartEvent):
        for idx, section in enumerate(pie_chart.sections):
            if idx == e.section_index:
                section.radius = hover_radius
                section.title_style = hover_title_style
            else:
                section.radius = normal_radius
                section.title_style = normal_title_style
        await pie_chart.update_async()

    pie_chart = ft.PieChart(
        sections_space=2,
        center_space_radius=40,
        expand=True,
        on_chart_event=on_chart_event,        
    )
    
    bar_chart_differences = ft.BarChart(
        expand=True,
        interactive=True,
        tooltip_bgcolor=ft.colors.WHITE60,
        horizontal_grid_lines=ft.ChartGridLines(
            color=ft.colors.GREY_300, width=1, dash_pattern=[3, 3]
        ),
        right_axis=ft.ChartAxis(
            labels_size=40, title=RotuloTexto("Diferencias",15 ,COLOR_LETRA, COLOR_BLANCO), title_size=30,
            show_labels=False
        )
    )
    listview_transacciones:ft.ListView = ft.ListView(spacing=5, padding=5,)    

    animacion_fuego = ft.Image(src=(SPRITE_PATH / 'fuego4.png'))

    def on_fire_click(e: ft.ControlEvent) -> None:
        """Acciona el switch para apagar o encender la animación del fuego

        Parameters
        ----------
        e : ft.ControlEvent
            _description_
        """
        switch.accionar()

    async def animate_sprite(sprite_list:list[str], inner_delay:float):
        """Carga las imagenes de la llama en bucle y de forma asíncrona 
        para simular el efecto parpadeante del fuego

        Parameters
        ----------
        image_path : Path
            _description_
        inner_delay : float
            _description_
        """
        while True:
                if switch.state:
                    for sprite in sorted(sprite_list):
                        animacion_fuego.src = (SPRITE_PATH / sprite)
                        await page.update_async()
                        await asyncio.sleep(inner_delay)
                    await page.update_async()
                else:
                    await asyncio.sleep(0.1)
                    await page.update_async()


    parte_resumenes = ft.Container(
        ft.Row(
            [
                ft.Container(
                    ft.Stack([
                        ft.Column(
                            [
                                RotuloTexto("Resumen", 20, COLOR_LETRA, COLOR_BLANCO),
                                ft.Container(pie_chart, border_radius=10, height=370),
                                ft.Container(
                                    ft.Column(
                                        [
                                            ft.Row([ft.Text("Participantes:", color=ft.colors.WHITE60, size=16),num_participantes]),
                                            ft.Row([ft.Text("Gasto medio:", color=ft.colors.WHITE60, size=16), media_gasto], vertical_alignment=ft.MainAxisAlignment.CENTER),
                                            ft.Row([ft.Text("Gasto total:", color=ft.colors.WHITE60, size=16), total_gasto], vertical_alignment=ft.MainAxisAlignment.CENTER),
                                        ],
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,                                        
                                    ),
                                    alignment=ft.alignment.center,
                                    padding=5,
                                    height=15,
                                    expand=True,
                                )
                                
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                    ]),
                    width=425, 
                    alignment=ft.alignment.center,
                    padding=5,
                    border_radius=8,
                    gradient=ft.LinearGradient(
                            begin=ft.alignment.center_left,
                            end=ft.alignment.center_right,
                            colors=COLORES_GRADIENTE,
                            ),                                                
                ),

                ft.Container(
                    ft.Column([
                        ft.Image(src='img/logo limpiado.png'),
                        ft.Container(animacion_fuego, on_click=on_fire_click),
                    ]),                     
                    expand=True, 
                    alignment=ft.alignment.top_center,
                    ),

                ft.Container(
                    ft.Column(
                        [
                            RotuloTexto("Ajustes", 20, COLOR_LETRA, COLOR_BLANCO),
                            ft.Container(bar_chart_differences, height=250, border_radius=10),
                            ft.Container(listview_transacciones, expand=True, alignment=ft.alignment.center),

                        ], 
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ), 
                    width=425,
                    alignment=ft.alignment.center,
                    padding=5,
                    border_radius=8,
                    gradient=ft.LinearGradient(
                            begin=ft.alignment.center_right,
                            end=ft.alignment.center_left,
                            colors=COLORES_GRADIENTE,
                    ),
                )      
                        
            ]
        ),
        width=1200,
        height=550,
        padding=5,
        border_radius=8,
    )

    # Parte agregar un participante
    desplegable_nombres = ft.Dropdown(
        label="Nombre",
        text_style=ft.TextStyle(font_family="Open Sans Bold"),
        text_size=18,
        autofocus=True,
        content_padding=5,
        options=await get_list_dropdown(), 
        height=40,
        focused_bgcolor='#fac5a0',
        color=COLOR_LETRA, 
        bgcolor='#fac5a0', 
        border_color=ft.colors.WHITE, 
        border_radius=8, 
        filled=True,
        alignment=ft.alignment.center,
        )
    
    concepto_persona = ft.TextField(
                        cursor_color='#c53c2f', 
                        text_size=18, 
                        content_padding=5, 
                        text_align=ft.TextAlign.CENTER, 
                        label="Concepto", 
                        height=40, 
                        expand=True, 
                        color=COLOR_LETRA, 
                        bgcolor='#fac5a0', 
                        border_color=ft.colors.WHITE, 
                        border_radius=8 #25
                        )
    importe_persona = ft.TextField(
                        keyboard_type=ft.KeyboardType.NUMBER, 
                        suffix_icon=ft.icons.EURO, 
                        cursor_color='#c53c2f', 
                        text_size=20, 
                        content_padding=5, 
                        text_align=ft.TextAlign.CENTER, 
                        label="Importe", 
                        height=40, 
                        expand=True, 
                        color=COLOR_LETRA, 
                        bgcolor='#fac5a0', 
                        border_color=ft.colors.WHITE, 
                        border_radius=8 #25
                        )
    

    listview = ft.ListView(spacing=10, padding=10, divider_thickness=2, expand=True)


    async def sacar_indice(nombre:str) -> int:
        """Saca el índice de una listview

        Parameters
        ----------
        nombre : str
            _description_

        Returns
        -------
        int
            _description_
        """
        for idx, linea in enumerate(listview.controls):
            if linea.nombre == nombre:
                return idx

    async def mostrar_transacciones(lista_transacciones:list[Transaction]) -> None:
        """Muestra en la listview los ajustes de cuentas con colores

        Parameters
        ----------
        lista_transacciones : list[Transaction]
            _description_
        """
        # Limpiamos la listview primero para volver a cargar las transacciones
        text_size = 15
        tipo_color = 'grafico'
        listview_transacciones.controls.clear()
        for trans in lista_transacciones:
            deudor = trans.from_participant
            acreedor = trans.to_participant
            importe = trans.amount
            listview_transacciones.controls.append(
                ft.Row([
                    RotuloTexto(f"{deudor}", text_size + 3, COLOR_LETRA, await get_color_async(deudor)) ,
                    ft.Text(f"debe a", size=text_size, color=COLOR_LETRA),
                    RotuloTexto(f"{acreedor}", text_size + 3, COLOR_LETRA, await get_color_async(acreedor)),
                    ft.Text(f"un total de", size=text_size, color=COLOR_LETRA),
                    RotuloTexto(f"{round(importe, 1)}", text_size + 5, COLOR_LETRA, await get_color_async(deudor)),
                    RotuloTexto(f"€", text_size + 5, COLOR_LETRA, COLOR_VERDE),
                    ])
            )

    async def borrar_participante(e: ft.ControlEvent) -> None:
        """Borra el participante y actualiza todos los widgets

        Parameters
        ----------
        e : ft.ControlEvent
            _description_
        """
        # Sacamos el nombre a borrar
        nombre_a_borrar = e.control.key

        # Sacamos el índice que corresponde con el nombre
        idx_a_borrar = await sacar_indice(nombre_a_borrar)

        # Borramos de la listview el índice
        listview.controls.pop(idx_a_borrar)

        # Borramos de la clase el participante
        bbq.delete_participant(nombre_a_borrar)

        # Recalculamos las diferencias
        bbq.set_participant_differences()        

        # Calculamos los ajustes
        lista_transacciones:list[Transaction] = await bbq.settle_expenses()

        # Mostramos los ajustes en la listview
        await mostrar_transacciones(lista_transacciones)

        # Actualizamos la media de gasto, el gasto total, y recalculamos las diferencias
        media_gasto.value = bbq.average_expense
        total_gasto.value = bbq.total_expense
        num_participantes.value = bbq.num_participants

        # Actualizamos los gráficos
        pie_chart.sections =  await create_pie_sections(bbq)
        bar_chart_differences.bar_groups = await create_barchartgroup(bbq)
        bar_chart_differences.bottom_axis = await create_barchart_axis(bbq)

        # Añadimos al dropdown de nuevo
        desplegable_nombres.options.append(ft.dropdown.Option(nombre_a_borrar))
        desplegable_nombres.value = ""
       
        await page.add_async()
   
    async def encontrar_opcion(nombre:str) -> ft.Dropdown.options:
        for opcion in desplegable_nombres.options:
            if nombre == opcion.key:
                return opcion
        return None

    async def agregar_participante_a_bbq_y_listview(e: ft.ControlEvent) -> None:
        """Agrega un participante a la instancia bbq y actualiza los widgets

        Parameters
        ----------
        e : ft.ControlEvent
            _description_
        """
        if (nombre:=desplegable_nombres.value) and (nombre not in bbq.participants_initial_expenses):
            # Añadimos participante a la instancia
            concepto = concepto_persona.value if concepto_persona.value else "Sin concepto"
            try:
                importe = float(importe_persona.value) if importe_persona.value else 0

                # Reiniciamos el mensaje de error
                importe_persona.error_text = ""
                await bbq.add_participant(nombre, importe, concepto)

                # Añadimos participante a la lista para visualizarlo
                listview.controls.append(LineaParticipante(nombre, concepto, importe, borrar_participante))
                media_gasto.value = str(bbq.average_expense) + " €"
                total_gasto.value = str(bbq.total_expense) + " €"
                num_participantes.value = bbq.num_participants

                # Quitamos participante del dropdown            
                opcion_a_borrar = await encontrar_opcion(nombre)
                if opcion_a_borrar is not None: 
                    desplegable_nombres.options.remove(opcion_a_borrar)

                # Quitamos participantes del concepto e importe
                concepto_persona.value = ""
                importe_persona.value = ""

                # Agregamos a los componentes del gráfico
                pie_chart.sections =  await create_pie_sections(bbq) 

                # Calculamos las diferencias
                bbq.set_participant_differences()     

                # Calculamos los ajustes
                lista_transacciones:list[Transaction] = await bbq.settle_expenses()

                # Mostramos los ajustes en la listview
                await mostrar_transacciones(lista_transacciones)

                # Añadimos al gráfico de barras
                bar_chart_differences.bar_groups = await create_barchartgroup(bbq)
                bar_chart_differences.bottom_axis = await create_barchart_axis(bbq)
            
            except ValueError:
                # Mostramos error
                importe_persona.error_text = "El valor debe ser un número"
                
            await page.update_async()
                

    parte_agregar = ft.Container(
        ft.Column(
            [
                #ft.Text(value="Agregar participantes", color=ft.colors.WHITE, size=20),
                RotuloTexto("Agregar participantes", 20, COLOR_LETRA, COLOR_BLANCO),
                ft.Row(
                    [
                    desplegable_nombres,
                    concepto_persona,
                    importe_persona,
                    ft.ElevatedButton(
                        content=ft.Icon(name=ft.icons.ADD),
                        bgcolor='#61b36f',
                        color=ft.colors.WHITE,
                        on_click=agregar_participante_a_bbq_y_listview
                        ),
                    ],
                )
            ],
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
        ),        
        alignment=ft.alignment.center,
        padding=15,
        border_radius=5,
        gradient=ft.LinearGradient(
            begin=ft.alignment.bottom_center,
            end=ft.alignment.top_center,
            colors=COLORES_GRADIENTE,
            ),
        height=110,
    )

    parte_listado_participantes = ft.Container(
        ft.Column(
            [
                RotuloTexto("Listado de participantes", 20, COLOR_LETRA, COLOR_BLANCO),
                listview,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        border_radius=10,
        padding=2,
        expand=True
    )

    contenedor_principal = ft.Container(
        ft.Column(
            controls=[
                parte_resumenes,
                parte_agregar,
                parte_listado_participantes,
                ]
            ),
        width= WIN_WIDTH,
        height=WIN_HEIGHT,
        expand=True,
        padding=2,
    )


    await page.add_async(
        contenedor_principal
        )
    await animate_sprite(SPRITE_LIST, 0.08)

if __name__ == '__main__':
    ft.app(
        target=main,
        assets_dir="assets")