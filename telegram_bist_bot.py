import logging
import asyncio
import pandas as pd
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import yfinance as yf
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

TOKEN = 'TELEGRAM_TOKEN_HERE'

BIST100_SYMBOLS = [
    "AEFES.IS", "AGHOL.IS", "AKBNK.IS", "AKCNS.IS", "AKGRT.IS", "AKSA.IS", "AKSEN.IS", "ALGYO.IS", "ARCLK.IS", "ASELS.IS", "AYGAZ.IS", "BIMAS.IS", "BRISA.IS", "CEMTS.IS", "DEVA.IS", "DOHOL.IS", "ECILC.IS", "ENJSA.IS", "ENKAI.IS", "EREGL.IS", "FROTO.IS", "GARAN.IS", "GUBRF.IS", "HEKTS.IS", "ISCTR.IS", "ISGYO.IS", "IZDMC.IS", "KARSN.IS", "KCHOL.IS", "KORDS.IS", "KOZAA.IS", "KOZAL.IS", "MPARK.IS", "MGROS.IS", "ODAS.IS", "OTKAR.IS", "PETKM.IS", "PGSUS.IS", "SAHOL.IS", "SASA.IS", "SISE.IS", "SOKM.IS", "TAVHL.IS", "TCELL.IS", "THYAO.IS", "TKFEN.IS", "TOASO.IS", "TRKCM.IS", "TTKOM.IS", "TUPRS.IS", "ULKER.IS", "VAKBN.IS", "VESTL.IS", "YATAS.IS", "YKBNK.IS", "ZOREN.IS"
]
UYARI_MESAJI = "🚨 YATIRIM TAVSİYESİ DEĞİLDİR 🚨\n🔵 Eğitim amaçlıdır 🔵"

def get_stock_data(symbol):
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1y")
        if data.empty:
            return None
        return data
    except Exception as e:
        logging.error(f"Error fetching data for {symbol}: {e}")
        return None

def get_ma_analysis(symbol):
    data = get_stock_data(symbol)
    if data is None:
        return None
    
    current_price = data['Close'].iloc[-1]
    ma50 = data['Close'].rolling(window=50).mean().iloc[-1]
    ma100 = data['Close'].rolling(window=100).mean().iloc[-1]
    ma200 = data['Close'].rolling(window=200).mean().iloc[-1]
    
    return current_price, ma50, ma100, ma200

def analyze_stock(symbol):
    df = get_stock_data(symbol)
    if df is None:
        return None, None, None
    df = df.reset_index()
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')
    model = RandomForestClassifier()
    X = df[['Open', 'High', 'Low', 'Close']].values
    y = (df['Close'].shift(-1) > df['Close']).astype(int).values[:-1]
    X_train, X_test, y_train, y_test = train_test_split(X[:-1], y, test_size=0.2, random_state=42)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions) if len(y_test) > 0 else None
    current_price = df['Close'].iloc[-1]
    suggestion = "Al" if model.predict([X[-1]])[0] == 1 else "Sat"
    return accuracy, suggestion, current_price

def get_rsi_analysis(symbol):
    data = get_stock_data(symbol)
    if data is None:
        return None
    
    # RSI hesaplama
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    current_price = data['Close'].iloc[-1]
    current_rsi = rsi.iloc[-1]
    
    return current_price, current_rsi

def get_momentum_analysis(symbol):
    data = get_stock_data(symbol)
    if data is None:
        return None
    
    # Momentum hesaplama (10 günlük)
    momentum = data['Close'] - data['Close'].shift(10)
    current_price = data['Close'].iloc[-1]
    current_momentum = momentum.iloc[-1]
    momentum_percentage = (current_momentum / current_price) * 100
    
    return current_price, momentum_percentage

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("BIST 100 Hareketli Ortalama Analizi", callback_data="1")],
        [InlineKeyboardButton("Hisse Hareketli Ortalama Analizi", callback_data="2")],
        [InlineKeyboardButton("BIST 100 Yapay Zeka Analizi", callback_data="3")],
        [InlineKeyboardButton("Hisse Yapay Zeka Analizi", callback_data="4")],
        [InlineKeyboardButton("BIST 100 RSI Analizi", callback_data="5")],
        [InlineKeyboardButton("Hisse RSI Analizi", callback_data="6")],
        [InlineKeyboardButton("BIST 100 Momentum Analizi", callback_data="7")],
        [InlineKeyboardButton("Hisse Momentum Analizi", callback_data="8")],
        [InlineKeyboardButton("En İyi 5 Hisse Analizi", callback_data="9")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    welcome_message = (
        f"{UYARI_MESAJI}\n\n"
        "Merhaba! Ben bir borsa analiz botuyum. Size nasıl yardımcı olabilirim?\n\n"
        "📊 Hisse analizi için aşağıdaki menüyü kullanabilirsiniz.\n"
    )
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("BIST 100 Hareketli Ortalama Analizi", callback_data="1")],
        [InlineKeyboardButton("Hisse Hareketli Ortalama Analizi", callback_data="2")],
        [InlineKeyboardButton("BIST 100 Yapay Zeka Analizi", callback_data="3")],
        [InlineKeyboardButton("Hisse Yapay Zeka Analizi", callback_data="4")],
        [InlineKeyboardButton("BIST 100 RSI Analizi", callback_data="5")],
        [InlineKeyboardButton("Hisse RSI Analizi", callback_data="6")],
        [InlineKeyboardButton("BIST 100 Momentum Analizi", callback_data="7")],
        [InlineKeyboardButton("Hisse Momentum Analizi", callback_data="8")],
        [InlineKeyboardButton("En İyi 5 Hisse Analizi", callback_data="9")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.reply_text(f"{UYARI_MESAJI}\n\nLütfen bir analiz yöntemi seçin:", reply_markup=reply_markup)

async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    choice = query.data

    if choice == "1":
        response = "BIST 100 Hareketli Ortalama Analizi - Zayıf Hisseler:\n\n"
        for symbol in BIST100_SYMBOLS:
            result = get_ma_analysis(symbol)
            if result:
                current_price, ma50, ma100, ma200 = result
                if current_price < ma50 and current_price < ma100 and current_price < ma200:
                    response += f"{symbol}:\nGüncel Fiyat: {current_price:.2f}\nMA50: {ma50:.2f}\nMA100: {ma100:.2f}\nMA200: {ma200:.2f}\n\n"
        await query.message.reply_text(response)
        await show_menu(update, context)

    elif choice == "2":
        await query.message.reply_text("Lütfen hareketli ortalama analizi yapmak istediğiniz hisse kodunu gönderin.")
        context.user_data['mode'] = 'ma_analysis'

    elif choice == "3":
        ai_explanation = (
            "🤖 Yapay Zeka Analiz Yöntemi:\n"
            "1. Son 1 yıllık veriler kullanılıyor\n"
            "2. Açılış, Yüksek, Düşük ve Kapanış fiyatları analiz ediliyor\n"
            "3. RandomForest algoritması ile tahmin yapılıyor\n"
            "4. Model, bir sonraki günün fiyatının yükseleceğini veya düşeceğini tahmin ediyor\n\n"
            "📊 Analiz Sonuçları:\n\n"
        )
        results = []
        for symbol in BIST100_SYMBOLS:
            accuracy, suggestion, current_price = analyze_stock(symbol)
            if accuracy is not None:
                results.append((symbol, accuracy, suggestion, current_price))

        results = sorted(results, key=lambda x: x[1], reverse=True)[:10]
        response = ai_explanation
        for stock in results:
            response += f"Hisse: {stock[0]}\nGüncel Fiyat: {stock[3]:.2f}\nDoğruluk: {stock[1]:.2f}\nÖneri: {stock[2]} ({stock[3]:.2f} TL'den)\n\n"
        await query.message.reply_text(response)
        await show_menu(update, context)

    elif choice == "4":
        await query.message.reply_text("Lütfen yapay zeka analizi yapmak istediğiniz hisse kodunu gönderin.")
        context.user_data['mode'] = 'ai_analysis'

    elif choice == "5":
        rsi_explanation = (
            "📈 RSI (Göreceli Güç Endeksi) Analizi:\n"
            "RSI, bir hisse senedinin aşırı alım veya aşırı satım bölgesinde olup olmadığını gösterir.\n"
            "- RSI < 30: Aşırı satım bölgesi (Alım fırsatı)\n"
            "- RSI > 70: Aşırı alım bölgesi (Satış fırsatı)\n\n"
            "🎯 En İyi 10 Alım Fırsatı:\n\n"
        )
        
        results = []
        for symbol in BIST100_SYMBOLS:
            result = get_rsi_analysis(symbol)
            if result:
                current_price, rsi = result
                if rsi < 40:  # Aşırı satım bölgesine yakın hisseleri seç
                    results.append((symbol, current_price, rsi))
        
        results = sorted(results, key=lambda x: x[2])[:10]  # En düşük RSI değerine sahip 10 hisse
        response = rsi_explanation
        for stock in results:
            response += f"Hisse: {stock[0]}\nGüncel Fiyat: {stock[1]:.2f}\nRSI: {stock[2]:.2f}\n\n"
        
        await query.message.reply_text(response)
        await show_menu(update, context)

    elif choice == "6":
        await query.message.reply_text("Lütfen RSI analizi yapmak istediğiniz hisse kodunu gönderin.")
        context.user_data['mode'] = 'rsi_analysis'

    elif choice == "7":
        momentum_explanation = (
            "📊 Momentum Analizi:\n"
            "Momentum, bir hisse senedinin fiyat değişim hızını gösterir.\n"
            "- Pozitif momentum: Yükseliş trendi\n"
            "- Negatif momentum: Düşüş trendi\n\n"
            "🎯 En Yüksek Momentuma Sahip 10 Hisse:\n\n"
        )
        
        results = []
        for symbol in BIST100_SYMBOLS:
            result = get_momentum_analysis(symbol)
            if result:
                current_price, momentum = result
                results.append((symbol, current_price, momentum))
        
        results = sorted(results, key=lambda x: x[2], reverse=True)[:10]
        response = momentum_explanation
        for stock in results:
            response += f"Hisse: {stock[0]}\nGüncel Fiyat: {stock[1]:.2f}\nMomentum: %{stock[2]:.2f}\n\n"
        
        await query.message.reply_text(response)
        await show_menu(update, context)

    elif choice == "8":
        await query.message.reply_text("Lütfen momentum analizi yapmak istediğiniz hisse kodunu gönderin.")
        context.user_data['mode'] = 'momentum_analysis'

    elif choice == "9":
        response = "🌟 BIST 100'de En İyi 5 Hisse Analizi 🌟\n\n"
        
        # Tüm analizleri yapıp puanlama sistemi oluşturalım
        stock_scores = {}
        
        # Her hisse için analizleri yapalım
        for symbol in BIST100_SYMBOLS:
            score = 0
            
            # MA Analizi
            ma_result = get_ma_analysis(symbol)
            if ma_result:
                current_price, ma50, ma100, ma200 = ma_result
                # Fiyat MA'ların altındaysa puan ver
                if current_price < ma50: score += 1
                if current_price < ma100: score += 1
                if current_price < ma200: score += 1
            
            # Yapay Zeka Analizi
            ai_result = analyze_stock(symbol)
            if ai_result:
                accuracy, suggestion, _ = ai_result
                if suggestion == "Al": score += 2
                if accuracy is not None:
                    score += accuracy
            
            # RSI Analizi
            rsi_result = get_rsi_analysis(symbol)
            if rsi_result:
                _, rsi = rsi_result
                if rsi < 40: score += 2  # Düşük RSI'ya daha fazla puan
                if rsi < 30: score += 1
            
            # Momentum Analizi
            momentum_result = get_momentum_analysis(symbol)
            if momentum_result:
                _, momentum = momentum_result
                if momentum < 0: score += 1  # Negatif momentum puan kazandırır
                if momentum < -5: score += 1
            
            stock_scores[symbol] = score
        
        # En yüksek puanlı 5 hisseyi seçelim
        top_stocks = sorted(stock_scores.items(), key=lambda x: x[1], reverse=True)[:5]
        
        for symbol, score in top_stocks:
            ma_result = get_ma_analysis(symbol)
            ai_result = analyze_stock(symbol)
            rsi_result = get_rsi_analysis(symbol)
            momentum_result = get_momentum_analysis(symbol)
            
            response += f"🔸 {symbol} (Puan: {score:.1f})\n"
            if ma_result:
                response += f"Fiyat: {ma_result[0]:.2f} TL\n"
                response += f"MA50/100/200: {ma_result[1]:.2f}/{ma_result[2]:.2f}/{ma_result[3]:.2f}\n"
            if ai_result:
                response += f"YZ Önerisi: {ai_result[1]} (Doğruluk: {ai_result[0]:.2f})\n"
            if rsi_result:
                response += f"RSI: {rsi_result[1]:.2f}\n"
            if momentum_result:
                response += f"Momentum: %{momentum_result[1]:.2f}\n"
            response += "\n"
        
        await query.message.reply_text(response)
        await show_menu(update, context)

async def check_stock(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    mode = context.user_data.get('mode', None)
    if mode is None:
        return
        
    stock_code = update.message.text.upper()
    if not stock_code.endswith('.IS'):
        stock_code += '.IS'

    if mode == 'ma_analysis':
        result = get_ma_analysis(stock_code)
        if result:
            current_price, ma50, ma100, ma200 = result
            status = "Alınabilir" if current_price < ma50 else "Alınmaz"
            await update.message.reply_text(
                f"Hisse: {stock_code}\n"
                f"Güncel Fiyat: {current_price:.2f}\n"
                f"MA50: {ma50:.2f}\n"
                f"MA100: {ma100:.2f}\n"
                f"MA200: {ma200:.2f}\n"
                f"Durum: {status}"
            )
            keyboard = [
                [InlineKeyboardButton("Ana Menüye Dön", callback_data="menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text("Ana menüye dönmek için tıklayın:", reply_markup=reply_markup)
        else:
            await update.message.reply_text("Geçersiz hisse kodu veya veri bulunamadı.")

    elif mode == 'ai_analysis':
        accuracy, suggestion, current_price = analyze_stock(stock_code)
        if accuracy is not None:
            await update.message.reply_text(
                f"Hisse: {stock_code}\n"
                f"Güncel Fiyat: {current_price:.2f}\n"
                f"Doğruluk: {accuracy:.2f}\n"
                f"Öneri: {suggestion}"
            )
            keyboard = [
                [InlineKeyboardButton("Ana Menüye Dön", callback_data="menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text("Ana menüye dönmek için tıklayın:", reply_markup=reply_markup)
        else:
            await update.message.reply_text("Geçersiz hisse kodu veya veri bulunamadı.")

    elif mode == 'rsi_analysis':
        result = get_rsi_analysis(stock_code)
        if result:
            current_price, rsi = result
            if rsi < 30:
                yorum = "Aşırı satım bölgesinde. Alım fırsatı olabilir."
            elif rsi > 70:
                yorum = "Aşırı alım bölgesinde. Satış fırsatı olabilir."
            elif rsi < 50:
                yorum = "Satış baskısı var."
            else:
                yorum = "Alım baskısı var."
                
            await update.message.reply_text(
                f"Hisse: {stock_code}\n"
                f"Güncel Fiyat: {current_price:.2f}\n"
                f"RSI Değeri: {rsi:.2f}\n"
                f"Yorum: {yorum}"
            )
            keyboard = [
                [InlineKeyboardButton("Ana Menüye Dön", callback_data="menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text("Ana menüye dönmek için tıklayın:", reply_markup=reply_markup)
        else:
            await update.message.reply_text("Geçersiz hisse kodu veya veri bulunamadı.")

    elif mode == 'momentum_analysis':
        result = get_momentum_analysis(stock_code)
        if result:
            current_price, momentum = result
            if momentum > 5:
                yorum = "Güçlü yükseliş trendi"
            elif momentum > 0:
                yorum = "Zayıf yükseliş trendi"
            elif momentum > -5:
                yorum = "Zayıf düşüş trendi"
            else:
                yorum = "Güçlü düşüş trendi"
                
            await update.message.reply_text(
                f"Hisse: {stock_code}\n"
                f"Güncel Fiyat: {current_price:.2f}\n"
                f"Momentum: %{momentum:.2f}\n"
                f"Yorum: {yorum}"
            )
            keyboard = [
                [InlineKeyboardButton("Ana Menüye Dön", callback_data="menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text("Ana menüye dönmek için tıklayın:", reply_markup=reply_markup)
        else:
            await update.message.reply_text("Geçersiz hisse kodu veya veri bulunamadı.")

if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_choice))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_stock))
    application.run_polling()