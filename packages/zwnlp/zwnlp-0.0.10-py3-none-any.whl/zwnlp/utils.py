import re
import langid

def temp_html_clean(s):
    s = s.replace('</p>', '').replace('</mark>', '')\
        .replace("<mark class='markpsn' onclick='yewpsn(this);' data-eid='1'>", '')
    s = re.sub(r"<mark onclick='yew\(this\);' data-eid='\d+'>", '', s)
    rtn = s.split('<p>')
    rtn = [s.strip() for s in rtn if s.strip()!='']
    return rtn

def langcode(s):
    t = langid.classify(s)
    return t[0]
