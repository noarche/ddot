# 📥 ddot — Diskless Downloader

**Build Date:** April 1, 2025  
**Author:** [noarche](https://github.com/noarche)  
**Repository:** [GitHub](http://github.com/noarche/ddot)

---

### ⚡ Overview

`ddot` is a bandwidth-intensive downloader designed to continuously download files or torrents **without using disk space**. After each successful download, files are **immediately deleted**. Ideal for:

- Testing network throughput
- Stress-testing SOCKS5 proxies
- Simulating large downloads

---

### 🔧 Features

- ✅ Repeated file/torrent downloads
- ✅ Deletes files after every cycle
- ✅ SOCKS5 proxy support (single or rotating list)
- ✅ Threaded downloads for high bandwidth use
- ✅ Built-in retry logic for stability
- ✅ Terminal output with vibrant colors
- ✅ Human-readable statistics

---

### 🛠️ Requirements

- Python 3.7+
- `libtorrent`
- Python libraries:
  - `requests`
  - `colorama`
  - `pysocks`

## Install dependencies:


`pip install requests colorama pysocks python-libtorrent`


# Basic torrent download loop

`python ddot.py -torrent /path/to/file.torrent`

# Basic file download loop

`python ddot.py -file https://example.com/file.zip`

# File download using a single SOCKS5 proxy

`python ddot.py -file https://example.com/file.zip -p 127.0.0.1:9050`

# Torrent download using a proxy list

`python ddot.py -torrent file.torrent -p proxies.txt`



## 🧰 Arguments

-torrent	Path to a .torrent file to download repeatedly

-file	URL to a file to download repeatedly

-p	SOCKS5 proxy in ip:port format or path to a .txt file with proxies

  If no arguments are provided, the script will prompt you interactively.

## 📎 Behavior

   If downloading torrents, the .torrent file is reused indefinitely.

   If downloading files, 2 threads are used by default (configurable).

   Downloaded files are deleted after completion.

   Proxy selection is randomized per download.

  On error or failure, the script retries up to 99 times before giving up.

## 💡 Tips

  To use with TOR, run:

    python ddot.py -file http://example.com/file -p 127.0.0.1:9050

  Use a proxy list (one ip:port per line) for auto-rotation.

  Run script from a Ramdisk to avoid disk IO.

## ⚠️ Disclaimer

This tool is provided for educational and testing purposes only.
Do not use it to violate terms of service, abuse resources, or engage in malicious activity.

## 🪙 Support


-------------------------------------------------------------------

# ꧁꧂  Buy me a coffee ☕

![qrCode](https://raw.githubusercontent.com/noarche/cd-ripper/main/unrelated-ignore/CryptoQRcodes.png)

**Bitcoin** address `bc1qnpjpacyl9sff6r4kfmn7c227ty9g50suhr0y9j`


**Ethereum** address `0x94FcBab18E4c0b2FAf5050c0c11E056893134266`


**Litecoin** address `ltc1qu7ze2hlnkh440k37nrm4nhpv2dre7fl8xu0egx`



-------------------------------------------------------------------

![noarche's GitHub stats](https://github-readme-stats.vercel.app/api?username=noarche&show_icons=true&theme=transparent)



# 🍭 Looking for a FAST Socks4/Socks5 Proxylist checker?

Written in GO for ultra high performance and reliability. Validate your proxylist is alive. 

[Download here](https://github.com/noarche/proxy-checker)


