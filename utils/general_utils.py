import sys
sys.path.insert(0, 'vendor')

from connection.db_connection import connect_to_database
from datetime import date
import uuid
import os
import requests
from requests_aws4auth import AWS4Auth

def clean_record(record_str):
    record = record_str[0].replace("(","").replace(")","").replace("\"", "")
    record = record.split(",")
    return record

def build_records(cursor, column_names):
    results = []
    for row in cursor.fetchall():
        result = {}
        for col_name, col_value in zip(column_names, row):
            if isinstance(col_value, date):
                result[col_name] = str(col_value)
            elif isinstance(col_value, uuid.UUID):
                result[col_name] = str(col_value)
            else:
                result[col_name] = col_value
        results.append(result)
    return results

def response_api(status, message, data):
    resp = {
        "code": status,
        "message": message,
        "data": data
    }
    return resp

def search_user(user_id):
    conn = connect_to_database()
    if conn is None:
        return 500
    try:
        cursor = conn.cursor()
        cursor.execute("select * from dbo.sp_getuserbyid(%s)", 
                    (user_id,))
        column_names = [desc[0] for desc in cursor.description]
        records = build_records(cursor, column_names)
    except Exception as e:
        return None
    return records

def check_user_existence(user_id, cur):
    try:
        cur.execute("select dbo.sp_getuserbyid(%s)", 
                    (user_id,))
        if cur.rowcount > 0:
            return True
        else: 
            return False
    except Exception as e:
        print(str(e))
        return False
    
def check_client_existence(client_id, cur):
    try:
        cur.execute("select dbo.sp_getClientById(%s)", 
                    (client_id,))
        if cur.rowcount > 0:
            return True
        else: 
            return False
    except Exception as e:
        print(str(e))
        return False

def check_subscription_existence(subscription_id, cur):
    try:
        cur.execute("select dbo.sp_getsubscriptionbyid(%s)", 
                (subscription_id,))
        if cur.rowcount > 0:
            return True
        else: 
            return False
    except Exception as e:
        print(str(e))
        return False

def save_file_s3(group, name, file_extension, base64File):

    payload = {
        "group": group,
        "name": name,
        "file_extension": file_extension,
        "file": base64File
    }

    headers = {
        'Analyzer-Key': os.environ['ANALYZER_KEY'],
    }
    
    try:
        response = requests.post(url=os.environ['SAVE_FILE_URL'], headers=headers, json=payload)
        response.raise_for_status()
        urlResponse = response.json()["body"]["location"]
    except requests.exceptions.Timeout as e:
        return 504
    except Exception as e:
        return 500

    return urlResponse

""" def search_elastic(query: dict, indexName: str):

    region = os.environ['ELASTIC_REGION']
    service = "es"
    session = requests.Session()
    awsauth = AWS4Auth(os.environ['ELASTIC_ID'], os.environ['ELASTIC_SECRET_KEY'], region, service,  session=session)
    host = os.environ['ELASTIC_HOST'] 
    
    es = Elasticsearch(
        hosts=[{"host": host, "port": 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )
    
    search_result = es.search(index=indexName, body=query)
    
    return search_result """