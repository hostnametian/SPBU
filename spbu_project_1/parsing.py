"""Handlers for txt, docx, pdf."""

from io import StringIO
from typing import List

from bs4 import BeautifulSoup
from docx import Document
from pdfminer3.converter import TextConverter
from pdfminer3.layout import LAParams
from pdfminer3.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer3.pdfpage import PDFPage


def paginate(list_of_paragraphs: list, max_page_length=5000) -> List[List]:
    """Split list of paragraphs into pages.
    Args:
        list_of_paragraphs: List of paragraphs.
        max_page_length: Approximate length of pages. Maximum number of characters for
            one page.
    Returns:
        List of pages.
    """

    '''
    将段落列表分成几页
     Args：
         list_of_paragraphs：段落列表
         max_page_length：大约页面的数量
     Returns：
         页面列表
    '''
    pages = []
    one_page = []
    page_len = 0
    for par in list_of_paragraphs:
        if page_len >= max_page_length:
            pages.append(one_page)
            one_page = []
            page_len = 0
        one_page.append(par)
        page_len += len(par)
    else:
        pages.append(one_page)
    return pages


def split_txt(file_content: str) -> List[List]:
    """Split text to pages.
    Args:
        file_content (str): file content
    Returns:
        list of pages.
    """

    '''
    将文本拆分为页面。
     args：
         file_content（str）：文件内容
     returns：
         页面列表
    '''

    return paginate(file_content.split("\n"))


def load_docx(file_path: str) -> List[List]:
    """Load a docx file and split document to pages.
    Args:
        file_path: path to docx file.
    Returns:
        list of pages.
    """

    '''
    加载docx文件并将文档拆分为页面。
     args：
         file_path：docx文件的路径。
     returns：
         页面清单
    '''
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return paginate(full_text)


def split_html(raw_html: str) -> List[List]:
    """Split html content to pages.
    Args:
        raw_html: html content
    Returns:
        list of pages
    """

    '''
    将html内容拆分为页面。
     args：
         raw_html：html内容
     return：
         页面清单
    '''
    soup = BeautifulSoup(raw_html, features="lxml")
    [s.extract() for s in soup(["style", "script", "head", "title", "meta", "[document]"])]
    # replace non-breaking space
    # 替换不间断空间
    soup = soup.get_text(strip=False).replace("\xa0", " ")
    lines = [line.strip() for line in soup.splitlines() if line.strip()]
    return paginate(lines)


def pdfminer_parser(path) -> List:
    """Load a PDF file and split document to pages.
    Args:
        pdf: PDF file or path to file
    Returns:
        list of pages.
    """

    '''
    加载PDF文件并将文档拆分为页面。
     args：
         pdf：PDF文件或文件路径
     returns：
         页面列表。
    '''
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    device = TextConverter(rsrcmgr, retstr, codec="utf-8", laparams=LAParams())
    list_of_pages = []
    with open(path, "rb") as pdf_file:
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos = set()

        for page in PDFPage.get_pages(
            pdf_file,
            pagenos,
            maxpages=maxpages,
            password=password,
            caching=caching,
            check_extractable=True,
        ):
            read_position = retstr.tell()
            interpreter.process_page(page)
            retstr.seek(read_position, 0)
            page_text = retstr.read()
            list_of_pages.append(page_text)
    device.close()
    retstr.close()
    return list_of_pages