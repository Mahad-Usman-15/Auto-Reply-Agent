from openai import BaseModel
import pyautogui
import time
import pyperclip
from agents import (AsyncOpenAI,Agent, RunContextWrapper,Runner,OpenAIChatCompletionsModel,
GuardrailFunctionOutput,
InputGuardrailTripwireTriggered,OutputGuardrailTripwireTriggered,input_guardrail,output_guardrail,set_tracing_disabled)
from dotenv import load_dotenv
import asyncio 
import os
load_dotenv()
set_tracing_disabled(disabled=True)
API_KEY=os.getenv("GEMINI_API_KEY")
# Make OpenAi client
client = AsyncOpenAI(
 api_key=API_KEY,
 base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
model=OpenAIChatCompletionsModel(
    openai_client=client,
    model="gemini-2.0-flash",
)
def is_last_message_from_sender(chat_log:str, sender_name="MU"):
    # Split the chat log into individual messages
    messages = chat_log.strip().split("/2024] ")[-1]
    if sender_name in messages:
        return True 
    return False


class Is_relevant(BaseModel):
    is_appropriate:bool
    reasoning:str
    
    
guardrailagent=Agent(
    name="GuardRail Agent",
    instructions="You have to make sure that the input is appropriate.It does not violate someone's sentiments",
       model=model,
)    
@input_guardrail()
async def check_user_input(ctx:RunContextWrapper[Is_relevant],agent,input):
    response=await Runner.run(
        guardrailagent,
        context=ctx.context,
        input=input,
    )
    return GuardrailFunctionOutput(
        output_info=response.final_output,
        tripwire_triggered=not response.final_output.is_appropriate
        
    )
 
ouput_guardrailagent=Agent(
    name="Output GuardRail Agent",
    instructions="You have to make sure that the output is appropriate.It does not violate someone's sentiments",
      model=model,
)    


@output_guardrail()
async def check_agent_output(ctx:RunContextWrapper[Is_relevant],agent,output):
    response=await Runner.run(
        ouput_guardrailagent,
        output,
        context=ctx.context,
       
    )
    return GuardrailFunctionOutput(
        output_info=response.final_output,
        tripwire_triggered=not response.final_output.is_appropriate
    )
    # Step 1: Click on the chrome icon at coordinates (988,1047)
pyautogui.click(942,1043)

time.sleep(1)  # Wait for 1 second to ensure the click is registered
while True:
    time.sleep(2)
    # Step 2: Drag the mouse from (1003, 237) to (2187, 1258) to select the text
    pyautogui.moveTo(969,523)
    pyautogui.dragTo(1712, 876, duration=2.0, button='left')  # Drag for 1 second

    # Step 3: Copy the selected text to the clipboard
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(2)  # Wait for 1 second to ensure the copy command is completed
    pyautogui.click(1655, 866)

    # Step 4: Retrieve the text from the clipboard and store it in a variable
    chat_history = pyperclip.paste()

    # Print the copied text to verify
    print(chat_history)
    print(is_last_message_from_sender(chat_history))
    if is_last_message_from_sender(chat_history):
     async def main():
         agent =Agent(
             name="Auto Reply Agent",
                      instructions= "You are a person named Mahad Usman who speaks Urdu as well as english. You are from Pakistan and you are a coder. You analyze chat history and roast people in a funny way. Output should be the next chat response (text message only).Do not start like this [21:02, 12/6/2025] Areeb",

          model=model,
         input_guardrails=[check_user_input],
         output_guardrails=[check_agent_output]
        )
         
         response = await Runner.run(
             agent,
             input=chat_history
         )
         pyperclip.copy(response.final_output)
         print(response.final_output)

        # Step 5: Click at coordinates (1808, 1328)
         pyautogui.click(1030, 969)
         time.sleep(1)  # Wait for 1 second to ensure the click is registered

        # Step 6: Paste the text
         pyautogui.hotkey('ctrl', 'v')
         time.sleep(1)  # Wait for 1 second to ensure the paste command is completed

        # Step 7: Press Enter
         pyautogui.press('enter')
    
     try:
      asyncio.run(main())
     except InputGuardrailTripwireTriggered:
         print("input Guardrail tripped")
     except OutputGuardrailTripwireTriggered:
         print("Output Guardrail Tripped")    
        