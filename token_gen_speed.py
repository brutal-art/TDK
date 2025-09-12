import time
import torch
from transformers import AutoTokenizer


def measure_token_generation_speed(model_name, prompt, max_length=256):
    """
    Prompts a language model and measures the token generation speed.

    Args:
        model_name (str): The name or path of the pre-trained model to use.
        prompt (str): The prompt to feed to the model.
        max_length (int): The maximum length of the generated sequence.

    Returns:
        float: The average token generation speed in tokens per second.  Returns None if an error occurs.
    """
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoTokenizer.from_pretrained(model_name).from_pretrained("ai/gemma3")  # Replace with your model

        input_ids = tokenizer(prompt, return_tensors="pt")

        start_time = time.time()
        output = model.generate(input_ids.input_ids, max_length=max_length)
        end_time = time.time()

        generated_tokens = len(output[0])  # Token count in the generated output
        elapsed_time = end_time - start_time

        if elapsed_time > 0:
            speed = generated_tokens / elapsed_time
            return speed
        else:
            print("Error: Time elapsed was zero.  Check your model and prompt.")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


if __name__ == "__main__":
    model_name = "gpt2"  # Or your preferred model
    prompt = "The quick brown fox jumps over the lazy"

    speed = measure_token_generation_speed(model_name, prompt)

    if speed is not None:
        print(f"Token generation speed: {speed:.2f} tokens/second")