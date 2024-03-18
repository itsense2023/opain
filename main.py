import string
from fastapi import FastAPI, HTTPException, Body
import httpx
from connection.db_connection import connect_to_database
import models.responses as STATUS_CODE
from utils.general_utils import build_records, response_api
from datetime import datetime
import pytz

app = FastAPI()
app.title = "Mi aplicación con FastAPI"
app.version = "0.0.1"
@app.get('/', tags=['CONFA'])
def message():
    return "Hello World!"

@app.post("/ldap")
async def make_external_post_request(data: dict = Body(...)):

    external_endpoint_url = "https://app.confa.co:8320/zionWS/rest/zion/metodo16"
    #data_to_send = {"usuario": "ext_prueba0",
    #                "contrasena" : "7PQQU41kzeNehKHKY3MI",
    #                "sistema" : 54}
    print(data)
    async with httpx.AsyncClient() as client:
        response = await client.post(external_endpoint_url, json=data)
        print(response)
    if response.status_code == 200:
        return {"message": "POST request successful", "response_data": response.json()}
    else:
        return {"message": "POST request failed", "status_code": response.status_code}

@app.get("/db/{table}")
def gen_get_all(table: str):
    
    #entity = event['path']['entity']
    entity = table
    available_entities = ["catalogs",
    "field",
    "form",
    "notification",
    "requests",
    "roles",
    "users"
    ]
    print(entity)
    conn = connect_to_database()
    if conn is None:
        return STATUS_CODE.INTERNAL_ERROR_SERVER
    cur = conn.cursor()
    try:
        cur.execute(f"select * from dbo.sp_gen_get_all_{entity}()")
        column_names = [desc[0] for desc in cur.description]
        records = build_records(cur, column_names)
        cur.close()
        conn.close()
        return response_api(STATUS_CODE.OK['code'], STATUS_CODE.OK['message'], records)
    except Exception as e:
        cur.close()
        conn.close()
        print("error --> ", str(e))
        return STATUS_CODE.INTERNAL_ERROR_SERVER

@app.get("/form/{form_id}")
def get_form_fields_by_id(form_id: int):
    
    #entity = event['path']['entity']
    form_id = form_id
    conn = connect_to_database()
    if conn is None:
        return STATUS_CODE.INTERNAL_ERROR_SERVER
    cur = conn.cursor()
    try:
        cur.execute(f"select * from dbo.sp_get_fields_form({form_id})")
        column_names = [desc[0] for desc in cur.description]
        records = build_records(cur, column_names)
        cur.close()
        conn.close()
        #_ = [get_catalog_by_id(record['catalog_source']) for record in records if record['catalog_source'] is not None]
        for record in records:
            if record['catalog_source'] is not None:
                record['catalog_source'] = get_catalog_by_id(record['catalog_source'])
                print(record['catalog_source'])
        return response_api(STATUS_CODE.OK['code'], STATUS_CODE.OK['message'], records)
    except Exception as e:
        cur.close()
        conn.close()
        print("error --> ", str(e))
        return STATUS_CODE.INTERNAL_ERROR_SERVER
def get_catalog_by_id(catalog_id: int):
    conn = connect_to_database()
    if conn is None:
        return STATUS_CODE.INTERNAL_ERROR_SERVER
    cur = conn.cursor()
    try:
        cur.execute(f"select * from dbo.sp_get_catalog_items({catalog_id})")
        column_names = [desc[0] for desc in cur.description]
        records = build_records(cur, column_names)
        cur.close()
        conn.close()
        return records
    except Exception as e:
        cur.close()
        conn.close()
        print("error --> ", str(e))
        return STATUS_CODE.INTERNAL_ERROR_SERVER

@app.post("/request/{form_id}")
def create_request(data: dict = Body(...)):

    desired_time_zone = 'UTC'
    #entity = event['path']['entity']
    data = data
    print(data)
    request= {}
    filing_date = user_creation_date = datetime.datetime.today()
    filing_time = datetime.now(pytz.timezone(desired_time_zone))
    print(filing_date)
    request_status = 1
    print(request_status)
    '''applicant_type =
    request_type = 
    doc_type = 
    doc_id = 
    <filing_date date>, 
	<filing_time timestamp with time zone>, 
	<request_status integer>, 
	<applicant_type integer>, 
	<request_type integer>, 
	<doc_type integer>, 
	<doc_id character varying>, 
	<applicant_name character varying>, 
	<applicant_email character varying>, 
	<applicant_cellphone character varying>, 
	<request_description character varying>, 
	<request_days integer>, 
	<assigned_user character varying>, 
	<request_answer character varying>, 
	<data_treatment boolean>, 
	<applicant_attachments character varying[]>, 
	<assigned_attachments character varying[]>'''
    conn = connect_to_database()
    if conn is None:
        return STATUS_CODE.INTERNAL_ERROR_SERVER
    cur = conn.cursor()
'''    try:
        cur.execute("select * from dbo.sp_createrequest(%s::int,%s::int,%s::bit,%s::date,%s::varchar)", 
                (data["plan_id"], data["package_id"], data["active_record"], data["created_date"], data["created_user"]))
        return STATUS_CODE.OK['code']
    except Exception as e:
        cur.close()
        conn.close()
        print("error --> ", str(e))
        return STATUS_CODE.INTERNAL_ERROR_SERVER'''