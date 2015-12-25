## Install

树莓派需要额外安装一些包:

```
sudo apt-get install libffi-dev
sudo apt-get install libxml2-dev
sudo apt-get install libxslt1-dev
sudo apt-get install python-dev
```


```
sudo pip install scrapy
git clone https://github.com/RaspberryTools/scrapy_comic.git
```

## Config

随便点入某个漫画, 如`http://comic.ck101.com/comic/6643`

填入`comic/spiders/spider.py`的 start_urls中, 如下:

```
start_urls = (
    'http://comic.ck101.com/comic/6643',
    )
```

在`comic/setting.py`里填写`IMAGES_STORE = 'Downloads/'`来设置下载地址


## Usage

恢复或暂停

```
scrapy crawl comic -s JOBDIR=crawls/somespider
```

需要扶墙的可使用proxychains

![](img/1.png)


