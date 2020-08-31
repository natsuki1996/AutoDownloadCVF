# -*- coding: utf-8 -*-

import os
from time import sleep

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

conf = 'CVPR2020'
header = 'http://openaccess.thecvf.com/'

urls = [
    'https://openaccess.thecvf.com/CVPR2020?day=2020-06-16',
    'https://openaccess.thecvf.com/CVPR2020?day=2020-06-17',
    'https://openaccess.thecvf.com/CVPR2020?day=2020-06-18',
]


def name_check(name):
    name = name.replace('?', '')
    name = name.replace(':', '')
    name = name.replace('*', '')
    name = name.replace('/', ' or ')
    return name


def main():
    if not os.path.exists(conf):
        os.mkdir(conf)

    paper_url, paper_title = list(), list()
    for url in urls:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')

        paper_info = [link.get('href') for link in soup.select('dd a') if link.get_text() == 'pdf']
        paper_url += [header + link for link in paper_info]
        paper_title += [name_check(link.split('/')[-1]) for link in paper_info]

    assert len(paper_url) == len(paper_title)

    for ptitle, purl in tqdm(zip(paper_title, paper_url), total=len(paper_title)):
        tqdm.write("save " + ptitle + " ...")
        pdfname = conf + '/' + ptitle
        if not os.path.exists(pdfname):
            r = requests.get(purl)
            with open(pdfname, 'wb') as f:
                f.write(r.content)


if __name__ == '__main__':
    main()
