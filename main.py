import asyncio
import aiohttp
from telebot.async_telebot import AsyncTeleBot  # Importação correta
from telebot import types
from discord import Webhook

TOKEN_TELEGRAM = ""
DISCORD_WEBHOOK_URL = ""

# Crie a instância do bot assíncrono corretamente
bot = AsyncTeleBot(TOKEN_TELEGRAM)

@bot.message_handler(func=lambda msg: "dc" in msg.text.lower())
async def enviar_menu(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📢 Enviar para Discord", callback_data="enviar_discord"))
    await bot.send_message(message.chat.id, "Clique para enviar:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "enviar_discord")
async def enviar_para_discord(call):
    try:
        # Tratamento robusto do username
        user = call.from_user
        username = (
            f"@{user.username}" 
            if user.username 
            else f"{user.first_name or 'Usuário'}"
        )

        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(DISCORD_WEBHOOK_URL, session=session)
            await webhook.send(f"🚨 Mensagem de {username} via Telegram!") # {username} agora esta aparecendo meu nome 'crepti' e meu id 
        await bot.answer_callback_query(call.id, "✅ Enviado para Discord!")
    except Exception as e:
        print(f"Erro ao enviar para Discord: {e}")
        await bot.answer_callback_query(call.id, "❌ Falha ao enviar!")

async def main():
    await bot.polling(non_stop=True)

if __name__ == '__main__':
    asyncio.run(main())
