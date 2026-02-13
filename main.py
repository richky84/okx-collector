import ccxt
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json
from datetime import datetime

# 1. 환경변수 설정
api_key = os.environ.get('OKX_API_KEY')
secret_key = os.environ.get('OKX_SECRET_KEY')
passphrase = os.environ.get('OKX_PASSPHRASE')

# 구글 시트 인증 정보 (Render의 Secret File 경로 또는 환경변수)
# 여기서는 Render의 'Secret File' 기능을 사용한다고 가정합니다.
json_file_path = '/etc/secrets/google_key.json' 

def record_trades():
    # --- OKX 연결 ---
    okx = ccxt.okx({
        'apiKey': api_key,
        'secret': secret_key,
        'password': passphrase,
    })

    # --- 구글 시트 연결 ---
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_file_path, scope)
    client = gspread.authorize(creds)
    
    # 내 스프레드시트 열기 (제목을 정확히 입력하세요!)
    spreadsheet = client.open("OKX 매매일지") 
    sheet = spreadsheet.sheet1 # 첫 번째 시트 선택

    try:
        trades = okx.fetch_my_trades('BTC/USDT', limit=5)
        
        if not trades:
            print("최근 거래 없음")
            return

        print("--- 구글 시트에 기록 중 ---")
        for trade in trades:
            dt = datetime.fromtimestamp(trade['timestamp'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
            side = trade['side'].upper()
            price = trade['price']
            amount = trade['amount']
            cost = trade['cost'] # 거래 금액
            
            # 시트에 한 줄 추가 (시간, 포지션, 가격, 수량, 금액)
            row = [dt, side, price, amount, cost]
            sheet.append_row(row)
            print(f"기록 완료: {row}")

    except Exception as e:
        print(f"에러 발생: {e}")

if __name__ == "__main__":
    record_trades()
