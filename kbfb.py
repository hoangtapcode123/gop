# Code by KhoiHuynh1109!
# Contact Me:
    # -> @khoilulbadao (Telegram)
    # -> valerie.alvares (Facebook)
# Thanks For Using !
# Delete these lines or you will be a dog
LIBRARIES = ["requests", "rich", "pystyle"]
for LIB in LIBRARIES:
    try:
        __import__(LIB)
    except ImportError:
        print(f"Đang tiến hành install thư viện: [{LIB}]")
        try:
            start_time = __import__('time').time()
            process = __import__('subprocess').Popen(["pip", "install", LIB], stdout=__import__('subprocess').PIPE, stderr=__import__('subprocess').PIPE)
            while True:
                return_code = process.poll()
                if return_code is not None:
                    if return_code == 0:
                        print()
                        print(f"Success .. [{LIB}]")
                    else:
                        print()
                        print(f"Failure .. {LIB}. Vui lòng thử lại sau.")
                        print(process.stderr.read().decode())
                    break
                current_time = __import__('time').time()
                elapsed_time = current_time - start_time
                print(f"Installing {LIB}... [{elapsed_time:.2f}s]", end='\\r')
                __import__('time').sleep(0.1)
        except Exception as e:
            print(f"Đã xảy ra lỗi khi cài đặt {LIB}: {e}")
            __import__('sys').exit(1)

import requests, re, os, time, threading
from pystyle import *
from rich.table import Table
from rich.console import Console
from rich.live import Live
from rich.text import Text

class KhoiHuynh:
    def __init__(self):
        self.list_cookie = []
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'vi-VN,vi;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-AU;q=0.6,en;q=0.5,fr-FR;q=0.4,fr;q=0.3,en-US;q=0.2',
            'cache-control': 'max-age=0',
            'dpr': '1.875',
            'sec-ch-prefers-color-scheme': 'light',
            'sec-ch-ua': '"Not:A-Brand";v="99", "Chromium";v="112"',
            'sec-ch-ua-full-version-list': '"Not:A-Brand";v="99.0.0.0", "Chromium";v="112.0.5615.135"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-model': '"SM-A037F"',
            'sec-ch-ua-platform': '"Android"',
            'sec-ch-ua-platform-version': '"12.0.0"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Mobile; rv:48.0; A405DL) Gecko/48.0 Firefox/48.0 KAIOS/2.5',
            'viewport-width': '980',
        }
        self.params = {
            'fb_ref': 'tn',
            'sr': '1',
            'paipv': '0',
            'ref_component': 'mbasic_home_header',
            'ref_page': '/wap/home.php',
            'refid': '7',
        }
        self.dict_friends = {}
        self.ki_tu = '\033[1;94m[\033[1;37m</>\033[1;94m]'
        self.delay = None
        self.table = None

    def check_live(self, cookies):
        cookies = {'cookie': cookies}
        check = requests.get('https://mbasic.facebook.com/profile', headers=self.headers, cookies=cookies).text
        if 'profile_id=' in check:
            name = check.split('<title>')[1].split('</title>')[0]
            profile_id = check.split('profile_id=')[1].split('&')[0]
            return name, profile_id
        return False

    def get_list_fr(self, cookies):
        cookies = {'cookie': cookies}
        get_fr = response = requests.get('https://mbasic.facebook.com/friends/center/mbasic/', params=self.params, headers=self.headers, cookies=cookies).text
        return get_fr

    def findall_all(self, cookies):
        rps = self.get_list_fr(cookies)
        table = Table(title_style='bold yellow', show_lines=True, style="bold white")
        table.add_column('STT', width=3, justify='center', style="bold white")
        table.add_column('NAME', width=20, justify='center', style="bold white")
        table.add_column('UID', width=15, justify='center', style="bold white")
        table.add_column("STATUS", width=20, justify='center')

        c = re.findall(r'">([^<]+)<\/a>(?:<div class="[^"]*">[^<]*<\/div>)?(?:<div class="[^"]*">)?<table class="m"><tbody><tr><td class="t"><div><a href="\/a\/friends\/add\/', rps)
        print(c)
        b = re.findall(r'href="\/a\/friends\/add\/(.*?)"', rps)
        id = [x.split('subject_id=')[1].split('&')[0] for x in b]
        table.title = f"Tìm thấy {len(b)} bạn bè gợi ý"
#        v = [f'Name: {c[i]} | Uid: {id[i]}' for i in range(len(b))]
        #print(''.join(v))
        for i in range(len(b)):
            href = b[i].replace('amp;', '')
            uid = id[i]
            table.add_row(str(i+1), c[i], uid, "[bold yellow]ĐANG XỬ LÝ[/bold yellow]")
            self.dict_friends[c[i]] = {'href': href, 'uid': uid}
        #Console().print(table)
        self.table = table
        return
        #print(self.dict_friends)

    def kb_fr(self, cookies):
        self.findall_all(cookies)
        cookies = {'cookie': cookies}
        with Live(self.table, console=Console(), screen=False, auto_refresh=False) as live:
            for i, (name, dict_kb) in enumerate(self.dict_friends.items()):
                href = dict_kb['href']
                #print('Đang Kb Với %s | Uid: %s' % (name, uid))
                kb = requests.get(f'https://mbasic.facebook.com/a/friends/add/{href}', headers=self.headers, cookies=cookies).text
                check = re.search(fr'{name}</a>(?:<div class="[^"]*">)?Đã gửi lời mời', kb)
                if check:
                    #print('Kb Thành Công Với %s | Uid: %s' % (name, uid))
                    status = "[bold green]KẾT BẠN THÀNH CÔNG[/bold green]"
                else:
                    status = "[bold red]KẾT BẠN THẤT BẠI[/bold red]"
                    #print('Kb Không Thành Công Với %s | Uid: %s' % (name, uid))
                self.table.columns[3]._cells[i] = status
                live.update(self.table, refresh=True)
                time.sleep(self.delay)
            self.dict_friends.clear()

    def cls_system(self):
        os.system('cls' if os.system == 'nt' else 'clear')
        banners = '''
 ██░ ██  ██ ▄█▀▄▄▄█████▓ ▒█████   ▒█████   ██▓    
▓██░ ██▒ ██▄█▒ ▓  ██▒ ▓▒▒██▒  ██▒▒██▒  ██▒▓██▒    
▒██▀▀██░▓███▄░ ▒ ▓██░ ▒░▒██░  ██▒▒██░  ██▒▒██░    
░▓█ ░██ ▓██ █▄ ░ ▓██▓ ░ ▒██   ██░▒██   ██░▒██░    
░▓█▒░██▓▒██▒ █▄  ▒██▒ ░ ░ ████▓▒░░ ████▓▒░░██████▒
▒ ░░▒░▒▒ ▒▒ ▓▒  ▒ ░░   ░ ▒░▒░▒░ ░ ▒░▒░▒░ ░ ▒░▓  ░
▒ ░▒░ ░░ ░▒ ▒░    ░      ░ ▒ ▒░   ░ ▒ ▒░ ░ ░ ▒  ░
░  ░░ ░░ ░░ ░   ░      ░ ░ ░ ▒  ░ ░ ░ ▒    ░ ░   
░  ░  ░░  ░                ░ ░      ░ ░      ░  ░
       Huynh Minh Khoi x Vu Cong Huy Hoang\n\n'''
        purple = Colors.StaticMIX((Col.purple, Col.blue))
        dark = Col.dark_gray
        print(Colorate.Diagonal(Colors.DynamicMIX((purple, dark)), Center.XCenter(banners)))


    def setting_kb(self):
        vtan = input(self.ki_tu + " \033[1;37mBạn có muốn vòng lặp vô tận không? Y/n: ").lower()
        if vtan == 'y':
            while 1:
                try:
                    self.delay = int(input(self.ki_tu + " \033[1;37mNhập delay kết bạn (NÊN ĐẶT CAO) [Số]: "))
                    break
                except Exception as e:
                    print(e)
            while 1:
                for i, cookie in enumerate(self.list_cookie):
                    print(self.ki_tu, f"\033[1;37mĐang dùng cookie thứ {i+1}")
                    self.kb_fr(cookie)
        else:
            while 1:
                try:
                    solan = int(input(self.ki_tu + " \033[1;37mNhập số vòng lặp muốn kết bạn [Số]: "))
                    break
                except Exception as e:
                    print(e)
            while 1:
                try:
                    self.delay = int(input(self.ki_tu + " \033[1;37mNhập Delay Kết Bạn (Nên Đặt Cao) [Số]: "))
                    break
                except Exception as e:
                    print(e)
            for x in range(solan):
                for i, cookie in enumerate(self.list_cookie):
                    print(self.ki_tu, f"\033[1;37mĐang dùng cookie thứ {i+1}")
                    self.kb_fr(cookie)

    def main(self):
        self.cls_system()
        if os.path.exists('COOKIES_HK.txt'):
            total = open('COOKIES_HK.txt', 'r', encoding='utf-8').readlines()
            hihi = input(self.ki_tu+f" \033[1;37mBạn đã có file cookie chứa {len(total)} cookies trong máy?\nDùng lại hay không? Y/n: ").lower()
            if hihi == 'y':
                self.list_cookie = [tt.strip('\n') for tt in total]
            else:
                nhapxoa = input(self.ki_tu+"Bạn muốn nhập hoặc xoá cookie nào không? [N] Nhập - [X] Xoá: ").lower()
                if nhapxoa == 'n':
                    cookie = input(self.ki_tu+ " \033[1;37mNhập cookie: ")
                    self.list_cookie = [tt.strip('\n') for tt in total]
                    self.list_cookie.append(cookie)
                    os.remove('COOKIES_HK.txt')
                    for cookie in self.list_cookie:
                        open('COOKIES_HK.txt', 'a', encoding='utf-8').write(cookie + "\n")
                elif nhapxoa == 'x':
                    self.list_cookie = [tt.strip('\n') for tt in total]
                    for i, cookie in enumerate(self.list_cookie):
                        print(f"{i+1}. {cookie}")
                    while 1:
                        try:
                            xoa = int(input(self.ki_tu + " \033[1;37mBạn muốn xoá cookie thứ mấy? (Số): ")) - 1
                            break
                        except Exception as e:
                            print(e)
                    self.list_cookie.pop(xoa)
                    os.remove('COOKIES_HK.txt')
                    for cookie in self.list_cookie:
                        open('COOKIES_HK.txt', 'a', encoding='utf-8').write(cookie + "\n")
                else:
                    teo = input(self.ki_tu+f" \033[1;37mBạn muốn xoá file cookie không? Y/n: ").lower()
                    if teo == 'y':
                        os.remove('COOKIES_HK.txt')
                        exit("Khởi động lại tool")
            ckk = input(self.ki_tu + " \033[1;37mBạn có muốn check lại cookie không? Y/n: ").lower()
            if ckk == 'y':
                for cookie in self.list_cookie:
                    check = self.check_live(cookie)
                    if not check:
                        self.list_cookie.remove(cookie)
                        print(self.ki_tu, f"\033[1;31mCookie {cookie} Die Và Đã Xoá Khỏi Danh Sách")
                    else:
                        print(self.ki_tu, f"\033[1;37mCookie Live! Name: {check_ck[0]} | Uid: {check_ck[1]}")
                os.remove('COOKIES_HK.txt')
                for cookie in self.list_cookie:
                    open('COOKIES_HK.txt', 'a', encoding='utf-8').write(cookie + "\n")
            else:
                self.setting_kb()
        else:
            dacookie = input(self.ki_tu+" \033[1;37mBạn có muốn đa cookie hay không? Y/n: ").lower()
            if dacookie == 'y':
                print(self.ki_tu, "\033[1;33m[ENTER ĐỂ NGỪNG NHẬP]")
                i_ck = 1
                while True:
                    cookie = input(self.ki_tu + f" \033[1;37mNhập cookie thứ [{i_ck}]: ")
                    if cookie == '':
                        break
                    check_ck = self.check_live(cookie)
                    if not check_ck:
                        print(self.ki_tu, "\033[1;31mCookie Thứ [{i_ck}] Die Vui Lòng Thử Lại")
                    else:
                        print(self.ki_tu, f"\033[1;37mCookie Live! Name: {check_ck[0]} | Uid: {check_ck[1]}")
                        self.list_cookie.append(cookie)
                        i_ck += 1
                save = input(self.ki_tu + " \033[1;37mBạn có muốn lưu cookie vào file không? Y/n: ").lower()
                if save == 'y':
                    for cookie in self.list_cookie:
                        open('COOKIES_HK.txt', 'a', encoding='utf-8').write(cookie + "\n")
                self.setting_kb()
           # if not os.path.exists()
            else:
                cookie = input(self.ki_tu + " \033[1;37mNhập cookie: ")
                check_ck = self.check_live(cookie)
                if not check_ck:
                    print(self.ki_tu, "\033[1;31mCookie Die Vui Lòng Thử Lại")
                else:
                    print(self.ki_tu, f"\033[1;37mCookie Live! Name: {check_ck[0]} | Uid: {check_ck[1]}")
                    self.list_cookie.append(cookie)
                save = input(self.ki_tu + " \033[1;37mBạn có muốn lưu cookie vào file không? Y/n: ").lower()
                if save == 'y':
                    open('COOKIES_HK.txt', 'a', encoding='utf-8').write(cookie + "\n")
                self.setting_kb()

KhoiHuynh().main()