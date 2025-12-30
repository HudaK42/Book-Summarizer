import re

def smart_chunk_text(text, max_words=1000, overlap=150):
    """
    Smart chunking with paragraph + sentence awareness
    and overlapping context preservation.
    """

    text = re.sub(r"\n{2,}", "\n\n", text).strip()
    paragraphs = text.split("\n\n")

    chunks = []
    current_chunk = []
    current_length = 0
    chunk_id = 1

    for para in paragraphs:
        words = para.split()
        para_length = len(words)

        # If paragraph too large → sentence split
        if para_length > max_words:
            sentences = re.split(r'(?<=[.!?])\s+', para)
            for sent in sentences:
                sent_words = sent.split()

                if len(sent_words) > max_words:
                    sent_words = sent_words[:max_words]

                if current_length + len(sent_words) > max_words:
                    chunks.append({
                        "chunk_id": chunk_id,
                        "text": " ".join(current_chunk)
                    })
                    chunk_id += 1

                    # Overlap
                    current_chunk = current_chunk[-overlap:]
                    current_length = len(current_chunk)

                current_chunk.extend(sent_words)
                current_length += len(sent_words)

        else:
            if current_length + para_length > max_words:
                chunks.append({
                    "chunk_id": chunk_id,
                    "text": " ".join(current_chunk)
                })
                chunk_id += 1

                current_chunk = current_chunk[-overlap:]
                current_length = len(current_chunk)

            current_chunk.extend(words)
            current_length += para_length

    if current_chunk:
        chunks.append({
            "chunk_id": chunk_id,
            "text": " ".join(current_chunk)
        })

    return {
        "total_chunks": len(chunks),
        "chunks": chunks
    }


def merge_chunk_summaries(chunk_summaries):
    """
    Merge summaries in chunk_id order
    and avoid redundancy.
    """

    # sort explicitly by chunk_id
    chunk_summaries = sorted(
        chunk_summaries,
        key=lambda x: x["chunk_id"]
    )

    merged = []

    for item in chunk_summaries:
        summary = item["summary"].strip()

        if not merged:
            merged.append(summary)
            continue

        prev_words = set(merged[-1].split()[:50])
        curr_words = set(summary.split()[:50])

        if len(prev_words & curr_words) < 20:
            merged.append(summary)

    return "\n\n".join(merged)
