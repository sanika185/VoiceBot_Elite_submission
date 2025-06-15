import pandas as pd
from modules.response_gen import generate_response
from translation import translate_to_hindi, translate_to_english

INPUT_FILE = "test.csv"
OUTPUT_FILE = "teamname_submissions.csv"

def main():
    try:
        # Load test questions
        df = pd.read_csv(INPUT_FILE)

        # Translate questions to Hindi
        df["Hindi_Questions"] = df["Questions"].apply(translate_to_hindi)

        # Generate responses using translated Hindi questions
        df["Responses"] = df["Hindi_Questions"].apply(generate_response)

        # Prepare final output: original English + Responses
        final_df = df[["Questions", "Responses"]]

        # Save to expected output file
        final_df.to_csv(OUTPUT_FILE, index=False)
        print(f"✅ Inference complete. Responses saved to {OUTPUT_FILE}")

    except Exception as e:
        print(f"[ERROR] Failed to run inference: {e}")

if __name__ == "__main__":
    main()
