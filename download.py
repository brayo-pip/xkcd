import getpass, os, multiprocessing, requests, re

baseurl = "https://xkcd.com/"
json_part = "info.0.json"

if os.name == "posix":
    # for unix systems like linux
    dirpath = "/home/" + getpass.getuser() + "/xkcd-comics/"
    filepath = dirpath + "index.txt"
if os.name == "nt":
    # for windows
    dirpath = "C:/Users/" + getpass.getuser() + "/xkcd-comics/"
    filepath = dirpath + "index.txt"

# still figuring out Mac OS


def initialize(dirpath, filepath):
    """runs once at script start"""
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    if not os.path.exists(filepath):
        # Creates the continue file on first run
        continue_file = open(filepath, "x")
        continue_file.write(str(1))
        continue_file.close()


initialize(dirpath, filepath)

continue_file = open(filepath, "r")
start_index = int(continue_file.read())
continue_file.close()


def continuum(filepath, index):
    """nothing classy just keeps a continue txt file for continuity"""
    continue_file = open(filepath, "r+")
    if index > int(continue_file.read()):
        continue_file.truncate(0)
        continue_file.write(str(index))
        continue_file.close()
        print("updated the continue file")


def check_i(i):
    """simply skips the urls without a comic or that the comic isn't an image"""
    if i == 404:
        # this one took me a while to figure out
        # turns out he skipped 404 for 'obvious reasons'
        return False
    if i == 1350 or i == 1608 or i == 2198:
        print("Visit https://xkcd.com/" + str(i) + "/ it's an interactive comic")
        return False
    if i == 1416:
        print(
            "Visit https://xkcd.com/1416 it's an .html file with a boring joke (subjective)"
        )
        return False

    if i == 1037 or i == 1663:
        # these ones I have no idea why he chose
        # these specific numbers but anyway there's no
        # comic here so we skip
        print("Skipped https://xkcd.com/" + str(i) + "/ the comic is not an image")
        return False
    if i == 472:
        # Randall Monroe screwed up the json data
        return False
    return True


def check_name(name):
    if "?" or "\\" or "/" or "*" or "<" or ">" or "|" or ":" or '"' in name:
        return True


def end_index():
    res = requests.get(baseurl + json_part)
    res.raise_for_status()
    json_data = res.json()
    return int(json_data["num"])


session = None


def set_global_session():
    """ The session implements persistent http connections """
    global session
    if not session:
        session = requests.Session()


end_index = end_index()


def download_comic(i):
    url = baseurl + str(i) + "/" + json_part
    res = session.get(url)
    res.raise_for_status()

    json_data = res.json()
    img_url = json_data["img"]

    # extract extension
    reg = r"\.[pjg][npi][gf]"
    ext = re.findall(reg, img_url)

    name = json_data["title"] + ext[0]
    # File names can't have these characters
    bad_chars = "<>?|\\/:*"

    if check_name(name):
        for h in bad_chars:
            name = name.replace(h, "")
            if not check_name(name):
                break
    if os.path.exists(os.path.join(dirpath, name)):
        print("skipping " + name + " comic: " + str(i))
        return
    print("downloading " + name)
    try:
        img = session.get(img_url)
    except:
        print("failed to get comic: " + str(i))
        img.raise_for_status()

    file = open(dirpath + name, "wb")
    for j in img.iter_content(chunk_size=1024 * 8):
        file.write(j)
    file.close()


def download_all_comics(sites):
    with multiprocessing.Pool(initializer=set_global_session) as pool:
        pool.map(download_comic, sites)


if __name__ == "__main__":
    sites = [i for i in range(start_index, end_index + 1)]
    download_all_comics(sites)
    continuum(filepath=filepath, index=end_index)
