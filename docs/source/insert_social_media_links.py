import os

THIS_DIR = os.path.dirname(__file__)


if __name__ == '__main__':
    index_html_path = os.path.join(THIS_DIR, '..', 'index.html')
    social_media_html_path = os.path.join(THIS_DIR, 'social_media.html')

    social_media_html = open(social_media_html_path).read()
    index_html = open(index_html_path).read()

    # add social media links
    index_html = index_html.replace('#social-media#', social_media_html)

    # change code snippet sidebar width
    index_html = index_html.replace(
        '<div class="sidebar">', '<div class="sidebar" style="width: 55%;">')

    with open(index_html_path, 'w') as f:
        f.write(index_html)
