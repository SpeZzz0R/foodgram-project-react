# import io
#
# from django.core.files.base import ContentFile
# from recipes.models import ShoppingCart
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.pdfbase import pdfmetrics
# from reportlab.pdfbase.ttfonts import TTFont
# from reportlab.platypus import Paragraph, SimpleDocTemplate
#
#
# def create_pdf_shopping_cart(user):
#     pdf_buffer = io.BytesIO()
#     shopping_cart_pdf = SimpleDocTemplate(pdf_buffer)
#
#     style = getSampleStyleSheet()
#     style['Normal'].fontName = 'DejaVuSerif'
#     style['Heading1'].fontName = 'DejaVuSerif'
#     font = TTFont('DejaVuSerif', './fonts/DejaVuSerif.ttf', 'UTF-8')
#     pdfmetrics.registerFont(font)
#
#     shopping_cart = {}
#     for obj in ShoppingCart.objects.filter(user=user):
#         ingredients = obj.recipe.ingredients.all()
#         for ingredient in ingredients:
#             ingredient_label = (
#                 f'{ingredient.name} ({ingredient.measurement_unit})'
#             )
#             if shopping_cart.get(ingredient_label):
#                 shopping_cart[ingredient_label] += ingredient.amount
#             else:
#                 shopping_cart[ingredient_label] = ingredient.amount
#     shopping_cart = [
#         '{}: {}\n'.format(key, val) for key, val in shopping_cart.items()
#     ]
#     shopping_cart = [
#         Paragraph(value, style['Normal']) for value in shopping_cart
#     ]
#     header = Paragraph('Список покупок:', style['Heading1'])
#     shopping_cart.insert(0, header)
#
#     shopping_cart_pdf.build(shopping_cart)
#
#     pdf_buffer.seek(0)
#     pdf = pdf_buffer.getvalue()
#     file_data = ContentFile(pdf)
#     file_data.name = 'shopping_cart.pdf'
#
#     return file_data
