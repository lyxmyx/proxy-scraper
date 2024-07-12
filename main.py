import os
import concurrent.futures
import sys
import time
import threading
import requests
from requests.exceptions import RequestException, SSLError, ReadTimeout
from pystyle import Write, System, Colors, Colorate, Anime
from colorama import Fore, Style
from datetime import datetime as dt
import ctypes
from proxy_links import http_links, socks5_links

try:
    import requests, colorama, pystyle, datetime, aiosocks, asyncio, aiohttp_socks, socks, socket, tls_client
except ModuleNotFoundError:
    os.system("pip install requests")
    os.system("pip install colorama")
    os.system("pip install pystyle")
    os.system("pip install datetime")
    os.system("pip install aiosocks")
    os.system("pip install asyncio")
    os.system("pip install aiohttp-socks")
    os.system("pip install socks")
    os.system("pip install tls_client")

from aiohttp_socks import ProxyConnector, ProxyType

https_scraped = 0
socks5_scraped = 0

http_checked = 0
socks5_checked = 0

red = Fore.RED
yellow = Fore.YELLOW
green = Fore.GREEN
blue = Fore.BLUE
orange = Fore.RED + Fore.YELLOW
pretty = Fore.LIGHTMAGENTA_EX + Fore.LIGHTCYAN_EX
magenta = Fore.MAGENTA
lightblue = Fore.LIGHTBLUE_EX
cyan = Fore.CYAN
gray = Fore.LIGHTBLACK_EX + Fore.WHITE
reset = Fore.RESET
pink = Fore.LIGHTGREEN_EX + Fore.LIGHTMAGENTA_EX
dark_green = Fore.GREEN + Style.BRIGHT
output_lock = threading.Lock()

def get_time_rn():
    date = dt.now()
    hour = date.hour
    minute = date.minute
    second = date.second
    timee = "{:02d}:{:02d}:{:02d}".format(hour, minute, second)
    return timee

def update_title(title):
    if os.name == 'nt':
        ctypes.windll.kernel32.SetConsoleTitleW(title)
    else:
        print(f'\33]0;{title}\a', end='', flush=True)

def update_title_scraped():
    global https_scraped, socks5_scraped
    title = f'[ Scraper ] HTTP/s Scraped : {https_scraped} ~ Socks5 Scraped : {socks5_scraped}'
    update_title(title)

def update_title_checked():
    global http_checked, socks5_checked
    title = f'[ Scraper ] HTTP/s Valid : {http_checked} ~ Socks5 Valid : {socks5_checked}'
    update_title(title)

def ui():
    update_title("[ Scraper ]")
    System.Clear()
    Write.Print(f"""
 ▄▄▄·▄▄▄        ▐▄• ▄  ▄· ▄▌    .▄▄ ·  ▄▄· ▄▄▄   ▄▄▄·  ▄▄▄·▄▄▄ .▄▄▄  
▐█ ▄█▀▄ █·▪      █▌█▌▪▐█▪██▌    ▐█ ▀. ▐█ ▌▪▀▄ █·▐█ ▀█ ▐█ ▄█▀▄.▀·▀▄ █·
 ██▀·▐▀▀▄  ▄█▀▄  ·██· ▐█▌▐█▪    ▄▀▀▀█▄██ ▄▄▐▀▀▄ ▄█▀▀█  ██▀·▐▀▀▪▄▐▀▀▄ 
▐█▪·•▐█•█▌▐█▌.▐▌▪▐█·█▌ ▐█▀·.    ▐█▄▪▐█▐███▌▐█•█▌▐█ ▪▐▌▐█▪·•▐█▄▄▌▐█•█▌
.▀   .▀  ▀ ▀█▄▀▪•▀▀ ▀▀  ▀ •      ▀▀▀▀ ·▀▀▀ .▀  ▀ ▀  ▀ .▀    ▀▀▀ .▀  ▀
                                                                                  
\t\t[ This tool is a scraper & checker for HTTP/s and SOCKS5 proxies. ]
\t\t\t\t\t[ The Best Ever Not Gonna Lie ]                                                                           
""", Colors.red_to_blue, interval=0.000)
    time.sleep(3)

ui()

def scrape_proxy_links(link, proxy_type):
    global https_scraped, socks5_scraped
    retries = 3
    for attempt in range(retries):
        try:
            response = requests.get(link, timeout=10)
            if response.status_code == 200:
                with output_lock:
                    time_rn = get_time_rn()
                    print(f"[ {pink}{time_rn}{reset} ] | ( {green}SUCCESS{reset} ) {pretty}Scraped --> ", end='')
                    sys.stdout.flush()
                    Write.Print(link[:60] + "*******\n", Colors.purple_to_red, interval=0.000)
                proxies = response.text.splitlines()
                if proxy_type == "https":
                    https_scraped += len(proxies)
                elif proxy_type == "socks5":
                    socks5_scraped += len(proxies)
                update_title_scraped()
                return proxies
        except (SSLError, ReadTimeout) as ssl_err:
            print(f"[ {pink}{get_time_rn()}{reset} ] | ( {red}SSL/Timeout ERROR{reset} ) Failed to scrape {link}: {ssl_err}")
            break  # Skip retries for SSL and timeout errors
        except RequestException as e:
            print(f"[ {pink}{get_time_rn()}{reset} ] | ( {red}ERROR{reset} ) Failed to scrape {link}: {e}")
            time.sleep(2)  # Wait before retrying
    return []

def scrape_proxies(proxy_list, proxy_type, file_name):
    proxies = []
    num_threads = 100
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        results = executor.map(lambda link: scrape_proxy_links(link, proxy_type), proxy_list)
        for result in results:
            proxies.extend(result)

    if not os.path.exists("scraped"):
        os.makedirs("scraped")

    with open(f"scraped/{file_name}", "w") as file:
        for proxy in proxies:
            if ":" in proxy and not any(c.isalpha() for c in proxy):
                file.write(proxy + '\n')

scrape_proxies(http_links, "https", "http_proxies.txt")
scrape_proxies(socks5_links, "socks5", "socks5_proxies.txt")

time.sleep(1)
if not os.path.exists("results"):
    os.makedirs("results")

a = open("results/http.txt", "w")
b = open("results/socks5.txt", "w")

a.write("")
b.write("")

a.close()
b.close()

valid_http = []
valid_socks5 = []

def check_proxy_http(proxy):
    global http_checked

    proxy_dict = {
        "http": "http://" + proxy,
        "https": "https://" + proxy
    }
    
    try:
        url = 'http://httpbin.org/get' 
        r = requests.get(url, proxies=proxy_dict, timeout=30)
        if r.status_code == 200:
            with output_lock:
                time_rn = get_time_rn()
                print(f"[ {pink}{time_rn}{reset} ] | ( {green}VALID{reset} ) {pretty}HTTP/S --> ", end='')
                sys.stdout.flush()
                Write.Print(proxy + "\n", Colors.cyan_to_blue, interval=0.000)
            valid_http.append(proxy)
            http_checked += 1
            update_title_checked()
            with open(f"results/http.txt", "a+") as f:
                f.write(proxy + "\n")
    except requests.exceptions.RequestException as e:
        pass

def checker_proxy_socks5(proxy):
    global socks5_checked
    try:
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, proxy.split(':')[0], int(proxy.split(':')[1]))
        socket.socket = socks.socksocket
        socket.create_connection(("www.google.com", 443), timeout=5)
        socks5_checked += 1
        update_title_checked()
        with output_lock:
            time_rn = get_time_rn()
            print(f"[ {pink}{time_rn}{reset} ] | ( {green}VALID{reset} ) {pretty}SOCKS5 --> ", end='')
            sys.stdout.flush()
            Write.Print(proxy + "\n", Colors.cyan_to_blue, interval=0.000)
        with open("results/socks5.txt", "a+") as f:
            f.write(proxy + "\n")
    except (socks.ProxyConnectionError, socket.timeout, OSError):
        pass

def check_all(proxy_type, pathTXT):
    with open(pathTXT, "r") as f:
        proxies = f.read().splitlines()

    with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:
        if proxy_type.startswith("http") or proxy_type.startswith("https"):
            executor.map(check_proxy_http, proxies)
        if proxy_type.startswith("socks5"):
            executor.map(checker_proxy_socks5, proxies)

def LetsCheckIt(proxy_types):
    threadsCrack = []
    for proxy_type in proxy_types:
        if os.path.exists(f"{proxy_type}_proxies.txt"):
            t = threading.Thread(target=check_all, args=(proxy_type, f"{proxy_type}_proxies.txt"))
            t.start()
            threadsCrack.append(t)
    for t in threadsCrack:
        t.join()

proxy_types = ["http", "socks5"]
LetsCheckIt(proxy_types)

os.remove("http_proxies.txt")
os.remove("socks5_proxies.txt")

if __name__ == "__main__":
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
