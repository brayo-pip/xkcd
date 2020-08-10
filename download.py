import bs4,requests,re,time #,os
baseurl = "https://xkcd.com/"
dirpath ="/home/nillnada/xkcd/all/"
reg = r"[\w|\d|\s|\(|\)]+\.[j|p][p|n][g]"

for i in range(403,614):
    if i == 404:
        """
        this one took me a while to figure out
        turns out he skipped 404 for 'obvious reasons'
        """
        continue
    if i%50==0:
        print("Sleeping for a while, this is my version of Congestion Control lol")
        time.sleep(10)
    url = baseurl+str(i)+"/"
    res = requests.get(url)
    #res.raise_for_status()
    soup = bs4.BeautifulSoup(res.content, features="lxml")
    img_url = "https:"+soup.body.find("div",id='comic').img['src']
    name = regex.findall(reg,img_url)
    """
    if os.path.exists(os.path.join(dirpath,name[0])):
        print("skipping" + name[0])
        continue
    """
    print("downloading "+name[0])
    img =requests.get(img_url)
    file = open("/home/nillnada/xkcd/all/"+name[0],"wb")
    for j in img.iter_content(1000000):
        file.write(j)
    file.close()
