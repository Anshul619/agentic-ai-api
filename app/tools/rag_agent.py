from openai import OpenAI
from tools.retrieval import retrieve_documents
from tools.evaluation import evaluate_faithfulness
from tools.observability import measure_latency, log_trace

import json
import time

client = OpenAI()