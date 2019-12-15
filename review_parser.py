from lxml import html as lh
from lxml import etree
from urllib.parse import urlparse
from requests import get


# Data archive
#Structure: [ [" Customer name", "Rate", "Date", "TitleReview", "TextReview"], [...], ...]
dater = []

def get_ua():
    header = {'User-agent': 'Mozilla/5.0'}
    return header

def url_formatter(url):
    """ Function of formatting the link of the goods, to the link of reviews of the Amazon
    :parm url - Amazon product link """

    purl = urlparse(url)
    newpath = purl.path.replace('/dp', "/product-reviews")
    ref_find = newpath.find("ref=")
    if (ref_find != -1):
        newpath = newpath[0:ref_find]
    return purl.scheme+"://"+purl.netloc+newpath

#Base parse funck :parm url -
def parse(url, page=1):
    """The main function of the parser Amazon reviews
    :parm url  - formated review link,
    :parm page=1 - deff parm,  for parse multipage reviews"""

    counter = 0

    print(f"Processing page в„– {page} ...")
    result = get(url, headers=get_ua())
    tree  = lh.document_fromstring(result.text)
    table_node = tree.xpath("//div[contains(@class, 'a-section review aok-relative')]")
    for node in table_node:
        counter += 1
        enode = node.xpath(".//text()")
        buyer = enode[0]
        rate  = enode[1]
        date  = enode[4]
        title_node = node.xpath(".//a[contains(@class, 'review-title')]")[0].xpath(".//text()")
        text_node = node.xpath(".//span[contains(@class, 'review-text')]")[0].xpath(".//text()")
        title = clear_str(" ".join(title_node))
        text  = clear_str(" ".join(text_node))
        dater.append([buyer, rate, date, title, text])
    if counter == 10:
        parse(f"{url_formatter(url)}ref=cm_cr_getr_d_paging_btm_next_{page+1}?pageNumber={page+1}", page+1)

def clear_str(str, optional = None):
    """Utility function to clean the line from garbage
    :parm str - any string,
    :parm optional=None(Type: list) - def parm , to describe additional trash signs"""

    chars = ['\t', '\n', '\r', '   ']
    if (optional):
        chars = list(set(chars + optional))
    str.strip()
    for char in chars:
        str =  str.replace(char, "")
    return str
