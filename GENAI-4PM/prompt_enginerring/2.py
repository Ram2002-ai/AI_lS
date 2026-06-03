# create a prompt using user input
def create_prompt():
    topic=input("Enter a topic for the story: ")
    tone=input("Enter the tone of the story (e.g., humorous, serious,adventurous): ")

    prompt=f"write a {tone} story about {topic}."
    return prompt

# Create a prompt using the function
generated_prompt = create_prompt()
print("Generated Prompt:", generated_prompt)