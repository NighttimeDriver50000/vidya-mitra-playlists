#!/usr/bin/env python3
import json
import re
titles = json.load(open("vidya-mitra-playlists.json"))
rawcourses = open("vidya-mitra-playlists.txt").read().strip().splitlines()
courses = list(map(lambda line: line.split(":"), rawcourses))
allinfo = []
for title in titles:
    a = re.sub(r"\(?[-eE]-?PG[Pp]?\)?", "", title)
    pmatch = re.search(r"P[-:\s]?(\d+)", a)
    pval = int(pmatch.group(1), base=10) if pmatch else 0
    b = re.sub(r"[-_,\s]*P(-\d*|[-:\s]?\d+)[-.]?", "", a)
    vmmatch = re.search(r"VM[-:\s]?(\d+)", b)
    vmval = int(vmmatch.group(1), base=10) if vmmatch else 0
    c = re.sub(r"[-_,\s]*VM[-:\s]?\d*[-.]?", "", b)
    hmatch = re.search(r"H(\d\d)\w\w", c)
    hval = int(hmatch.group(1), base=10) if hmatch else 0
    d = re.sub(r"[-:\s]+", " ", c).strip()
    course = "Zzz Uncategorized"
    final = d
    for name, test in courses:
        fulltest = r"^({0})(\s+|\(|$)|\s*\(({0})(,.*)?\)|\s+({0})$".format(test)
        if re.search(fulltest, d):
            course = name
            final = re.sub(fulltest, "", d).strip()
            if not final:
                final = d
            break
    if hval > 0:
        numtype = "H"
        num = hval
    elif vmval > 0:
        numtype = "VM"
        num = vmval
    else:
        numtype = "P"
        num = pval
    info = (course, numtype, num, final, title)
    allinfo.append(info)
allinfo.sort()
for info in allinfo:
    print("{} ({}-{}): {} [{}]".format(*info))
