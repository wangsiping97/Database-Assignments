import requests
from bs4 import BeautifulSoup
from urllib import parse

def loggedSession(username, password):
    # 传入网络学堂的用户名和密码，返回一个已登录的 session
    res = requests.get("http://learn.tsinghua.edu.cn/f/login")
    soup = BeautifulSoup(res.text, "html.parser")
    data = {'i_user': username, 'i_pass': password, 'atOnce': 'true'}
    url = soup.find('form', attrs={'id':'loginForm'})['action']
    session = requests.Session()
    res = session.post(url,data=data)
    soup = BeautifulSoup(res.text, "html.parser")
    url = soup.find('a')['href']
    try:
        ticket = parse.parse_qs(parse.urlparse(url).query)['ticket'][0]
    except:
        raise Exception('无效的用户名或密码！')
    res = session.get('http://learn.tsinghua.edu.cn/b/j_spring_security_thauth_roaming_entry?ticket='+ticket)
    # res = session.get('http://learn.tsinghua.edu.cn/f/wlxt/common/courseSearch')
    return session