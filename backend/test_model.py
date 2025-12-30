import os
import sys
from flask import Flask
from flask_cors import CORS



# -------------------------------------------------
# FIX PATH FIRST (CRITICAL)
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


from models.summarization_model import summarize_text

text = """Machine learning enables computers to learn from data. 
It is widely used in AI applications like natural language processing, 
computer vision, and recommendation systems."""

summary, t = summarize_text(text)
print("Summary:", summary)
print("Processing time:", t)
