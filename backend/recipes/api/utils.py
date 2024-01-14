import json
import re
import traceback

from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics, ttfonts
from reportlab.pdfgen import canvas


# Monster PDFGenerator v0.1
class PDFGenerator:
    IMAGE_PATTERN = r'image'
    TITLE_PATTERN = r'title'
    LIST_PATTERN = r'list'
    START_NEW_PAGE_PATTERN = r'new_page'

    def __init__(self, filename, fonts_path, data_path):
        self.pdf = canvas.Canvas(
            filename=filename,
            pagesize=A4,
        )
        self.fonts = self.load_files(fonts_path)
        self.data = self.load_files(data_path)

        self.register_fonts()

    def load_files(self, path):
        try:
            with open(path, 'r') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            print(
                f'Файл {path} не найден.'
            )
        except json.decoder.JSONDecodeError as e:
            print(
                f'Ошибка при декодировании JSON: {e}'
            )
        except Exception as e:
            traceback.print_exc()
            print(
                f'Неизвестная ошибка: {e}'
            )
        return None

    def register_fonts(self):
        if self.fonts:
            for font_key, font_value in self.fonts.items():
                try:
                    pdfmetrics.registerFont(
                        ttfonts.TTFont(
                            name=font_value['font_name'],
                            filename=font_value['font_path'],
                        )
                    )
                except Exception as e:
                    traceback.print_exc()
                    print(
                        f'Ошибка при регистрации шрифта '
                        f'"{font_value["font_name"]}": {e}'
                    )

    def set_font(self, font):
        try:
            self.pdf.setFont(
                psfontname=font['font_name'],
                size=font['font_size'],
            )
        except Exception as e:
            traceback.print_exc()
            print(
                f'Ошибка при установке шрифта "{font["font_name"]}": {e}'
            )

    def draw_title(self, x, y, text):
        self.set_font(
            font=self.fonts['title'],
        )
        self.pdf.drawString(
            x=x,
            y=y,
            text=text,
        )

    def draw_list(
            self,
            data,
            items_per_page_first,
            items_per_page_others,
            first_page_y,
            other_pages_y,
            x,
    ):
        self.set_font(
            font=self.fonts['text'],
        )
        y = first_page_y
        items_per_page = items_per_page_first
        for index, item in enumerate(data):
            try:
                if index > 0 and index % items_per_page == 0:
                    page_number = int(index / items_per_page) + 1
                    if page_number >= 2:
                        items_per_page = items_per_page_others
                        self.pdf.showPage()
                        self.set_font(
                            font=self.fonts['text'],
                        )
                        y = other_pages_y - (
                            index % items_per_page_others * 20
                        )
                self.pdf.drawString(
                    x,
                    y - (index % items_per_page * 20),
                    item,
                )
            except Exception as e:
                traceback.print_exc()
                print(
                    f'Ошибка при отрисовке элемента списка {item}: {e}'
                )

    def generate_pdf(self, list_data=None):
        for data_key, data_value in self.data.items():
            try:
                if re.search(self.IMAGE_PATTERN, data_key):
                    self.pdf.drawImage(
                        image=data_value['image'],
                        x=data_value['x'],
                        y=data_value['y'],
                        height=data_value['height'],
                        width=data_value['width'],
                    )
                elif re.search(self.TITLE_PATTERN, data_key):
                    self.draw_title(
                        x=data_value['x'],
                        y=data_value['y'],
                        text=data_value['text'],
                    )
                elif re.search(self.LIST_PATTERN, data_key):
                    list_source = (
                        list_data if list_data is not None
                        else data_value['objects']
                    )
                    self.draw_list(
                        data=list_source,
                        items_per_page_first=data_value[
                            'items_per_page_first'
                        ],
                        items_per_page_others=data_value[
                            'items_per_page_others'
                        ],
                        first_page_y=data_value['first_page_y'],
                        other_pages_y=data_value['other_pages_y'],
                        x=data_value['x'],
                    )
                elif re.search(self.START_NEW_PAGE_PATTERN, data_key):
                    if data_value == 'True':
                        self.pdf.showPage()

            except Exception as e:
                traceback.print_exc()
                print(
                    f'Ошибка при обработке элемента "{data_key}": {e}'
                )

        self.pdf.save()
        return self.pdf
