import requests, re, csv, tqdm
from lxml import etree
from multiprocessing import Pool


def create_csv():
    '''
    创建保存数据的 csv
    :return:
    '''
    with open('../output/urls.csv','w',newline='',encoding='utf8') as f:
        wr = csv.writer(f)
        wr.writerow(['链接'])

def get_html(url):
    '''
    获取 html 页面
    :param url:
    :return:
    '''
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
    }
    response = requests.get(url,headers=headers)
    response.encoding = 'utf8'
    return response.text

def get_page():
    '''
    获得需要爬取的总页数
    :return:
    '''
    url = 'http://www.maomijiaoyi.com/index.php?/chanpinliebiao_c_2_1--24.html'
    html = get_html(url)
    page = re.findall('共.*?条 1/(.*?)页',html,re.S)[0]
    page = int(page)
    return page

def get_url(pg,page):
    '''
    获得此页所有交易猫猫的链接
    :param pg:
    :return:
    '''
    print('正在爬取 %s 页，共 %s 页' % (str(pg),str(page)))
    url = 'http://www.maomijiaoyi.com/index.php?/chanpinliebiao_c_2_{}--24.html'.format(str(pg))
    html = get_html(url)
    html = etree.HTML(html)

    urls = html.xpath('//div[@class="content"]/a/@href')
    urls = ['http://www.maomijiaoyi.com'+url for url in urls][:-2]

    write_to_csv(urls)

def write_to_csv(urls):
    '''
    保存进 csv
    :param infos:
    :return:
    '''
    urls = [[url] for url in urls]
    with open('../output/urls.csv','a+',newline='',encoding='utf8') as f:
        wr = csv.writer(f)
        wr.writerows(urls)

if __name__ == '__main__':
    # 创建保存数据的文件
    create_csv()
    # 获得总页数
    page = get_page()
    # 多进程爬取
    p = Pool()
    for pg in range(page):
        p.apply_async(get_url,args=(pg+1,page))
    p.close()
    p.join()