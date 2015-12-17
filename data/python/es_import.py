import json
import object_storage
import re
from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient

es = Elasticsearch("http://elasticm1:9200")
ic = IndicesClient(es)

mapping = '{"mappings": {"comment": {"properties": {"created_utc": {"type": "date","format": "epoch_second"}, "body": {"type": "string", "analyzer": "english"}}}}}'

ic.create(index='2007',body=mapping)

sl_storage = object_storage.get_client('username',
                                       'key' ,
                                       datacenter='sjc01')


def iterload(src):
    buffer = ""
    dec = json.JSONDecoder()
    for chunk in src:         
        buffer = buffer + chunk
        while(True):
            try:
                r = dec.raw_decode(buffer)
            except:
                break
            yield r[0]
            buffer = buffer[r[1]:].strip(" \n\r\t")

chunk_size = 512*1024
count = 0
rc = sl_storage['reddit2']
for item in rc:
    match = re.search('^2007', item.name)
    if match:
        for j in iterload(item.chunk_download(chunk_size)):
            for key in j.keys():
            	es.index(index="2007", doc_type="comment", body=json.dumps(j))
        print count
