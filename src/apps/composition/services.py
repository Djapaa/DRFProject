def get_path_upload_title(instance, file):
    """ Построение пути к файлу: media/composition_image/id/slug_photo"""
    return f'composition_image/{instance.id}/{instance.slug}_{file}'