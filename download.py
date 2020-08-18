import bs4,getpass,requests,re,time,os
baseurl = "https://xkcd.com/"
regex = r"[\w\d\s\(\)]+\.[pjg][npi][gf]"

if os.name == "posix":
    #for unix systems like linux
    dirpath = "/home/"+getpass.getuser()+"/xkcd/"
    filepath = dirpath+"index.txt"
if os.name == "nt":
    #for windows
    dirpath = "C:/Users/"+getpass.getuser()+"/xkcd"
    filepath = dirpath+"index.txt"

#still figuring out Mac OS

def initialize(dirpath,filepath):
    """runs once at script start"""
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    if not os.path.exists(filepath):
        #Creates the continue file on first run
        continue_file = open(filepath, "x")
        continue_file.write(str(i))
        continue_file.close()

continue_file = open(filepath,"r")
start_index = int(continue_file.read())
continue_file.close()


def continuum(filepath):
    """nothing classy just keeps a continue txt file for continuity"""
    continue_file = open(filepath,"w+")
    continue_file.truncate(0)
    continue_file.write(str(i))
    continue_file.close()
    print("updated the continue file")

def check_i(i):
    """simply skips the urls without a comic or that the comic isn't an image"""
    if i == 404:
        #this one took me a while to figure out
        #turns out he skipped 404 for 'obvious reasons'
        return False
    if i == 1350 or i == 1608 or i == 2198:
        print("Visit https://xkcd.com/"+str(i)+"/ it's an interactive comic")
        return False
    if i == 1416:
        print("Visit https://xkcd.com/1416 it's an .html file with a boring joke (subjective)")
        return False

    if i == 1037 or i == 1663:
        #these ones I have no idea why he chose
        #these specific numbers but anyway there's no
        #comic here so we skip

        print("Skipped https://xkcd.com/"+str(i)+"/ the comic is not an image")
        return False
    if i == 1538 or i == 1953:
        #these are just incorrectly parsed am working on it though
        print("Skipped https://xkcd.com/"+str(i)+"/ the script can't pass these correctly \n Am working on a fix though \n")
        return False
    return True
#The session implements persistent http connections
session = requests.Session()
for i in range(start_index,2346+1):
    if not check_i(i):
        continue
    if i % 10 == 0:
        print("Sleeping for a while, this is my version of Congestion Control lol")
        continuum(filepath)
        time.sleep(0.5)
    url = baseurl+str(i)+"/"
    try:
        res = session.get(url)
    except:
        continuum(filepath)
        continue
        #res.raise_for_status()
    soup = bs4.BeautifulSoup(res.content, features="lxml")
    img_url = "https:"+soup.body.find("div",id='comic').img['src']
    name = re.findall(regex,img_url)

    if os.path.exists(os.path.join(dirpath,name[0])):
        print("skipping " + name[0]+" comic: "+str(i))
        continue
    print("downloading "+name[0])
    try:
        img = session.get(img_url)
    except:
        print("failed to get comic: "+str(i))
        continuum(filepath)
        continue

    file = open(dirpath+name[0],"wb")
    for j in img.iter_content(chunk_size=1024*8):
        file.write(j)
    file.close()