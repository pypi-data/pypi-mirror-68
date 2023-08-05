def download(g,n):
    import requests
    f=requests.get(g)
    with open(n,"wb") as p:
        for c in r.iter_content(chunk_size=1024):
            p.write(c)
