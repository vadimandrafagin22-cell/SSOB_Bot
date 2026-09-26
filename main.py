import asyncio
import random
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

# =========================================================
# ВСТАВЬ СВОЙ ТОКЕН НИЖЕ:
# =========================================================
BOT_TOKEN = "8985323016:AAF3SW30gUQMMZkXSQIwq3AElsKQLYLqb3k"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


# Состояния прохождения
class Quest(StatesGroup):
    step_1_password = State()
    step_2_buttons = State()


# Вспомогательная функция для симуляции "зависания"
async def fake_lag(message: types.Message, seconds: float = 3.0):
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    await asyncio.sleep(seconds)


# --- 1. СТАРТ: Вежливый ассистент ---
@dp.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🛡️ Подтвердить статус VIP",
                    callback_data="confirm_status",
                )
            ]
        ]
    )

    await message.answer(
        "⚙️ **Служба «SafeDelivery»**\n\n"
        "Здравствуйте! Я ваш персональный цифровой ассистент.\n"
        "На ваше имя зафиксирована передача закрытого контейнера [СЕКРЕТНО].\n\n"
        "Пожалуйста, подтвердите вашу личность для получения доступа.",
        parse_mode="Markdown",
        reply_markup=kb,
    )


# --- 2. ВЗЛОМ: Анонимы перехватывают управление ---
@dp.callback_query(F.data == "confirm_status")
async def hacking_event(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    # Симуляция сбоя через редактирование текста
    await callback.message.edit_text("🔄 Идентификация... [10%]")
    await asyncio.sleep(1)
    await callback.message.edit_text("🔄 И̶д̶е̵н̴т̶и̶ф̵и̷к̶а̵ц̶и̶я̷... [45%]")
    await asyncio.sleep(1)
    await callback.message.edit_text("⚠️ **ERROR 0x8800: UNKNOWN INJECTION**")
    await asyncio.sleep(1.5)

    await callback.message.answer(
        "☠️ **СИСТЕМА ЗАХВАЧЕНА ГРУППОЙ X-NULL**\n\n"
        "Привет, именинник! Твой ассистент теперь под нашим контролем.\n"
        "Если хочешь добраться до своего подарка, придется пройти наши тесты.\n\n"
        "🔒 **Блок #1:** Введи секретный код доступа.\n"
        "*(Подсказка: Твоя любимая фразочка / дата рождения / слово, которое знают только свои)*",
        parse_mode="Markdown",
    )

    await state.set_state(Quest.step_1_password)


# --- 3. ШАГ 1: Ввод пароля ---
@dp.message(Quest.step_1_password)
async def check_password(message: types.Message, state: FSMContext):
    # Укажи правильный пароль (в нижнем регистре)
    RIGHT_PASSWORD = "секрет"  # <-- ПОМЕНЯЙ НА СВОЙ ПАРОЛЬ

    if message.text.strip().lower() == RIGHT_PASSWORD:
        await fake_lag(message, 2.5)
        await message.answer(
            "🟢 **КОД ПРИНЯТ.** Но это было слишком просто...\n\n"
            "Переходим к модулю дестабилизации интерфейса. "
            "Посмотрим, сможешь ли ты нажать нужную кнопку, когда система рушится!"
        )

        await send_glitch_buttons(message, state)
    else:
        await fake_lag(message, 3.5)

        glitch_texts = [
            "❌ N̶O̵P̷E̷! Ошибка доступа. Уровень дестабилизации: 45%",
            "⚠️ В̵Н̶И̸М̷А̷Н̸И̴Е̸! Система теряет связь с сервером...",
            "⚙️ *Ассистент:* По..пожалуйста, вводи точнее, они меня п̶е̴р̶е̸п̶р̸о̶ш̷и̴в̸а̴ю̴т̷...",
        ]

        await message.answer(
            f"{random.choice(glitch_texts)}\n\nПопробуй ввести пароль еще раз!"
        )


# --- 4. ШАГ 2: Перепутанные кнопки ---
async def send_glitch_buttons(message: types.Message, state: FSMContext):
    await state.set_state(Quest.step_2_buttons)

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔴 КРАСНАЯ", callback_data="btn_wrong"
                ),
                InlineKeyboardButton(
                    text="🔵 СИНЯЯ", callback_data="btn_wrong"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🟢 ЗЕЛЕНАЯ", callback_data="btn_green"
                ),
                InlineKeyboardButton(
                    text="🟡 ЖЕЛТАЯ", callback_data="btn_wrong"
                ),
            ],
        ]
    )

    await message.answer(
        "⚡ **ПРОТОКОЛ ХАОСА**\n\n"
        "Задание: Нажми на **ЗЕЛЕНУЮ** кнопку, чтобы восстановить питание бота!",
        parse_mode="Markdown",
        reply_markup=kb,
    )


@dp.callback_query(Quest.step_2_buttons, F.data == "btn_wrong")
async def button_wrong(callback: types.CallbackQuery):
    await callback.answer("❌ ОШИБКА!", show_alert=True)
    await asyncio.sleep(2)

    await callback.message.edit_text(
        "💥 **СИСТЕМА КРИТИЧЕСКИ ПЕРЕГРУЖЕНА!**\n\n"
        "Кнопки не слушают команды! Попробуй еще раз (если сможешь).",
        reply_markup=callback.message.reply_markup,
    )


@dp.callback_query(Quest.step_2_buttons, F.data == "btn_green")
async def button_green_troll(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    await callback.message.edit_text("⏳ Обработка клика...")
    await asyncio.sleep(3.0)

    await callback.message.edit_text(
        "😈 **Ха-ха! Мы переменили сигналы!**\n"
        "Зеленый цвет под напряжением! Бот полностью выведен из строя!"
    )

    await asyncio.sleep(2)
    msg = await callback.message.answer("Z̷a̶l̵g̶o̷_̷E̸r̵r̶o̸r̸_̷9̸9̸%̸")

    for text in ["F̵A̸T̴A̶L̵ ̷E̸R̵R̵O̷R̴", "S̶Y̵S̷T̵E̷M̶ ̴D̶O̷W̶N̸", "💥 100% OVERLOAD"]:
        await asyncio.sleep(1)
        await msg.edit_text(text)

    await asyncio.sleep(2)

    # --- 5. ФИНАЛ ---
    await msg.answer(
        "🎉 **ПРОТОКОЛ ЗАВЕРШЕН!**\n\n"
        "Ладно, ладно! Ты прошел через этот цифровой ад и доказал свой уровень.\n"
        "Анонимы отступают, а твой подарок находится...\n\n"
        "📍 **В запечатанной коробке под столом / у ведущего в руках!**\n\n"
        "С Днём Рождения! 🎂",
        parse_mode="Markdown",
    )

    await state.clear()


async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
