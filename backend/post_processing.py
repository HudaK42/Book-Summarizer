import re

# -----------------------------------------
# 1. Split text into sentences
# -----------------------------------------
def split_sentences(text):
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.strip() for s in sentences if s.strip()]


# -----------------------------------------
# 2. Remove duplicate sentences
# -----------------------------------------
def remove_duplicates(sentences):
    seen = set()
    result = []

    for s in sentences:
        key = s.lower()
        if key not in seen:
            seen.add(key)
            result.append(s)

    return result


# -----------------------------------------
# 3. Reorder sentences (simple heuristic)
# -----------------------------------------
def reorder_sentences(sentences):
    intro = []
    body = []
    conclusion = []

    for s in sentences:
        s_lower = s.lower()
        if any(word in s_lower for word in ["in conclusion", "overall", "thus", "finally"]):
            conclusion.append(s)
        elif len(s.split()) < 12:
            intro.append(s)
        else:
            body.append(s)

    return intro + body + conclusion


# -----------------------------------------
# 4. Enforce length constraint
# -----------------------------------------
def enforce_length(sentences, max_words=180):
    result = []
    word_count = 0

    for s in sentences:
        words = s.split()
        if word_count + len(words) <= max_words:
            result.append(s)
            word_count += len(words)
        else:
            break

    return result


# -----------------------------------------
# 5. Formatting improvements
# -----------------------------------------
def format_text(sentences):
    formatted = []
    for s in sentences:
        s = s.strip()
        s = s[0].upper() + s[1:] if s else s
        if not s.endswith(('.', '!', '?')):
            s += '.'
        formatted.append(s)

    return "\n\n".join(formatted)


# -----------------------------------------
# 6. Complete post-processing pipeline
# -----------------------------------------
def refine_summary(text, max_words=180):
    sentences = split_sentences(text)
    sentences = remove_duplicates(sentences)
    sentences = reorder_sentences(sentences)
    sentences = enforce_length(sentences, max_words)
    return format_text(sentences)
