def get_path_upload_avatar(instance, file):
    """ Построение пути к файлу: media/avatars/user_id/photo"""
    return f'avatars/{instance.id}/{file}'