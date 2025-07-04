import os
import random
from datetime import datetime, timedelta
import time
import re
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

model = ChatGoogleGenerativeAI(
    google_api_key="AIzaSyDuNe3K1AABInkX9xFzFPMRJe90WD0q10s",
    model="gemini-1.5-flash",
    temperature=0.9,
)

OUTPUT_FILE_NAME = "./data/generated_tickets.txt"
NUMBER_OF_TICKETS_TO_GENERATE = 10000
TICKETS_PER_BATCH = 15

PROGRAMMATIC_START_ID = 10000

CURRENT_DATE = datetime(2025, 6, 18)
DATE_RANGE_DAYS = 365

ticket_generation_prompt = PromptTemplate(
    input_variables=["num_tickets", "start_date", "end_date"],
    template="""Generate {num_tickets} unique technical support tickets. Each ticket must follow this exact format on a new line:
    "Ticket #ID: Description - Status: [New/Investigating/Resolved] - Created:YYYY-MM-DD"

    Pay close attention to the spacing, especially after 'Created:'. There MUST be a space between 'Created:' and the date.

    Ensure:
    - ID is a unique 5-digit number (between 10001 and 99999).
    - Description is a concise, plausible IT-related issue for a service desk. **Vary these descriptions significantly and ensure each is a distinct problem.** Examples of issues include but are not limited to: "printer not responding", "email sync error", "software update failed", "network drive inaccessible", "login issues", "video conferencing problem", "laptop overheating", "account locked", "VPN connection issues", "account locked out", "microphone not detected", "application crashing", "hard drive full", "virus detected", "password reset needed", "monitor flickering", "keyboard input lag", "slow system performance", "external monitor not detected", "file corruption", "browser issues", "antivirus update failure", "keyboard shortcuts not working", "mouse not responding", "password expired", "two-factor authentication problem", "wifi intermittent connection", "lost data recovery request", "new software installation request", "hardware upgrade request", "server access denied".
    - Status is randomly one of 'New', 'Investigating', or 'Resolved'.
    - Created date is a random date between {start_date} and {end_date}.

    Example of desired output (note the space after 'Created:' and diverse descriptions):
    Ticket #12345: My keyboard is not responding. - Status: New - Created: 2025-03-10
    Ticket #98765: VPN connection keeps dropping frequently. - Status: Investigating - Created: 2025-06-01
    Ticket #54321: Unable to access shared network drive. - Status: Resolved - Created: 2025-01-25
    """
)

def generate_tickets():
    os.makedirs(os.path.dirname(OUTPUT_FILE_NAME), exist_ok=True)

    if os.path.exists(OUTPUT_FILE_NAME):
        try:
            os.remove(OUTPUT_FILE_NAME)
            print(f"Existing file '{OUTPUT_FILE_NAME}' deleted.")
        except OSError as e:
            print(f"Error deleting file '{OUTPUT_FILE_NAME}': {e}")
            return

    print(f"Starting ticket generation. Output will be saved to: {OUTPUT_FILE_NAME}")

    min_date = (CURRENT_DATE - timedelta(days=DATE_RANGE_DAYS)).strftime("%Y-%m-%d")
    max_date = (CURRENT_DATE + timedelta(days=DATE_RANGE_DAYS)).strftime("%Y-%m-%d")

    tickets_generated_count = 0
    generated_ids = set()
    current_programmatic_id = PROGRAMMATIC_START_ID

    with open(OUTPUT_FILE_NAME, "w", encoding="utf-8") as f:
        while tickets_generated_count < NUMBER_OF_TICKETS_TO_GENERATE:
            try:
                current_prompt = ticket_generation_prompt.format(
                    num_tickets=TICKETS_PER_BATCH,
                    start_date=min_date,
                    end_date=max_date
                )

                generation_chain = LLMChain(llm=model, prompt=PromptTemplate(
                    input_variables=[],
                    template=current_prompt
                ))

                response = generation_chain.run({})

                generated_lines = [line.strip() for line in response.split('\n') if line.strip()]

                for line in generated_lines:
                    if tickets_generated_count >= NUMBER_OF_TICKETS_TO_GENERATE:
                        break

                    match = re.match(r"Ticket #(\d{5}): (.+?) - Status: (.+?) - Created: *(\d{4}-\d{2}-\d{2})", line)
                    
                    if match:
                        llm_generated_id = match.group(1)
                        description = match.group(2)
                        status = match.group(3)
                        created_date = match.group(4)

                        if llm_generated_id in generated_ids:
                            new_id = str(current_programmatic_id)
                            while new_id in generated_ids:
                                current_programmatic_id += 1
                                new_id = str(current_programmatic_id)
                            print(f"Warning: Duplicate LLM ID '{llm_generated_id}' found. Assigning new ID '{new_id}'.")
                            final_id_to_write = new_id
                        else:
                            final_id_to_write = llm_generated_id
                            
                        generated_ids.add(final_id_to_write)
                        
                        final_line = f"Ticket #{final_id_to_write}: {description} - Status: {status} - Created: {created_date}"
                        f.write(final_line + "\n")
                        tickets_generated_count += 1
                        current_programmatic_id += 1 
                    else:
                        print(f"Warning: Skipped malformed line from LLM: {line[:100]}...")
                
                print(f"Progress: {tickets_generated_count}/{NUMBER_OF_TICKETS_TO_GENERATE} tickets generated.")

                if tickets_generated_count >= NUMBER_OF_TICKETS_TO_GENERATE:
                    break

                time.sleep(0.5)

            except Exception as e:
                print(f"Error in batch: {e}")
                print("Retrying after a short delay...")
                time.sleep(5)

    print(f"\nFinished generating tickets. Total tickets written: {tickets_generated_count}")
    
    if tickets_generated_count < NUMBER_OF_TICKETS_TO_GENERATE:
        print(f"Note: Did not reach target of {NUMBER_OF_TICKETS_TO_GENERATE} tickets due to errors or LLM not producing enough lines per request.")

    print(f"Check '{OUTPUT_FILE_NAME}' for your generated data.")

if __name__ == "__main__":
    generate_tickets()