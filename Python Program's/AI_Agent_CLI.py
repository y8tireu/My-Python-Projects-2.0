#!/usr/bin/env python3
"""
CLI script for local text generation using GPT-J 6B.

- Attempts to use bitsandbytes 8-bit if user requests GPU and if CUDA is available.
- Otherwise falls back to standard half-precision (float16 or bfloat16) on CPU.
- After loading, you can enter multiple prompts in a loop until "exit" or "quit."
"""

import argparse
import sys
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from transformers import BitsAndBytesConfig

def parse_args():
    parser = argparse.ArgumentParser(
        description="Run GPT-J 6B text generation locally via CLI, with optional GPU acceleration."
    )
    parser.add_argument(
        "--use-gpu",
        action="store_true",
        help="Enable GPU acceleration if CUDA is available. Requires ~12GB VRAM for GPT-J."
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Choose a Torch dtype for fallback CPU
    # We'll use bfloat16 if supported, else float16
    compute_dtype = torch.bfloat16 if hasattr(torch, "bfloat16") else torch.float16

    # Decide if we can do bitsandbytes 8-bit
    # Only do 8-bit if user specifically wants GPU AND CUDA is available
    use_8bit = False
    device_map = "cpu"

    if args.use_gpu and torch.cuda.is_available():
        # We try using bitsandbytes 8-bit on GPU
        # If that fails, we catch the exception and fallback below
        use_8bit = True
        device_map = "auto"
        print("User requested GPU. CUDA is available. Attempting 8-bit GPU loading...")

    # Now prepare the quantization config
    # If use_8bit is True, we pass BitsAndBytesConfig with 8-bit
    # If not, we won't pass quantization_config at all, so we do standard half-precision
    bnb_config = None
    if use_8bit:
        bnb_config = BitsAndBytesConfig(load_in_8bit=True)

    print("\nLoading GPT-J 6B. This may take a while...")

    model_id = "EleutherAI/gpt-j-6B"
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_id)

        if bnb_config:
            # Attempt 8-bit loading on GPU
            model = AutoModelForCausalLM.from_pretrained(
                model_id,
                torch_dtype=compute_dtype,
                device_map=device_map,
                quantization_config=bnb_config
            )
        else:
            # Fallback: standard half-precision (CPU or GPU if manually forced)
            # Usually this will be CPU float16/bfloat16 if no GPU is requested or available
            model = AutoModelForCausalLM.from_pretrained(
                model_id,
                torch_dtype=compute_dtype,
                device_map=device_map
            )

        generator = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            device_map=device_map
        )
        print("Model loaded successfully.")

    except Exception as e:
        print(f"Error loading model: {e}")
        sys.exit(1)

    # Interactive loop
    print("\n--- Interactive GPT-J Session ---")
    print("Type 'exit' or 'quit' to end the session.\n")

    while True:
        user_input = input("Enter a prompt: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting...")
            break

        # If empty prompt, provide a default
        if not user_input:
            user_input = "Hello from GPT-J 6B!"

        # Generate text
        try:
            output = generator(
                user_input,
                max_new_tokens=100,     # You can tweak these default generation params
                temperature=0.7,
                top_p=0.9,
                do_sample=True,
                pad_token_id=generator.tokenizer.eos_token_id
            )
            text_out = output[0]["generated_text"]
            print(f"\n>>> {text_out}\n")
        except Exception as e:
            print(f"Error generating text: {e}")


if __name__ == "__main__":
    main()
