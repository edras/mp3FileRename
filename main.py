import os
import eyed3
from eyed3.id3.tag import Tag


def is_wrong_text_in_title(title):
    wrong_terms = ['track', 'title', 'titel', 'trilha', 'faixa', 'spur', 'none']
    if any(wrong_term in title.lower() for wrong_term in wrong_terms):
        return True
    return False


def is_wrong_text_in_album(album):
    wrong_terms = ['none', 'desconhecido']
    if any(wrong_term in album.lower() for wrong_term in wrong_terms):
        return True
    return False


def is_number_in_front_of_text(text):
    parts = text.split('-')
    parts = parts[0].split(' ')
    try:
        if len(parts[0]) < 4:
            float(parts[0])
            return True
    except ValueError:
        return False


def is_title_wrong(title):
    if is_wrong_text_in_title(title):
        return True
    if is_number_in_front_of_text(title):
        return True
    return False


def is_album_wrong(album):
    if is_wrong_text_in_album(album):
        return True
    return False


def create_title(file_name):
    name = file_name.replace('.mp3', '').split('-')[-1].strip()
    if is_number_in_front_of_text(name):
        name = ' '.join(name.split(' ')[1:])
    if name == '':
        name = ' '.join(file_name.replace('.mp3', '').split('-')[1:])
    return name.strip()


def create_album(folder):
    album_name = ''
    sub_folders = folder.split(os.sep)
    for sub_folder in sub_folders:
        if 'guaira' in sub_folder.lower():
            album_name = sub_folder
            break
        elif 'gramado' in sub_folder.lower():
            album_name = sub_folder
            break

    if album_name == '':
        album_name = sub_folders[-1]

    album_name = album_name.replace('Músicas', '').strip()
    return album_name


def rename_mp3_files(location):
    for root, dirs, files in os.walk(location):
        for m_file in files:
            if m_file.endswith('.mp3'):
                mp3_file = os.path.join(root, m_file)
                mp3 = eyed3.load(mp3_file)
                try:
                    if mp3.tag is None:
                        mp3.tag = Tag()
                        mp3.tag.save()
                    title = mp3.tag.title if mp3.tag.title is not None else 'None'
                    album = mp3.tag.album if mp3.tag.album is not None else 'None'
                    changed = False
                    if is_title_wrong(title):
                        title = create_title(m_file)
                        mp3.tag.title = title
                        changed = True
                    if is_album_wrong(album):
                        album = create_album(root)
                        mp3.tag.album = album
                        changed = True
                    if changed:
                        mp3.tag.save()
                    if is_number_in_front_of_text(m_file):
                        new_filename = title.replace('/', '-').replace('\\', '-')+'.mp3'
                        new_filepath = os.path.join(root, new_filename)
                        os.rename(mp3_file, new_filepath)
                        # print('File:{}, \t\t\ttitle:{}, \talbum:{}'.format(mp3_file, title, album))
                except AttributeError:
                    print('File:{}, \t\t\tERRO NO ARQUIVO'.format(mp3_file))


if __name__ == '__main__':
    start_folder = "/home/edras/MusicTest"
    rename_mp3_files(start_folder)


