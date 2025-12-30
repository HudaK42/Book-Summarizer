
# import time
# import logging
# import torch
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
# from backend.chunking import smart_chunk_text, merge_chunk_summaries

# # ---------------- LOGGING ----------------
# logging.basicConfig(
#     filename="model_logs.log",
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s"
# )

# logger = logging.getLogger(__name__)

# # ---------------- DEVICE ----------------
# device = torch.device("cpu")

# # ---------------- LOAD MODEL ONCE ----------------
# MODEL_NAME = "sshleifer/distilbart-cnn-12-6"

# logger.info("Loading DistilBART model on CPU...")

# tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
# model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME).to(device)
# model.eval()

# logger.info("Model loaded successfully")


# # ---------------- MAIN SUMMARIZATION FUNCTION ----------------
# def summarize_text(text, max_input_length=1024, max_output_length=200):
#     """
#     Summarize text using chunking + DistilBART
#     Returns:
#         final_summary (str)
#         processing_time (float)
#         total_chunks (int)
#     """
#     start_time = time.time()

#     if not text or not text.strip():
#         return None, None, 0

#     # 1️⃣ Chunk text
#     chunk_data = smart_chunk_text(
#         text,
#         max_words=max_input_length,
#         overlap=150
#     )

#     chunks = chunk_data["chunks"]
#     total_chunks = chunk_data["total_chunks"]

#     chunk_summaries = []

#     # 2️⃣ Summarize each chunk
#     for chunk in chunks:
#         inputs = tokenizer(
#             chunk["text"],
#             max_length=max_input_length,
#             truncation=True,
#             return_tensors="pt"
#         )

#         with torch.no_grad():
#             summary_ids = model.generate(
#                 inputs["input_ids"].to(device),
#                 max_length=max_output_length,
#                 num_beams=4,
#                 early_stopping=True
#             )

#         summary_text = tokenizer.decode(
#             summary_ids[0],
#             skip_special_tokens=True
#         )

#         chunk_summaries.append({
#             "chunk_id": chunk["chunk_id"],
#             "summary": summary_text
#         })

#     # 3️⃣ Merge summaries
#     final_summary = merge_chunk_summaries(chunk_summaries)

#     processing_time = round(time.time() - start_time, 2)

#     return final_summary, processing_time, total_chunks


import time
import logging
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from backend.chunking import smart_chunk_text, merge_chunk_summaries

# -----------------------------------------
# Logging
# -----------------------------------------
logging.basicConfig(
    filename="model_logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# -----------------------------------------
# Globals
# -----------------------------------------
tokenizer = None
model = None
device = torch.device("cpu")


def load_model():
    global tokenizer, model

    if model is not None:
        return

    logger.info("Loading DistilBART model on CPU...")
    MODEL_NAME = "sshleifer/distilbart-cnn-12-6"

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
    model.to(device)
    model.eval()

    logger.info("Model loaded successfully")


def summarize_text(text, max_input_length=1024, max_output_length=200):
    """
    Returns:
        final_summary (str)
        processing_time (float)
        total_chunks (int)
    """
    try:
        load_model()
        start_time = time.time()

        # 1️⃣ Chunk text
        chunk_data = smart_chunk_text(
            text,
            max_words=max_input_length,
            overlap=150
        )

        chunks = chunk_data["chunks"]
        total_chunks = chunk_data["total_chunks"]

        logger.info(f"Text chunked | total_chunks={total_chunks}")

        chunk_summaries = []

        # 2️⃣ Summarize each chunk
        for chunk in chunks:
            prompt = ("Write a detailed, explanatory summary in multiple paragraphs, "
                "covering key events, background, and outcomes clearly:\n\n"
                + chunk["text"]
            )

            inputs = tokenizer(
                prompt,
                max_length=max_input_length,
                truncation=True,
                padding = "longest",
                return_tensors="pt"
            )

            input_ids = inputs["input_ids"].to(device)
            attention_mask = inputs["attention_mask"].to(device)

            # Dynamic min length (important)
            min_len = max(60, int(0.3 * max_output_length))

            with torch.no_grad():
                summary_ids = model.generate(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    max_new_tokens=max_output_length,
                    min_length=min_len,
                    num_beams=4,
                    length_penalty=1.1,
                    early_stopping=True
                )

            summary = tokenizer.decode(
                summary_ids[0],
                skip_special_tokens=True
            )

            chunk_summaries.append({
                "chunk_id": chunk["chunk_id"],
                "summary": summary
            })

        # 3️⃣ Merge chunk summaries
        final_summary = merge_chunk_summaries(chunk_summaries)

        # 4️⃣ Second-pass summarization (ONLY if really needed)
        if total_chunks > 10 and len(final_summary.split()) > 300:
            logger.info("Running second-pass summarization")

            inputs = tokenizer(
                final_summary,
                max_length=1024,
                truncation=True,
                return_tensors="pt"
            )

            input_ids = inputs["input_ids"].to(device)
            attention_mask = inputs["attention_mask"].to(device)

            with torch.no_grad():
                summary_ids = model.generate(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    max_new_tokens=350,
                    min_length=180,
                    num_beams=4,
                    length_penalty=1.1,
                    early_stopping=True
                )

            final_summary = tokenizer.decode(
                summary_ids[0],
                skip_special_tokens=True
            )

        processing_time = round(time.time() - start_time, 2)

        logger.info(
            f"Summarization done | time={processing_time}s | chunks={total_chunks}"
        )

        return final_summary, processing_time, total_chunks

    except Exception:
        logger.exception("Summarization failed")
        return None, None, 0
