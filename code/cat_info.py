import requests, re, csv
import pandas as pd
from lxml import etree
from multiprocessing import Pool


def create_csv():
    '''
    创建保存数据的 csv
    :return:
    '''
    with open('../output/cat_info.csv','w',newline='',encoding='utf8') as f:
        wr = csv.writer(f)
        wr.writerow(['地区','商家名称','标题','价格','浏览次数','卖家承诺','在售只数','年龄',
                     '品种','预防','联系人','联系电话','异地运费','是否纯种',
                     '猫咪性别','驱虫情况','猫咪年龄','能否视频','链接'])


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


def get_info(url,i,l):
    '''
    提取此页中每一只猫猫的交易信息
    :param urls:
    :return:
    '''
    print('第 %s 条，共 %s 条' % (str(i),str(l)))
    info = []
    html = get_html(url)
    # 地区
    html1 = etree.HTML(html)
    area = html1.xpath('//div[@class="bread_crumb"]/a/span/text()')[2:4]
    area = '/'.join(area)
    # 商家名称
    shopName = re.findall('<div class="name" style="margin-top: 0;">(.*?)</div>',html,re.S)[0]
    shopName = shopName.replace('\r','').replace('\n','').strip()
    # 标题
    title = re.findall('<title>(.*?)</title>',html,re.S)[0]
    # 价格
    price = re.findall('<span>价格</span>.*?<span class="red size_24">(.*?)<span>元/只</span></span>',html,re.S)[0]
    # 浏览次数
    view = re.findall('<span>浏览次数:</span>.*?<span class="red">(.*?)</span>',html,re.S)[0]
    # 卖家承诺
    promise = re.findall('<span class="red">卖家承诺: (.*?)</span>',html,re.S)[0]
    # 在售只数
    saleNum = re.findall('<div>在售只数</div>.*?<div class="red">(.*?)</div>',html,re.S)[0]
    # 年龄
    age = re.findall('<div>年龄</div>.*?<div class="red">(.*?)</div>', html, re.S)[0]
    # 品种
    kind = re.findall('<div>品种</div>.*?<div class="red">(.*?)</div>', html, re.S)[0]
    # 预防
    prevent = re.findall('<div>预防</div>.*?<div class="red">(.*?)</div>', html, re.S)[0]
    # 联系人
    linkman = re.findall('<div class="c999">联系人　:</div>.*?<div class="c333">(.*?)</div>', html, re.S)[0]
    # 联系电话
    linkphone = re.findall('<div class="c999">联系电话:</div>.*?<div class="c333">(.*?)</div>', html, re.S)[0]
    # 异地运费
    freight = re.findall('<div class="c999">异地运费:</div>.*?<div class="c333">(.*?)</div>', html, re.S)[0]
    freight = freight.replace('\r','').replace('\n','').strip()
    # 是否纯种
    purebred = re.findall('<div>.*?是否纯种: <span class="c333">(.*?)</span>.*?</div>', html, re.S)[0]
    purebred = purebred.replace('\r','').replace('\n','').strip()
    # 猫咪性别
    sex = re.findall('<div>.*?猫咪性别: <span class="c333">(.*?)</span>.*?</div>', html, re.S)[0]
    sex = sex.replace('\r','').replace('\n','').strip()
    # 驱虫情况
    expelling = re.findall('<div>.*?疫苗情况: <span class="c333">(.*?)</span>.*?</div>', html, re.S)[0]
    expelling = expelling.replace('\r', '').replace('\n', '').strip()
    # 猫咪年龄
    age = re.findall('<div>.*?猫咪年龄: <span class="c333">(.*?)</span>.*?</div>', html, re.S)[0]
    age = age.replace('\r', '').replace('\n', '').strip()
    # 能否视频
    vedio = re.findall('<div>.*?能否视频: <span class="c333">(.*?)</span>.*?</div>', html, re.S)[0]
    vedio = vedio.replace('\r', '').replace('\n', '').strip()

    # 保存进列表
    info.append([area,shopName,title,price,view,promise,saleNum,age,kind,prevent,
                     linkman,linkphone,freight,purebred,sex,expelling,
                     age,vedio,url])

    # 保存
    write_to_csv(info)


def write_to_csv(infos):
    '''
    保存进 csv
    :param infos:
    :return:
    '''
    with open('../output/cat_info.csv','a+',newline='',encoding='utf8') as f:
        wr = csv.writer(f)
        wr.writerows(infos)


if __name__ == '__main__':
    # 创建保存数据的文件
    create_csv()
    # 读取需要爬取的 url
    df = pd.read_csv('../output/urls.csv')
    urls = list(df['链接'])
    l = len(urls)
    # 多进程爬取
    p = Pool()
    for i in range(49303,l):
        p.apply_async(get_info,args=(urls[i],i+1,l))
    p.close()
    p.join()

