import bs4,requests,re,time,os,tqdm
baseurl = "https://xkcd.com/"
dirpath = "/home/nillnada/xkcd/all/"
reg = r"[\w\d\s\(\)]+\.[pjg][npi][gf]"

filepath = "/home/nillnada/xkcd/index.txt"
continue_file = open(filepath,"r")
start_index = int(continue_file.read())
continue_file.close()

session = requests.Session()
def continuum(filepath):
    """ nothing classy just keeps a continue txt file for continuity """
    continue_file = open(filepath,"w+")
    continue_file.truncate(0)
    continue_file.write(str(i))
    continue_file.close()
    print("updated the continue file")
for i in range(1,2000):
    if i == 404:
        """
        this one took me a while to figure out
        turns out he skipped 404 for 'obvious reasons'
        """
        continue
    if i == 1037 or 1608 or 1663:
        """
        these ones I have no idea why he chose
        these specific numbers but anyway there's no
        comic here so we skip
        """ 
        continue

    if i % 50 == 0:
        if i == 1350:
            print("Visit https://xkcd.com/1350/ it's an interactive comic")
            continue
        print("Sleeping for a while, this is my version of Congestion Control lol")
        continuum(filepath)
        time.sleep(2)
    url = baseurl+str(i)+"/"
    try:
        res = session.get(url)
    except:
        continuum(filepath)  
        #res.raise_for_status()
    soup = bs4.BeautifulSoup(res.content, features="lxml")
    img_url = "https:"+soup.body.find("div",id='comic').img['src']
    name = re.findall(reg,img_url)

    if os.path.exists(os.path.join(dirpath,name[0])):
        print("skipping " + name[0]+" comic: "+str(i))
        continue
    print("downloading "+name[0])
    try:
        img =session.get(img_url)
    except:
        continuum(filepath)
    file = open("/home/nillnada/xkcd/all/"+name[0],"wb")
    for j in img.iter_content(chunk_size=1024*8*1024):
        file.write(j)
    file.close()

