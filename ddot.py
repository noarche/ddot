import argparse
import requests
import os
import socks
import socket
import libtorrent as lt
import time
import random
import threading
from colorama import Fore, Style, init
from concurrent.futures import ThreadPoolExecutor

init(autoreset=True)

def set_proxy(ip, port):
    try:
        socks.set_default_proxy(socks.SOCKS5, ip, port)
        socket.socket = socks.socksocket
    except Exception as e:
        print(f"{Fore.RED}Failed to set proxy {ip}:{port}. Error: {e}")
        raise


def human_readable_size(size_in_bytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024


def download_torrent(torrent_file, proxies=None, total_data_transferred=0, retries=99):
    ses = lt.session()
    ses.listen_on(6881, 6891)


    info = lt.torrent_info(torrent_file)
    h = ses.add_torrent({'ti': info, 'save_path': './'})

    print(f"{Fore.GREEN}Starting download: {torrent_file}")
    try:
        while not h.is_seed():
            status = h.status()
            total_data_transferred += status.total_download
            print(f"\r{Fore.CYAN}Downloading: {status.name} | Progress: {status.progress*100:.2f}% | Total Downloaded: {human_readable_size(total_data_transferred)}", end="")
            time.sleep(1)

      
        print(f"\n{Fore.GREEN}Torrent finished: {torrent_file}")
        print(f"{Fore.YELLOW}Total data transferred: {human_readable_size(total_data_transferred)}")
        for file in os.listdir('./'):
            if file.endswith(".part"): 
                print(f"{Fore.MAGENTA}Deleting file: {file}")
                os.remove(file)
                print(f"{Fore.GREEN}File deleted successfully.")
        print(f"{Fore.MAGENTA}Restarting the cycle...")
        time.sleep(1) 
        download_torrent(torrent_file, proxies, total_data_transferred)

    except RecursionError as e:
        if retries > 0:
            print(f"{Fore.RED}RecursionError encountered. Retrying... ({retries} retries left)")
            time.sleep(2)
            download_torrent(torrent_file, proxies, total_data_transferred, retries - 1)
        else:
            print(f"{Fore.RED}Maximum retries reached. Aborting torrent download.")
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Download interrupted, stopping torrent download.")
        ses.remove_torrent(h)
    except Exception as e:
        print(f"{Fore.RED}An unexpected error occurred: {e}")


def download_file(url, proxies=None, total_data_transferred=0, retries=99):
    if proxies:
        proxy = random.choice(proxies)
        ip, port = proxy.split(':')
        try:
            set_proxy(ip, int(port))
        except Exception as e:
            print(f"{Fore.RED}Skipping proxy {ip}:{port} due to error: {e}")
            if retries > 0:
                print(f"{Fore.YELLOW}Retrying with a different proxy... ({retries} retries left)")
                time.sleep(2)
                download_file(url, proxies, total_data_transferred, retries - 1)
            else:
                print(f"{Fore.RED}Maximum retries reached. Aborting file download.")
                return

    try:
        response = requests.get(url, stream=True)
        file_name = url.split('/')[-1]
        with open(file_name, 'wb') as f:
            print(f"{Fore.GREEN}Starting download: {file_name}")
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    total_data_transferred += len(chunk)
        print(f"{Fore.GREEN}Download finished: {file_name}")
        print(f"{Fore.YELLOW}Total data transferred: {human_readable_size(total_data_transferred)}")
      
        print(f"{Fore.MAGENTA}Deleting file: {file_name}")
        os.remove(file_name)
        print(f"{Fore.GREEN}File deleted successfully.")
        time.sleep(1)  
        download_file(url, proxies, total_data_transferred)

    except requests.exceptions.RequestException as e:
        if retries > 0:
            print(f"{Fore.RED}Error occurred: {e}. Retrying... ({retries} retries left)")
            time.sleep(2)
            download_file(url, proxies, total_data_transferred, retries - 1)
        else:
            print(f"{Fore.RED}Maximum retries reached. Aborting file download.")
    except Exception as e:
        print(f"{Fore.RED}An unexpected error occurred: {e}")


def threaded_download_file(url, proxies=None, total_data_transferred=None, retries=99, thread_count=2):
    if total_data_transferred is None:
        total_data_transferred = [0]  

    def download_worker(thread_id):
        if proxies:
            proxy = random.choice(proxies)
            ip, port = proxy.split(':')
            try:
                set_proxy(ip, int(port))
            except Exception as e:
                print(f"{Fore.RED}[Thread {thread_id}] Skipping proxy {ip}:{port} due to error: {e}")
                return

        try:
            response = requests.get(url, stream=True)
            file_name = f"{url.split('/')[-1]}.thread{thread_id}"
            with open(file_name, 'wb') as f:
                print(f"{Fore.GREEN}[Thread {thread_id}] Starting download: {file_name}")
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        total_data_transferred[0] += len(chunk) 
            print(f"{Fore.GREEN}[Thread {thread_id}] Download finished: {file_name}")
            print(f"{Fore.RED}[Thread {thread_id}] Total data transferred so far: {human_readable_size(total_data_transferred[0])}")
            # Delete the file after download
            print(f"{Fore.BLUE}[Thread {thread_id}] Deleting file: {file_name}")
            os.remove(file_name)
            print(f"{Fore.GREEN}[Thread {thread_id}] File deleted successfully.")
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}[Thread {thread_id}] Error occurred: {e}")
        except Exception as e:
            print(f"{Fore.RED}[Thread {thread_id}] An unexpected error occurred: {e}")

  
    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        futures = [executor.submit(download_worker, i) for i in range(thread_count)]
        for future in futures:
            try:
                future.result() 
            except Exception as e:
                print(f"{Fore.RED}An error occurred in a thread: {e}")

    print(f"{Fore.GREEN}All threads completed. Total data transferred so far: {human_readable_size(total_data_transferred[0])}")


def main():
    parser = argparse.ArgumentParser(
        description="""This script downloads torrents or files using optional SOCKS5 proxies.
        
        Options:
        -torrent {torrentFile}  : Download the torrent repeatedly. The downloaded file is deleted after each download cycle.
        -file {URL}             : Download the file from the given URL repeatedly. The file is deleted after each download cycle.
        -p {proxy}              : Use a SOCKS5 proxy (ip:port) or a text file containing a list of SOCKS5 proxies (one per line) to rotate.
        
        Build Date: April 1 2025 
        Visit http://github.com/noarche/ddot for the latest version and more information.
        The objective is to maximize bandwidth usage without actually using disk space by deleting the files after they are downloaded.
        The script will continue downloading until stopped by the user."""
    )


    parser.add_argument('-torrent', type=str, help="Path to the torrent file")
    parser.add_argument('-file', type=str, help="URL of the file to download")
    parser.add_argument('-p', type=str, help="SOCKS5 proxy (ip:port) or path to a text file with a list of proxies")


    args = parser.parse_args()


    proxies = None
    if args.p:
        if args.p.endswith('.txt'):
            with open(args.p, 'r') as f:
                proxies = [line.strip() for line in f if line.strip()]
        else:
            proxies = [args.p]

 
    if not args.torrent and not args.file:
        choice = input("Do you want to download a torrent or a file? (torrent/file): ").strip().lower()
        if choice == 'torrent':
            args.torrent = input("Enter the path to the torrent file: ").strip()
        elif choice == 'file':
            args.file = input("Enter the URL of the file to download: ").strip()
        else:
            print(f"{Fore.RED}Invalid choice. Exiting.")
            return

   
    if args.torrent:
        total_data_transferred = 0
        while True:
            download_torrent(args.torrent, proxies, total_data_transferred)
    elif args.file:
        total_data_transferred = [0]  
        while True:
            threaded_download_file(args.file, proxies, total_data_transferred, thread_count=2) 
    else:
        print(f"{Fore.RED}Please provide either -torrent or -file argument.")

if __name__ == "__main__":
    main()

