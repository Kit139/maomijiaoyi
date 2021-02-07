import requests, re, csv
from lxml import etree
from tqdm import tqdm


def create_csv():
    '''
    创建保存数据的 csv
    :return:
    '''
    with open('../output/cat_kind.csv','w',newline='',encoding='utf8') as f:
        wr = csv.writer(f)
        wr.writerow(['品种','参考价格','中文学名','别名','祖先','分布区域',
                     '原产地','体型','原始用途','今日用途','分组','身高',
                     '体重','寿命','整体','毛发','颜色','头部','眼睛',
                     '耳朵','鼻子','尾巴','胸部','颈部','前驱','后驱',
                     '基本信息','FCI标准','性格特点','生活习性','优点/缺点',
                     '喂养方法','鉴别挑选'])

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

def get_kind_url(html):
    '''
    提取所有品种 url
    :param html:
    :return:
    '''
    html = etree.HTML(html)
    infos = html.xpath('//div[@class="pinzhong_left"]/a')
    urls = []
    for info in infos:
        url = info.xpath('./@href')[0]
        url = 'http://www.maomijiaoyi.com' + url
        urls.append(url)
    return urls

def get_info(html):
    '''
    提取猫猫品种详情信息
    :param html:
    :return:
    '''
    # 品种
    kind = re.findall('div class="line1">.*?<div class="name">(.*?)<span>',html,re.S)[0]
    kind = kind.replace('\r','').replace('\n','').replace('\t','')
    # 参考价格
    price = re.findall('<div>参考价格：</div>.*?<div>(.*?)</div>',html,re.S)[0]
    price = price.replace('\r', '').replace('\n', '').replace('\t', '')
    # 中文学名
    chineseName = re.findall('<div>中文学名:</div>.*?<div>(.*?)</div>',html,re.S)[0]
    chineseName = chineseName.replace('\r', '').replace('\n', '').replace('\t', '')
    # 别名
    otherName = re.findall('<div>别名:</div>.*?<div>(.*?)</div>',html,re.S)[0]
    otherName = otherName.replace('\r', '').replace('\n', '').replace('\t', '')
    # 祖先
    ancestor = re.findall('<div>祖先:</div>.*?<div>(.*?)</div>',html,re.S)[0]
    ancestor = ancestor.replace('\r', '').replace('\n', '').replace('\t', '')
    # 分布区域
    area = re.findall('<div>分布区域:</div>.*?<div>(.*?)</div>',html,re.S)[0]
    area = area.replace('\r', '').replace('\n', '').replace('\t', '')
    # 原产地
    sourceArea = re.findall('<div>原产地:</div>.*?<div>(.*?)</div>',html,re.S)[0]
    sourceArea = sourceArea.replace('\r', '').replace('\n', '').replace('\t', '')
    # 体型
    bodySize = re.findall('<div>体型:</div>.*?<div>(.*?)</div>', html, re.S)[0]
    bodySize = bodySize.replace('\r', '').replace('\n', '').replace('\t', '').strip()
    # 原始用途
    sourceUse = re.findall('<div>原始用途:</div>.*?<div>(.*?)</div>', html, re.S)[0]
    sourceUse = sourceUse.replace('\r', '').replace('\n', '').replace('\t', '')
    # 今日用途
    todayUse = re.findall('<div>今日用途:</div>.*?<div>(.*?)</div>', html, re.S)[0]
    todayUse = todayUse.replace('\r', '').replace('\n', '').replace('\t', '')
    # 分组
    group = re.findall('<div>分组:</div>.*?<div>(.*?)</div>', html, re.S)[0]
    group = group.replace('\r', '').replace('\n', '').replace('\t', '')
    # 身高
    height = re.findall('<div>身高:</div>.*?<div>(.*?)</div>', html, re.S)[0]
    height = height.replace('\r', '').replace('\n', '').replace('\t', '')
    # 体重
    weight = re.findall('<div>体重:</div>.*?<div>(.*?)</div>', html, re.S)[0]
    weight = weight.replace('\r', '').replace('\n', '').replace('\t', '')
    # 寿命
    lifetime = re.findall('<div>寿命:</div>.*?<div>(.*?)</div>', html, re.S)[0]
    lifetime = lifetime.replace('\r', '').replace('\n', '').replace('\t', '')
    # 整体
    entirety = re.findall('<div>整体</div>.*?<!-- 页面小折角 -->.*?<div></div>.*?<div>(.*?)</div>',html,re.S)[0]
    entirety = entirety.replace('\r', '').replace('\n', '').replace('\t', '').strip()
    # 毛发
    hair = re.findall('<div>毛发</div>.*?<div></div>.*?<div>(.*?)</div>', html, re.S)[0]
    hair = hair.replace('\r', '').replace('\n', '').replace('\t', '').strip()
    # 颜色
    color = re.findall('<div>颜色</div>.*?<div></div>.*?<div>(.*?)</div>', html, re.S)[0]
    color = color.replace('\r', '').replace('\n', '').replace('\t', '').strip()
    # 头部
    head = re.findall('<div>头部</div>.*?<div></div>.*?<div>(.*?)</div>', html, re.S)[0]
    head = head.replace('\r', '').replace('\n', '').replace('\t', '').strip()
    # 眼睛
    eye = re.findall('<div>眼睛</div>.*?<div></div>.*?<div>(.*?)</div>', html, re.S)[0]
    eye = eye.replace('\r', '').replace('\n', '').replace('\t', '').strip()
    # 耳朵
    ear = re.findall('<div>耳朵</div>.*?<div></div>.*?<div>(.*?)</div>', html, re.S)[0]
    ear = ear.replace('\r', '').replace('\n', '').replace('\t', '').strip()
    # 鼻子
    nose = re.findall('<div>鼻子</div>.*?<div></div>.*?<div>(.*?)</div>', html, re.S)[0]
    nose = nose.replace('\r', '').replace('\n', '').replace('\t', '').strip()
    # 尾巴
    tail = re.findall('<div>尾巴</div>.*?<div></div>.*?<div>(.*?)</div>', html, re.S)[0]
    tail = tail.replace('\r', '').replace('\n', '').replace('\t', '').strip()
    # 胸部
    chest = re.findall('<div>胸部</div>.*?<div></div>.*?<div>(.*?)</div>', html, re.S)[0]
    chest = chest.replace('\r', '').replace('\n', '').replace('\t', '').strip()
    # 颈部
    neck = re.findall('<div>颈部</div>.*?<div></div>.*?<div>(.*?)</div>', html, re.S)[0]
    neck = neck.replace('\r', '').replace('\n', '').replace('\t', '').strip()
    # 前驱
    fontFoot = re.findall('<div>前驱</div>.*?<div></div>.*?<div>(.*?)</div>', html, re.S)[0]
    fontFoot = fontFoot.replace('\r', '').replace('\n', '').replace('\t', '').strip()
    # 后驱
    rearFoot = re.findall('<div>前驱</div>.*?<div></div>.*?<div>(.*?)</div>', html, re.S)[0]
    rearFoot = rearFoot.replace('\r', '').replace('\n', '').replace('\t', '').strip()

    # 保存前面的猫猫属性
    cat = [kind,price,chineseName,otherName,ancestor,area,sourceArea,
           bodySize,sourceUse,todayUse,group,height,weight,lifetime,
           entirety,hair,color,head,eye,ear,nose,tail,chest,neck,
           fontFoot,rearFoot]

    # 提取标签栏信息（基本信息-FCI标准-性格特点-生活习性-优缺点-喂养方法-鉴别挑选）
    html = etree.HTML(html)
    labs = html.xpath('//div[@class="property_list"]/div')
    for lab in labs:
        text = lab.xpath('string(.)')
        text = text.replace('\n','').replace('\t','').replace('\r','').replace(' ','')
        cat.append(text)

    return cat

def write_to_csv(info):
    '''
    保存数据
    :param info:
    :return:
    '''
    with open('../output/cat_kind.csv','a+',newline='',encoding='utf8') as f:
        wr = csv.writer(f)
        wr.writerow(info)

if __name__ == '__main__':
    # 创建 csv
    create_csv()
    # 猫咪品种 url
    url = 'http://www.maomijiaoyi.com/index.php?/pinzhongdaquan_5.html'
    # 获取品种页面中的所有 url
    html = get_html(url)
    urls = get_kind_url(html)
    # 进度条
    pbar = tqdm(urls)
    # 开始爬取
    for url in pbar:
        html = get_html(url)
        info = get_info(html)
        write_to_csv(info)