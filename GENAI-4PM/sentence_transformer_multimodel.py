from sentence_transformers import SentenceTransformer

# 1. Load a model that supports both text and images
model = SentenceTransformer("Qwen/Qwen3-VL-Embedding-2B")

# 2. Encode images from URLs
img_embeddings = model.encode([
    "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/tasks/car.jpg",
    "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/bee.jpg",
])

# 3. Encode text queries (one matching + one hard negative per image)
text_embeddings = model.encode([
    "A green car parked in front of a yellow building",
    "A red car driving on a highway",
    "A bee on a pink flower",
    "A wasp on a wooden table",
])

# 4. Compute cross-modal similarities
similarities = model.similarity(text_embeddings, img_embeddings)
print(similarities)
# tensor([[0.5115, 0.1078],
#         [0.1999, 0.1108],
#         [0.1255, 0.6749],
#         [0.1283, 0.2704]])