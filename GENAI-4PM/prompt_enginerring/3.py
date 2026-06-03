#  create a prompt using python loops and conditions

topics=["squad game", "space adventure", "mystery novel"]
tones=["humorous", "serious", "adventurous"]

prompts=[]

for topic in topics:
    for tone in tones:
        prompt=f"write a {tone} story about {topic}."
        prompts.append(prompt)

# Print all generated prompts
for prompt in prompts:
    print("Generated Prompt:", prompt)
    