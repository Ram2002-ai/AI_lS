# create prompts using templates

def create_summary_prompt(text):
    prompt=f"Summarize the following text:\n{text}"
    return prompt.format(text=text)

# Example usage of  using the template function
input_text="Artificial Intelligence is transforming the world by enabling machines to learn from data and make decisions"
summary_prompt=create_summary_prompt(input_text)
print("Generated Summary Prompt:", summary_prompt)