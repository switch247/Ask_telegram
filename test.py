
# Handler for button clicks
@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def handle_button_click(message: types.Message):
    if message.text == "Ask qn":
        await message.answer("You clicked 'Ask qn' button!")
    elif message.text == "Hire tutor":
        await message.answer("You clicked 'Hire tutor' button!")
    elif message.text == "Materials":
        await message.answer("You clicked 'Materials' button!")
    elif message.text == "Additional services":
        await message.answer("You clicked 'Additional services' button!")

# Handler for the "Ask qn" button
@dp.message_handler(lambda message: message.text == "Ask qn")
async def ask_question(message: types.Message):
    # Prompt the user to ask a question
    await message.answer("Please enter your question:")

    # Set the state to store the user's question
    await SomeState.waiting_for_question.set()


# Handler for storing the user's question
@dp.message_handler(state=SomeState.waiting_for_question)
async def store_question(message: types.Message, state: FSMContext):
    # Store the user's question in the state
    await state.update_data(question=message.text)

    # Ask for approval from channel admins
    await message.answer("Your question has been received. Awaiting approval from channel admins.")


# Handler for approving the question and posting it to the channel
@dp.message_handler(lambda message: message.text == "Approve", is_chat_admin=True)
async def approve_question(message: types.Message, state: FSMContext):
    # Get the stored question from the state
    data = await state.get_data()
    question = data.get('question')

    # Post the question to the channel
    await bot.send_message(chat_id='CHANNEL_ID', text=question)

    # Reset the state
    await state.finish()

    # Notify the user
    await message.answer("Your question has been approved and posted to the channel.")

# Define your handlers
@dp.message_handler(state=SomeState.waiting_for_question)
async def store_question(message: types.Message, state: FSMContext):
    # Store the user's question in the state
    await state.update_data(question=message.text)

    # Ask for approval from channel admins
    await ...

@dp.message_handler(Command('post_question'))
async def post_question(message: types.Message):
    # Create a new conversation state
    async with dp.current_state(chat=message.chat.id, user=message.from_user.id) as state:
        # Get the stored question from the state
        data = await state.get_data()
        question = data.get('question')

        # Post the question to the channel
        await bot.send_message(chat_id='CHANNEL_ID', text=question)

        # Reset the state
        await state.reset_state()

]