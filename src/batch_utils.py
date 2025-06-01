# batch_utils.py

def classify_batch(sentences, model):
    results = []
    for sent in sentences:
        try:
            output = model(sent)
            top = output[0]
            results.append({"sentence": sent, "emotion": top["label"].lower(), "score": top["score"]})
        except Exception:
            results.append({"sentence": sent, "emotion": "error", "score": 0.0})
    return results

# this must be top-level to work with multiprocessing
def batch_worker(chunk_and_model):
    chunk, model = chunk_and_model
    return classify_batch(chunk, model)