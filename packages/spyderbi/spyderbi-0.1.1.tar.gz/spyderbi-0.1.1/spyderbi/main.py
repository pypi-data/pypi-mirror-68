from simpleinfo import getinfo
import json
p=getinfo(av="", bv='', uid="32708362")
p.translate('BV1LK411W735')
#js=p.authorinfos(types="")
js=p.videoinfos(oid="498082939",types="message")
#print(js['data'])#p.list_all_member()


p.getgoodjson(js)