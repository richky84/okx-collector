import ccxt
import os
from datetime import datetime

# Render의 환경변수에서 Key를 가져옵니다 (보안)
api_key = os.environ.get('OKX_API_KEY')
secret_key = os.environ.get('OKX_SECRET_KEY')
passphrase = os.environ.get('OKX_PASSPHRASE')

def record_trades():
    if not api_key or not secret_key:
        print("API Key가 설정되지 않았습니다.")
        return

    # OKX 연결
    okx = ccxt.okx({
        'apiKey': api_key,
        'secret': secret_key,
        'password': passphrase,
    })

    try:
        # 최근 체결 내역 5개 조회
        trades = okx.fetch_my_trades('BTC/USDT', limit=5)
        
        if not trades:
            print(f"[{datetime.now()}] 최근 거래 내역 없음")
            return

        print(f"--- [{datetime.now()}] 매매 타점 기록 시작 ---")
        for trade in trades:
            dt = datetime.fromtimestamp(trade['timestamp'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
            side = trade['side'].upper() # BUY or SELL
            price = trade['price']
            amount = trade['amount']
            print(f"시간: {dt} | 포지션: {side} | 가격: {price} | 수량: {amount}")
        print("---------------------------------------------")

    except Exception as e:
        print(f"에러 발생: {e}")

if __name__ == "__main__":
    record_trades()