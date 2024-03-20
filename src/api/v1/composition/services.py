from typing import Dict, Optional

from django.db.models import Avg


def get_path_upload_title(instance, file):
    """ Построение пути к файлу: media/composition_image/id/slug_photo"""
    return f'composition_image/{instance.id}/{instance.slug}_{file}'


# class ModelAnnotate:
#     """
#     Класс анотирует модель при помощи Django ORM метода annotate
#     :param
#         model = Django ORM модель (Composition)
#         annotates = Словарь вида {'Название': Агрегатная функция('Поле по которому будет производиться вычесление')}
#         ({'avg_rating': Avg('usercompositionrelation__rating)})
#
#     """
#
#     def __init__(self, model, annotates):
#         self.model = model
#         self.annotates = annotates
#
#     def get_model(self):
#         return self.model
#
#     def annotate(self, only_args: Optional[list[str]] = None):
#         if only_args:
#             query = self.model.objects.annotate(**self.annotates).only(*only_args)
