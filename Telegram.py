from multiprocessing import Process
from pathlib import Path
import time

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

BASE_DIR = Path(__file__).resolve().parent
PRODUCTS = {
    "laptop": {
        "id": "laptop",
        "name": "Acer Aspire 5",
        "price": "Bs 3.450",
        "image": "image/lap1.jpg",
    },
    "teclado": {
        "id": "teclado",
        "name": "Teclado Streamer RGB",
        "price": "Bs 690",
        "image": "image/tec1.jpg",
    },
    "monitor": {
        "id": "monitor",
        "name": "Samsung Odyssey G5",
        "price": "Bs 2.950",
        "image": "image/mon1.jpg",
    },
}

def simulacion_pago():
    print("Iniciando validación bancaria en Valve Store...")
    for i in range(1, 5):
        print(f"Comprobando pago... {i}")
        time.sleep(1)
    print("Pago aprobado en segundo plano.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "¡Bienvenido a Valve Store!\n\n"
        "Usa /ayuda para ver todos los comandos o /catalogo para ver los productos."
    )

async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "COMANDOS DE VALVE STORE\n\n"
    "1. /start - Iniciar el bot\n"
      "2. /ayuda - Lista completa de comandos\n"
        "3. /catalogo - Ver catálogo de productos\n"
        "4. /laptop - Ver imagen y precio de Laptop\n"
        
        
     "5. /teclado - Ver imagen y precio de Teclado\n"
        "6. /monitor - Ver imagen y precio de Monitor\n"
        "7. /comprar - Confirmación de compra\n"
        "8. /procesarpago - Ejecutar pago \n"
     "9. /comprobante - Descargar factura PDF\n"
        "10. /gracias - Escuchar audios"
    )

async def catalogo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "CATÁLOGO VALVE STORE\n\n"
        + "\n".join(
            f"{index}. /{product['id']} - {product['name']} ({product['price']})"
            for index, product in enumerate(PRODUCTS.values(), start=1)
        )
    )

async def comprar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "CONFIRMACIÓN DE COMPRA\n\n"
        "Para realizar el pago de tu producto ejecuta:\n"
        "/procesarpago"
    )

async def procesarPago(update: Update, context: ContextTypes.DEFAULT_TYPE):
    proceso = Process(target=simulacion_pago)
    proceso.start()

    await update.message.reply_text(
        "Comprobando pago...\n"
        "Procesando pago\n"
        "¡Pago exitoso! ✅\n"
        "Descarga tu recibo con /comprobante"
    )

async def laptopEnviar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    product = PRODUCTS["laptop"]
    context.user_data["producto_actual"] = product["id"]
    with open(BASE_DIR / product["image"], "rb") as laptop:
        await update.message.reply_photo(
            photo=laptop, 
            caption=f"{product['name']} - Precio: {product['price']} | Para comprar ejecuta: /comprar"
        )

async def tecladoEnviar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    product = PRODUCTS["teclado"]
    context.user_data["producto_actual"] = product["id"]
    with open(BASE_DIR / product["image"], "rb") as teclado:
        await update.message.reply_photo(
            photo=teclado, 
            caption=f"{product['name']} - Precio: {product['price']} | Para comprar ejecuta: /comprar"
        )

async def monitorEnviar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    product = PRODUCTS["monitor"]
    context.user_data["producto_actual"] = product["id"]
    with open(BASE_DIR / product["image"], "rb") as monitor:
        await update.message.reply_photo(
            photo=monitor, 
            caption=f"{product['name']} - Precio: {product['price']} | Para comprar ejecuta: /comprar"
        )


async def pdfEnviar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open("pdfs/factura.pdf", "rb") as pdf:
        await update.message.reply_document(
            document=pdf, 
            filename="factura.pdf",
            caption="Factura de compra. Para escuchar tu agradecimiento ejecuta: /gracias"
        )


async def audioEnviar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    product = PRODUCTS.get(context.user_data.get("producto_actual"), PRODUCTS["laptop"])
    with open(product["audio"], "rb") as audio:
        await update.message.reply_audio(
            audio=audio, 
            caption=f"¡Muchas gracias por tu compra en Valve Store! Disfruta tu nuevo/a {product['name']}.\n\nPara seguir explorando ejecuta: /catalogo"
        )

if __name__ == "__main__":
    TOKEN = ""

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ayuda", ayuda))
    app.add_handler(CommandHandler("catalogo", catalogo))
    app.add_handler(CommandHandler("laptop", laptopEnviar))
    app.add_handler(CommandHandler("teclado", tecladoEnviar))
    app.add_handler(CommandHandler("monitor", monitorEnviar))
    app.add_handler(CommandHandler("comprar", comprar))
    app.add_handler(CommandHandler("procesarpago", procesarPago))
    app.add_handler(CommandHandler("comprobante", pdfEnviar))
    app.add_handler(CommandHandler("gracias", audioEnviar))

    print("Conectando con Telegram...", flush=True)
    app.run_polling()