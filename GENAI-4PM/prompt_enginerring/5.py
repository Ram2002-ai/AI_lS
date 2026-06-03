# generating multiple prompts using dynamically list and strings

def generate_prompts_from_data(data_list):
    prompts=[]
    for data in data_list:
        prompt=f"write a story about {data}."
        prompts.append(prompt)
    return prompts

# Example usage
topics=["squad game", "space adventure", "mystery novel"]
generated_prompts=generate_prompts_from_data(topics)
for prompt in generated_prompts:
    print("Generated Prompt:", prompt)