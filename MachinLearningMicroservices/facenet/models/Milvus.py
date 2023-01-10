from sre_constants import SUCCESS
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection
import requests, json
class Milvus:
    def __init__(self):
        self.client = None
        self.collection = None
        self.schema = None
        self.client = self.connect()
        self.collection = self.create_collection()
        
    def connect(self):
        return connections.connect(alias="default", host='localhost', port='19530')
    
    def create_collection(self):
        collection_name = "facial_embeddings"
        dim = 128
        prime = FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id = True)
        #es_id = FieldSchema(name="es_id", dtype=DataType.INT64)
        embeddings = FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim = dim)
        # images_link = FieldSchema(name="image", dtype=DataType.STRING)
        schema = CollectionSchema(fields= [prime,embeddings],description="images embeddings")
        collection = Collection(name = collection_name,schema = schema)
        collection.load()
        return collection
    
    def insert(self,entities,image_link):
        """
            Insert Records Into Milvus DB
        """
        try:
            self.create_collection()
        except Exception as E:
            print(E)
        idx = list(self.collection.insert([[entities]])._primary_keys)
        print("ids")
        print(idx)
        headers = {
            "Content-Type":"application/json"
        }
        data = {
                "image_id":idx[0],
                "url":image_link
            }
        print(f"Uploading data {data}\tto Elastic Search")
        response = requests.post("http://10.100.102.107:9200/facial_embeddings_index/_doc",data=json.dumps(data),headers = headers)

        return idx[0]

    def search(self,embeddings):
        top = 10
        distance = "L2"
        search_params = {"metric_type": distance, "params": {"nprobe": 20000}}
        results = self.collection.search(
            [embeddings], "embeddings", search_params, top
            ) 
        images = []
        for raw_result in results:
            for result in raw_result:
                _ = self.fetch_image(result.id)
                images.append({"id":result.id,"distance":result.distance,"metric":distance,**_})
        print("matched images :", images)
        return sorted(list({r['url']: r for r in images}.values()),key=lambda k: k['distance'],reverse=True)

    def query_elasticsearch(self,query):
        headers = {
            "Content-Type":"application/json"
        }
        response = requests.post("http://10.100.102.107:9200/facial_embeddings_index/_search",data=json.dumps(query),headers = headers)
        try:
            return response.json()
        except:
            return []

    def fetch_image(self,id):
        print(id)
        query = {
            "query":{
                "match":{
                    "milvus_id":id
                }
            }
        }
        success = True
        exception,response,images = "","",""
        
        try:
            response = self.query_elasticsearch(query)
            print(response)
        except:
            success = False
            exception = "ES_NOT_FOUND"
        
        try:
            images = response['hits']['hits'][0]['_source']['images']
        except:
            success = False
            exception = "No Image Found for id {}".format(id)
                    
        return {"url":images,"success":success, "exception":exception}