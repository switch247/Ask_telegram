import csv, logging
from aiogram import Bot, Dispatcher, types,executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext


# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token="6279551458:AAGtGSJpADrw3IEK-230oUlu0ebTNMEji-s")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# File path for storing questions
QUESTIONS_FILE = "questions.csv"

# Define the conversation states
class SomeState(StatesGroup):
    waiting_for_question = State()
    waiting_for_approval = State()


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [ "Ask Question" , "Hire Tutor", "Materials", "Additional Services"]
    keyboard.add(*buttons)
    await message.answer("Welcome! Please select an option:", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "Hire Tutor")
async def ask_question(message: types.Message):
     # Read rows from the tutors.csv file
    with open('tutors.csv', 'r') as file:
       reader = csv.reader(file)
       tutors = list(reader)
        # Send the tutors to the user
       for tutor in tutors:
           tutor_info = f"Name: {tutor[0]} \n Subject: {tutor[1]} \n Rate: {tutor[2]}"
           await message.answer(tutor_info)
    # await message.answer("Hire Tutor coming soon..:")

@dp.message_handler(lambda message: message.text == "Materials")
async def ask_question(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["material catagory 1", "material catagory 2"]
    keyboard.add(*buttons)
    await message.answer("Materials coming soon..:", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "Additional Services")
async def ask_question(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Submit Assignment", "submit pre ayinebeim"]
    keyboard.add(*buttons)
    await message.answer("Additional Services:", reply_markup=keyboard)
    # await message.answer("Additional Services coming soon..")


@dp.message_handler(lambda message: message.text == "Ask Question")
async def ask_question(message: types.Message):
    await message.answer("Please enter your question:")
    await SomeState.waiting_for_question.set()
    # await dp.register_message_handler(message, process_question)

@dp.message_handler(state=SomeState.waiting_for_question)
async def process_question(message: types.Message , state: FSMContext):
    question = message.text
    user_id = message.from_user.id
    current_time = message.date

    # Store the question in a CSV file
    with open(QUESTIONS_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([question, current_time, user_id, False])

    await message.answer("Your question has been submitted for approval.")
    # Reset the state
    await state.finish()


@dp.message_handler(commands=['approve'])
async def approve_question(message: types.Message):
    # if message.from_user.id in [admin.user.id for admin in await bot.get_chat_administrators(message.chat.id)]:

    # Retrieve the questions from the CSV file
    questions = []
    with open(QUESTIONS_FILE, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            # print(row)
            if "False"== row[3]:  # Check if the question is not already approved
                questions.append(row)
    # print(questions)
    if not questions:
        await message.answer("No pending questions for approval.")
        return

    for i, question in enumerate(questions):
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        question_text = question[0]
        approve_button = types.InlineKeyboardButton(text=f"Approve Question {i+1}", callback_data=f"approve_{i}")
        keyboard.add(approve_button)
        await message.answer(f"Question {i+1}: {question_text}", reply_markup=keyboard)
    # else:
    #     await message.answer("You are not authorized to approve questions.")



@dp.callback_query_handler(lambda query: query.data.startswith('approve_'))
async def process_approval(query: types.CallbackQuery):
    
    question_index = int(query.data.split('_')[1])
    print(question_index)

    # Retrieve the questions from the CSV file
    questions = []
    with open(QUESTIONS_FILE, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if "False"== row[3]:  # Check if the question is not already approved
                questions.append(row)
    chat_idd =query.message.chat.id
    if question_index < len(questions):
        approved_question = questions[question_index][0]

        # Update the CSV file with the approved question
        questions[question_index][3] = True
        with open(QUESTIONS_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(questions)

        # Send the approved question to the group
        await bot.send_message(chat_id=chat_idd, text=approved_question)

        try:
            await bot.send_message(chat_id=chanel_or_group, text=approved_question)
            await query.answer("Question approved and sent to the group.")
        except:
            pass
    else:
        await query.answer("Invalid question index.")

chanel_or_group='@beertutorials1'
if __name__ == '__main__':
    # Start the bot
    try:
        executor.start_polling(dp)
    except Exception as e:
        logging.exception(e)
