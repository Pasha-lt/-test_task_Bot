from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from pyppeteer import launch
from pyppeteer.errors import PyppeteerError, TimeoutError
from tempfile import NamedTemporaryFile
from config import TOKEN


bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
class ScreenshotForm(StatesGroup):
    url = State()


@dp.message_handler(commands=['start'])
async def process_hello(message: types.Message):
    await bot.send_message(message.from_user.id,  'Приветствую\n Пишите адрес сайта и мы вам сделаем скриншот.')


@dp.message_handler()
async def process_url(message: types.Message, state: FSMContext):
    await message.reply('Делаю скриншот...')
    browser = await launch()
    try:
        page = await browser.newPage()
        url = message.text
        if not url.startswith('http'):
            url = 'http://' + url
            print(url)
        await page.goto(url)
        
        #await page.setViewport(viewport=dict(width=1920, height=1085))
        # Если закоментируем эту часть кода тогда будут сохраняться 'длинные сайты' но из-за        
        # большого размера изображения принтскрин будет плохого качества. 
        # способ обхода, отельно сохраняем и отправляем пользователю.
        
        with NamedTemporaryFile() as fp:
            await page.screenshot(path=fp.name, type='jpeg', quality=200, fullPage=True)
            await message.reply_photo(fp.file)
    except (PyppeteerError, TimeoutError) as e:
        await message.reply('Ошибка, обратитесь к разработчику 093-128-22-25')
    finally:
        await state.finish()
        await browser.close()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
