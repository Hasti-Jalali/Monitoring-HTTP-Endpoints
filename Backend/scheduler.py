from app import db, app
import requests
import schedule
from datetime import datetime

# print(db.Table('request').columns.keys())

def call_urls():
    print('Sending requests...')
    with app.app_context():
        urls = db.session.execute('select * from url').all()
    for url in urls:
        address = url[1]
        result = requests.get(address)
        status = result.status_code
        date = datetime.now()
        query = f'Insert into request (url_id, result, timestamp) values ({url[0]}, {status}, "{date}")'
        with app.app_context():
            db.session.execute(query)
        db.commit()


  

schedule.every(5).minutes.do(call_urls)
while True: 
  schedule.run_pending()