import pubchempy as pcp
import requests
import random
import ssl
from urllib.request import urlopen
from urllib.parse import quote
from bs4 import BeautifulSoup
from tqdm import tqdm
import time
import pandas as pd
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


user_agent = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    ]
ssl._create_default_https_context = ssl._create_unverified_context

def CIRconvert(name):
    try:
        url = 'http://cactus.nci.nih.gov/chemical/structure/' + quote(name) + '/smiles'
        ans = urlopen(url).read().decode('utf8')
    except:
        ans = ''
    return ans

def smiles2cas(smiles):
    # SMILES-to-CAS Author: Buckwheat
    cid_for_smiles = pcp.get_compounds(smiles, "smiles")[0].cid
    url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/%s/JSON/?heading=CAS" % cid_for_smiles
    response = requests.get(url, headers={'User-Agent': random.choice(user_agent), "connection": "close"}, timeout=5,
                            verify=False)
    cas_num = response.json()['Record']['Section'][0]['Section'][0]['Section'][0]["Information"][0]['Value'][
        'StringWithMarkup'][0]['String']

    return cas_num.split(';')[0]

def cas2msds(sml, cas_number=False):
    if cas_number == False:
        cas = smiles2cas(sml)
    else:
        cas = sml
    url = f'https://www.chemsrc.com/searchResult/{cas}/'
    # data = {'chemSearch': cas}
    # response = requests.post(url, data=data, headers={'User-Agent': random.choice(user_agent), "connection": "close"},
    #                          timeout=5, verify=False)
    response = requests.get(url, headers={'User-Agent': random.choice(user_agent), "connection": "close"}, timeout=5,
                            verify=False)  
    # print(response.text[20000:40000])
    soup = BeautifulSoup(response.text, 'lxml')
    name = soup.find('title').text
    name = name[:name.find('_MSDS')]
    all_strong = soup.select('strong', class_='msds_title')
    all_strong = [i for i in all_strong if i.text.split('.')[0][2] in [str(j) for j in range(17)]]
    # print(soup.find_all(['strong'])[0:1])
    props = {'cas': cas, 'name': name}
    for strong in all_strong:
        props[strong.text] = []
        for sibling in strong.next_siblings:
            if sibling in all_strong or 'msds_title' in str(sibling) or 'hr' in str(sibling):
                props[strong.text] = ''.join(props[strong.text])
                break
            if len(str(sibling)) >= 3:
                props[strong.text].append(str(sibling).replace('<b>', '').replace('</b>', '').replace('<br/>', '').rstrip('\n'))
                if '<b>' in str(sibling):
                    pass# props[strong.text].append('\n')
    # print(props)
    return props

if __name__ == '__main__':
    # smiles = ["CC(C)(C(=O)Br)Br", '10061-68-4', 'Semicarbazide hydrochloride']
    smiles = open('msds_input.txt').readlines()
    msds = []
    for sml in tqdm(smiles):
        if CIRconvert(sml) != '':
            msds.append(cas2msds(CIRconvert(sml)))
        elif sml.upper() == sml.lower():
            msds.append(cas2msds(sml, cas_number=True))
        else:
            msds.append(cas2msds(sml))
    df = pd.DataFrame(msds)
    df.to_csv('msds_'+time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time()))+'.csv', index=None, encoding='utf_8_sig')
