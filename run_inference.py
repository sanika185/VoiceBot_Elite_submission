import pandas as pd
import os

from modules.response_gen import generate_response

INPUT_PATH = "test.csv"
OUTPUT_PATH = "output/responses.csv"

def main():
    try:
        df = pd.read_csv(INPUT_PATH)

        if "Questions" not in df.columns:
            raise ValueError("Input CSV must contain a 'Questions' column.")

        responses = []

        for question in df["Questions"]:
            question = str(question).strip()
            response = generate_response(question)
            responses.append(response)

        df["Responses"] = responses
        os.makedirs("output", exist_ok=True)
        df.to_csv(OUTPUT_PATH, index=False, encoding='utf-8')

        print(f"✅ Inference complete. Responses saved to {OUTPUT_PATH}")
    except Exception as e:
        print(f"[ERROR] Failed to run inference: {e}")

if __name__ == "__main__":
    main()
