import json,requests,twstock
from linebot import LineBotApi, WebhookHandler
from linebot.models import  TextSendMessage

twstock.__update_codes()
user_taget = {}

def linebot(request):
    try:
        access_token = 'P0U7qkoKkoNau+nK/0gW7v6FJNG/eoS9ixrjK84qGvE3Jm7d7COAep/sMsgHH8D3tcPiYG1tStKvaCXVwJtV0bUVBOqUWMxbQwYYBBKzAjUyx++QeoFI8os87J5Y8Y7GmGNOHW5a5QdlBnENk113wgdB04t89/1O/w1cDnyilFU='
        secret = 'aa7e289ac042ac3b493499df89f2cfb9'
        body = request.get_data(as_text=True)
        json_data = json.loads(body)
        line_bot_api = LineBotApi(access_token)
        handler = WebhookHandler(secret)
        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)
        #設定使用者基本資料
        tk = json_data['events'][0]['replyToken']
        user_id = json_data['events'][0]['source']['userId']
        
        if json_data['events'][0]['message']['type'] == 'text':
            user_message = json_data['events'][0]['message']['text']
            if user_message == '設定股票':
                retext = 'set'
                line_bot_api.reply_message(tk,TextSendMessage(text='輸入你的股票編號:'))
            elif user_message == '設定最高價':
                retext = 'hpset'
                line_bot_api.reply_message(tk,TextSendMessage(text='輸入你想設定的最高價'))
            elif user_message == '設定最低價':
                retext = 'lpset'
                line_bot_api.reply_message(tk,TextSendMessage(text='輸入你想設定的最低價'))
            handle_message(user_message,tk,user_id,line_bot_api,retext)        
            
        else:
            line_bot_api.reply_message(tk,TextSendMessage(text='請輸入文字訊息'))

        print(user_message)

    except:
        url = 'https://notify-api.line.me/api/notify'
        token = 'R4BSFVdXCWINsjn76YcWAj41kZRjLgSGMaR96FoGzMd'
        headers = {
            'Authorization': 'Bearer ' + token    # 設定權杖
        }
        data = {
            'message':'function error！'     # 設定要發送的訊息
        }
        data = requests.post(url, headers=headers, data=data)  
        print('error')
    return 'OK'



def handle_message(user_message,tk,user_id,line_bot_api,retext):
    global stock , hpset , lpset
    if retext == 'set':
        if user_message.isdigit() and len(user_message) == 4  :            
            stock = user_message
            user_taget[user_id] = {'id':user_id,'stock':stock}
            reply = f"你設定{stock},請設定你要的最高價/最低價格。"
            line_bot_api.reply_message(tk,TextSendMessage(text=reply))
        else:
            line_bot_api.reply_message(tk,TextSendMessage(text='請輸入正確的股票代號(4碼)'))
    elif retext == 'hpset' and 'stock' in user_taget.get(user_id,{}):
        hpset = user_message
        user_taget[user_id].update({'hpset':hpset})
        if 'lpset' in user_taget.get(user_id,{}):
            reply = f"你設定的股票代號:{stock}\最高價格:{hpset}\最低價格:{lpset}\n設定完成，如要重設請再按功能"
        else: 
            reply = f"你設定{hpset},請繼續設定你要的最低價格。"
        line_bot_api.reply_message(tk,TextSendMessage(text=reply))
    elif retext == 'lpset' and 'stock' in user_taget.get(user_id,{}):
        lpset = user_message
        user_taget[user_id].update({'lpset':lpset})
        if 'hpset' in user_taget.get(user_id,{}):
            reply = f"你設定的股票代號:{stock}\最高價格:{hpset}\最低價格:{lpset}\n設定完成，如要重設請再按功能"
        else:    
            reply = f"你設定{lpset},請繼續設定你要的最高價格。"
        line_bot_api.reply_message(tk,TextSendMessage(text=reply))
    else:
        line_bot_api.reply_message(tk,TextSendMessage(text='請輸入正確的股票代號(4碼)，請重新開始。'))


    
def check_stock_price():
    global current_stock_price
    
    current_stock_price += random.uniform(-5, 5)
    
    target_price = 90.0
    exit_price = 80.0
    
    current_time = datetime.now().time()
    current_day = datetime.now().weekday()
    
    if time(10, 0) <= current_time <= time(16, 0) and current_day < 5:  # 在周一到周五的上午10點到下午4點執行
        print(f"您設定的股價: {current_stock_price}")
    
        if current_stock_price <= exit_price:
            print("目前股價已超越設定股價")
            scheduler.shutdown()
        elif current_stock_price <= target_price:
            print("目前股價已低於設定股價")
            execute_task()
    else:
        print("現在不在服務時段")
#異步起發器
scheduler.add_job(check_stock_price, trigger='interval', minutes=1)



    
                 
