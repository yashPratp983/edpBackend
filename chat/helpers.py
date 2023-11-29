import json
import os

def create_assistant(client):
  assistant_file_path = 'assistant.json'

  if os.path.exists(assistant_file_path):
    with open(assistant_file_path, 'r') as file:
      assistant_data = json.load(file)
      assistant_id = assistant_data['assistant_id']
      print("Loaded existing assistant ID.")
  else:
    file = client.files.create(file=open("/home/yash/Downloads/Lec 8. Key management and distribution.pdf", "rb"),
                               purpose='assistants')

    assistant = client.beta.assistants.create(instructions="""
          Tell your disease so that we can help you.
          """,
                                              model="gpt-4-1106-preview",
                                              tools=[{
                                                  "type": "retrieval"
                                              }],
                                              file_ids=[file.id])

    # assistant=client.beta.assistants.create(name="Math Tutor",
    # instructions="You are a personal math tutor. Write and run code to answer math questions.",
    # tools=[{"type": "retrieval"}],
    # model="gpt-3.5-turbo-1106"
    # )

    with open(assistant_file_path, 'w') as file:
      json.dump({'assistant_id': assistant.id}, file)
      print("Created a new assistant and saved the ID.")

    assistant_id = assistant.id

  return assistant_id
