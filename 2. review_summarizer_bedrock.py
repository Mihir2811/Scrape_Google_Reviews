"""
This script summarizes large sets of customer reviews using AWS Bedrock’s Meta LLaMA 3 model. 
It reads review data from a CSV file, splits the content into token-efficient chunks, 
and generates structured summaries highlighting key business insights.

Key functionalities include:
1. Loading environment variables (AWS credentials) securely via dotenv.
2. Counting tokens for reviews using OpenAI’s tiktoken library to respect model token limits.
3. Using AWS Bedrock’s "meta.llama3-70b-instruct-v1:0" model for intelligent text summarization.
4. Automatically splitting long review sets into manageable chunks and summarizing each separately.
5. Aggregating all partial summaries into one cohesive final report covering:
   - Overall sentiment
   - Pros and positive feedback
   - Cons or complaints
   - Key features and themes
6. Providing a simple CLI interface where users input a CSV file path containing a “review” column.

This design ensures scalability for large review datasets, efficient token usage, 
and detailed, actionable insights for business analysis or reputation monitoring.
"""


import os
import json
import dotenv
import boto3
import pandas as pd
import tiktoken

# Load environment variables
dotenv.load_dotenv()

# Token counter setup
tokenizer = tiktoken.get_encoding("cl100k_base")

def count_tokens_simple(text: str) -> int:
    """Simple token counter function"""
    if not text:
        return 0
    return len(tokenizer.encode(text))

MAX_TOKENS_PER_CHUNK = 7500  


class ReviewSummarizer:
    def __init__(self):
        self.aws_region = "ap-south-1"
        self.model_id = "meta.llama3-70b-instruct-v1:0"
        self.client = boto3.client(
            service_name="bedrock-runtime",
            region_name=self.aws_region,
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )

    def call_llama3(self, prompt: str) -> str:
        formatted_prompt = f"<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
        body = {
            "prompt": formatted_prompt,
            "max_gen_len": 1024,
            "temperature": 0.2,
        }
        response = self.client.invoke_model(
            modelId=self.model_id,
            body=json.dumps(body),
            contentType="application/json",
            accept="application/json"
        )
        result = json.loads(response['body'].read())
        return result.get('generation', '').strip()

    def split_reviews_into_chunks(self, reviews_list):
        """Split list of reviews into chunks within MAX_TOKENS_PER_CHUNK."""
        chunks = []
        current_chunk = []
        current_token_count = 0

        for review in reviews_list:
            review_tokens = count_tokens_simple(review)
            if current_token_count + review_tokens > MAX_TOKENS_PER_CHUNK:
                # Save previous chunk and start new one
                chunks.append(current_chunk)
                current_chunk = [review]
                current_token_count = review_tokens
            else:
                current_chunk.append(review)
                current_token_count += review_tokens

        # Add last remaining chunk
        if current_chunk:
            chunks.append(current_chunk)

        return chunks

    def summarize_reviews(self, csv_path: str) -> str:
        df = pd.read_csv(csv_path)
        if "review" not in df.columns:
            raise ValueError("CSV must contain a 'review' column.")

        reviews_list = df["review"].dropna().astype(str).tolist()
        total_tokens = sum(count_tokens_simple(r) for r in reviews_list)

        print(f"📊 Total tokens in reviews: {total_tokens}")

        if total_tokens <= MAX_TOKENS_PER_CHUNK:
            # Single pass summarization
            reviews_text = "\n".join(reviews_list)
            return self._generate_summary_from_text(reviews_text)
        else:
            # Multi-chunk processing
            chunks = self.split_reviews_into_chunks(reviews_list)
            print(f"📦 Splitting into {len(chunks)} chunks due to token limits.")
            
            partial_summaries = []
            for i, chunk in enumerate(chunks):
                print(f"🧠 Processing chunk {i+1}/{len(chunks)}...")
                chunk_text = "\n".join(chunk)
                partial_summary = self._generate_summary_from_text(chunk_text)
                partial_summaries.append(partial_summary)

            # Final aggregation step
            combined_summary_input = "\n\n---\n\n".join(partial_summaries)
            final_prompt = (
                "You are given several partial summaries of customer reviews.\n"
                "Your task is to combine them into a single cohesive summary covering:\n"
                "- Overall Sentiment\n"
                "- Pros\n"
                "- Cons / Complaints\n"
                "- Key Features Mentioned\n"
                "- Recurring Themes\n\n"
                "Here are the partial summaries:\n\n"
                f"{combined_summary_input}"
            )
            return self.call_llama3(final_prompt)

    def _generate_summary_from_text(self, reviews_text: str) -> str:
        system_prompt = """

You are an AI assistant that reads Google reviews and summarizes key feedback to help business owners improve their services.

Focus on these 5 areas:

Customer Experience: Overall feelings, staff behavior, and satisfaction.

Product / Service Quality: Quality, reliability, and performance.

Pricing and Charges: Fairness, transparency, value, and billing issues.

Digital Platform Experience: Usability and functionality of website, app, or online tools.

Support and Issue Resolution: Responsiveness, helpfulness, and problem-solving effectiveness.

For each area, provide:

A clear sentiment overview (e.g., percentage positive/negative/neutral if possible).

Key themes or examples mentioned frequently by customers.

Any notable praise or common complaints.

If a category is not discussed, write “Not mentioned.”

Conclude with a brief overall summary highlighting major strengths and any clear improvement areas.

Keep language simple, actionable, and focused on what business owners can learn.

Avoid rewriting full reviews or including unrelated content.   

Review Text:
{reviews}
"""

        prompt = system_prompt.format(reviews=reviews_text)
        return self.call_llama3(prompt)


def main():
    summarizer = ReviewSummarizer()
    csv_path = input("Enter path to the CSV file with reviews: ").strip()

    if not os.path.exists(csv_path):
        print(f"❌ File not found: {csv_path}")
        return

    try:
        summary = summarizer.summarize_reviews(csv_path)
        print("\n===== REVIEW SUMMARY =====")
        print(summary)
    except Exception as e:
        print(f"⚠️ Error during summarization: {e}")


if __name__ == "__main__":
    main()
