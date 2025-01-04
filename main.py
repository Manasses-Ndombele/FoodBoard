import flet as ft
import requests
import re

api_key = 'c9cfff63f4a64ea3b139d0cb1e2f203a'

def get_receipts_list(filters):
    url = f'https://api.spoonacular.com/recipes/findByNutrients?'
    for c, (filter_key, filter_value) in enumerate(filters.items()):
        if c == 0:
            url += f'{filter_key}={filter_value.value}'

        elif c % 2 == 1:
            url += f'&{filter_key}={filter_value.value}'

    url += f'&number=10&apiKey={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        receipts_datas = response.json()
        return receipts_datas

def main(page: ft.Page):
    def get_started_page():
        start_view = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text('Olá, seja bem vindo!', size=30, weight=ft.FontWeight.BOLD, italic=True, text_align=ft.TextAlign.CENTER),
                    ft.Text('Vamos fazer análises visuais de 10 receitas nutritivas para si, baseado em nutrientes que devem ser adicionados a sua dieta e em dados que serão obtidos atavés da Spoonacular API que servirá de base para a construção de um dashboard.', size=20, font_family='Consolas', selectable=True, text_align=ft.TextAlign.CENTER),
                    ft.ElevatedButton(text='Bora Começar!', bgcolor=ft.Colors.GREY, color=ft.Colors.BLUE_50, width=200, height=30, on_click=questions_page)
                ],
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            expand=True,
            padding=20
        )

        page.add(start_view)

    def receipts_list_page(receipts):
        def on_chart_hover(e: ft.PieChartEvent, chart: ft.PieChart):
            hover_title_style = ft.TextStyle(
                size=22,
                color=ft.Colors.WHITE,
                weight=ft.FontWeight.BOLD,
                shadow=ft.BoxShadow(blur_radius=2, color=ft.Colors.BLACK54),
            )

            normal_title_style = ft.TextStyle(size=16, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)
            for idx, section in enumerate(chart.sections):
                if idx == e.section_index:
                    section.radius = 150
                    section.title_style = hover_title_style

                else:
                    section.radius = 140
                    section.title_style = normal_title_style

            chart.update()

        def set_pie_section(value, color):
            nutri_re_pattern = r'(\d+)\s*(IU|mg|g|μg)'
            return ft.PieChartSection(
                re.sub(nutri_re_pattern, r'\1', value),
                color=color,
                radius=140,
                border_side=ft.BorderSide(0, ft.Colors.with_opacity(0, ft.Colors.WHITE)),
                title=value,
                title_style=ft.TextStyle(size=16, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)
            )

        page.clean()
        receipts_view = ft.ListView(expand=1, spacing=10, padding=20)
        for data in receipts:
            chart = ft.PieChart(
                sections=[
                    set_pie_section(data.get('protein'), ft.Colors.GREEN),
                    set_pie_section(data.get('fat'), ft.Colors.RED),
                    set_pie_section(data.get('carbs'), ft.Colors.BLUE),
                    set_pie_section(data.get('calcium'), ft.Colors.RED_400),
                    set_pie_section(data.get('cholesterol'), ft.Colors.PURPLE_400),
                    set_pie_section(data.get('vitaminA'), ft.Colors.BLUE_400),
                    set_pie_section(data.get('vitaminC'), ft.Colors.INDIGO_400),
                    set_pie_section(data.get('vitaminD'), ft.Colors.BROWN_200),
                    set_pie_section(data.get('iron'), ft.Colors.AMBER_200)
                ],
                sections_space=1,
                center_space_radius=0,
                expand=True
            )

            chart.on_chart_event = lambda e, chart=chart: on_chart_hover(e, chart)
            datas_column = ft.Column(controls=[ft.ListView(
                controls=[
                    ft.Row(controls=[
                            ft.Text(data.get('title'), expand=True, size=20, weight=ft.FontWeight.BOLD)
                        ],
                        spacing=15
                    ),
                    ft.Row(controls=[
                            ft.Icon(name=ft.Icons.CIRCLE, color=ft.Colors.GREEN),
                            ft.Text('Proteínas')
                        ],
                        expand=True
                    ),
                    ft.Row(controls=[
                            ft.Icon(name=ft.Icons.CIRCLE, color=ft.Colors.RED),
                            ft.Text('Gorduras')
                        ],
                        expand=True
                    ),
                    ft.Row(controls=[
                            ft.Icon(name=ft.Icons.CIRCLE, color=ft.Colors.BLUE),
                            ft.Text('Carbohidratos')
                        ],
                        expand=True
                    ),
                    ft.Row(controls=[
                            ft.Icon(name=ft.Icons.CIRCLE, color=ft.Colors.RED_400),
                            ft.Text('Cálcio')
                        ],
                        expand=True
                    ),
                    ft.Row(controls=[
                            ft.Icon(name=ft.Icons.CIRCLE, color=ft.Colors.PURPLE_400),
                            ft.Text('Colesterol')
                        ],
                        expand=True
                    ),
                    ft.Row(controls=[
                            ft.Icon(name=ft.Icons.CIRCLE, color=ft.Colors.BLUE_400),
                            ft.Text('Vitamina A')
                        ],
                        expand=True
                    ),
                    ft.Row(controls=[
                            ft.Icon(name=ft.Icons.CIRCLE, color=ft.Colors.INDIGO_400),
                            ft.Text('Vitamina C')
                        ],
                        expand=True
                    ),
                    ft.Row(controls=[
                            ft.Icon(name=ft.Icons.CIRCLE, color=ft.Colors.BROWN_200),
                            ft.Text('Vitamina D')
                        ],
                        expand=True
                    ),
                    ft.Row(controls=[
                            ft.Icon(name=ft.Icons.CIRCLE, color=ft.Colors.AMBER_200),
                            ft.Text('Ferro')
                        ],
                        expand=True
                    )
                ],
                expand=True
            )], expand=True)

            receipts_view.controls.append(
                ft.Row(controls=[
                        ft.Image(src=data.get('image'), fit=ft.ImageFit.COVER, repeat=ft.ImageRepeat.NO_REPEAT, border_radius=ft.border_radius.all(10)),
                        chart,
                        datas_column
                    ],
                    expand=True
                )
            )

        page.add(receipts_view)

    def questions_page(e):
        def validate_form():
            def display_error(text_field, msg):
                text_field.error_text = msg
                page.update()

            def remove_error_msg():
                field.error_text = ''
                page.update()

            submit_form_btn.text = 'Aguarde um momento...'
            submit_form_btn.disabled = True
            form = {
                'minCarbs': min_carbs,
                'maxCarbs': max_carbs,
                'minProtein': min_proteins,
                'maxProtein': max_proteins,
                'minFat': min_fat,
                'maxFat': max_fat,
                'minCalcium': min_calcium,
                'maxCalcium': max_calcium,
                'minCholesterol': min_cholesterol,
                'maxCholesterol': max_cholesterol,
                'minVitaminA': min_vitamin_a,
                'maxVitaminA': max_vitamin_a,
                'minVitaminC': min_vitamin_c,
                'maxVitaminC': max_vitamin_c,
                'minVitaminD': min_vitamin_d,
                'maxVitaminD': max_vitamin_d,
                'minIron': min_iron,
                'maxIron': max_iron
            }

            for field_key, field in form.items():
                if not field.value.isnumeric():
                    display_error(field, 'O valor fornecido para este campo não é numérico!')

                else:
                    if 'min' in field_key:
                        if not int(field.value) < int(form[f'max{field_key[3:]}'].value):
                            display_error(field, 'O valor fornecido não pode ser maior ou igual do que o campo seguinte!')

                        else:
                            remove_error_msg()

                    if 'max' in field_key:
                        if not int(field.value) > int(form[f'min{field_key[3:]}'].value):
                            display_error(field, 'O valor fornecido não pode ser menor ou igual do que o campo anterior!')

                        else:
                            remove_error_msg()

            receipts_list_page(get_receipts_list(form))

        def handle_submit_form(e):
            validate_form()

        page.clean()
        questions_lv = ft.ListView(expand=True, spacing=10, padding=20)
        questions_lv.controls.append(ft.Text('Selecione os nutrientes mais essenciais para adicionar a sua dieta baseado nas recomendações do seu nutricionista.', size=20, weight=ft.FontWeight.BOLD, italic=True))
        questions_lv.controls.append(ft.Text('Carbohidratos'))
        min_carbs = ft.TextField(label='Mínimo')
        max_carbs = ft.TextField(label='Máximo')
        questions_lv.controls.append(ft.Row(spacing=5, controls=[min_carbs, max_carbs]))
        questions_lv.controls.append(ft.Text('Proteínas'))
        min_proteins = ft.TextField(label='Mínimo')
        max_proteins = ft.TextField(label='Máximo')
        questions_lv.controls.append(ft.Row(spacing=5, controls=[min_proteins, max_proteins]))
        questions_lv.controls.append(ft.Text('Gordura'))
        min_fat = ft.TextField(label='Mínimo')
        max_fat = ft.TextField(label='Máximo')
        questions_lv.controls.append(ft.Row(spacing=5, controls=[min_fat, max_fat]))
        questions_lv.controls.append(ft.Text('Cálcio'))
        min_calcium = ft.TextField(label='Mínimo')
        max_calcium = ft.TextField(label='Máximo')
        questions_lv.controls.append(ft.Row(spacing=5, controls=[min_calcium, max_calcium]))
        questions_lv.controls.append(ft.Text('Colesterol'))
        min_cholesterol = ft.TextField(label='Mínimo')
        max_cholesterol = ft.TextField(label='Máximo')
        questions_lv.controls.append(ft.Row(spacing=5, controls=[min_cholesterol, max_cholesterol]))
        questions_lv.controls.append(ft.Text('Vitamina A'))
        min_vitamin_a = ft.TextField(label='Mínimo')
        max_vitamin_a = ft.TextField(label='Máximo')
        questions_lv.controls.append(ft.Row(spacing=5, controls=[min_vitamin_a, max_vitamin_a]))
        questions_lv.controls.append(ft.Text('Vitamina C'))
        min_vitamin_c = ft.TextField(label='Mínimo')
        max_vitamin_c = ft.TextField(label='Máximo')
        questions_lv.controls.append(ft.Row(spacing=5, controls=[min_vitamin_c, max_vitamin_c]))
        questions_lv.controls.append(ft.Text('Vitamina D'))
        min_vitamin_d = ft.TextField(label='Mínimo')
        max_vitamin_d = ft.TextField(label='Máximo')
        questions_lv.controls.append(ft.Row(spacing=5, controls=[min_vitamin_d, max_vitamin_d]))
        questions_lv.controls.append(ft.Text('Ferro'))
        min_iron = ft.TextField(label='Mínimo')
        max_iron = ft.TextField(label='Máximo')
        questions_lv.controls.append(ft.Row(spacing=5, controls=[min_iron, max_iron]))
        submit_form_btn = ft.ElevatedButton(text='Enviar', bgcolor=ft.Colors.GREY, color=ft.Colors.BLUE_50, width=200, on_click=handle_submit_form)
        questions_lv.controls.append(ft.Row(controls=[submit_form_btn], spacing=30))
        page.add(questions_lv)

    page.title = 'FoodBoaord - Dashboard de análise de receitas nutritivas'
    modal_info = ft.AlertDialog(title=ft.Text('Descrição', size=30, weight=ft.FontWeight.BOLD), content=ft.Text('Este programa tem um foco em demonstrar meus conhecimentos em programação desktop com Flutter usando o Python e habilidades de conexão com APIs exemplificando aqui fazendo uma conexão gratuita com a SpoonacularAPI com o objetivo de obter dados de receitas para usar como base na construção de um dashboard de avalição nutritiva de alimentos recomendados para si através de uma requesição a SpoonacularAPI.\n\nCopyright © 2025 Manassés Ndombele - Programador Pleno', font_family='Consolas', selectable=True, size=20))
    page.appbar = ft.AppBar(
        title=ft.Text('FoodBoard', color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
        center_title=False,
        bgcolor=ft.Colors.RED_400,
        actions=[ft.IconButton(ft.Icons.QUESTION_MARK_OUTLINED, on_click=lambda e: page.open(modal_info))]
    )

    get_started_page()

ft.app(target=main)
