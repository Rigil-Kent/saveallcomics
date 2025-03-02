import os
from shutil import copyfile
from flask import render_template, session, redirect, url_for, flash, request, current_app
from . import main
from .forms import Ripper
from .. import db
from flask_login import current_user, login_required
from ..panelrip import ripper, zipper


accepted_methods = ['GET', 'POST']
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}


def download_comic_files(soup):
    # create list for comic file links
    comic_files = []

    # set the image_folder name to the title of the comic
    image_folder = os.path.join(current_app.config['DOWNLOAD_FOLDER'], ripper.get_title(soup))
    print(image_folder)

    # append each comic link found in the bs4 response to the comic file list
    for link in ripper.get_img_links(soup):
        comic_files.append(link)

    # download the completed comic list
    ripper.download_img_links(comic_files, soup, current_app.config['DOWNLOAD_FOLDER'])

    # create a comic archive from all images in image_folder
    zipper.create_comic_archive(ripper.get_title(soup), image_folder)

    # copy comic to stash
    print('Copying comic to personal stash')
    filename = ripper.get_title(soup) + '.cbr'
    src = str(os.path.join(image_folder, filename))
    print(src)
    dest = str(os.path.join(current_app.config['STASH_FOLDER'], filename))
    print(dest)
    copyfile(src, dest)
    


@main.route('/', methods=accepted_methods)
def index():
    form = Ripper()

    if form.validate_on_submit():
        soup = ripper.get_soup_obj(form.search.data, headers)
        download_comic_files(soup)
        title = ripper.get_title(soup)
        cover = title + ' 000.jpg'
        return render_template('success.html', title=title, cover=cover)

    return render_template('index.html', form=form)