import re
import json
import spacy
from spacy import displacy

def filtered_data(data_file, filter):
    with open(data_file) as f:
        for line in f:
            item = json.loads(line)
            if filter(item):
                yield item

def export(data, outfile="filtered.json"):
    with open(outfile, "w") as f:
        f.writelines([json.dumps(x) + "\n" for x in data])

# example filter:
# filter checks the review for exactly one occurrence of " and ", 
# as well as having exactly one "." which is at the end, and having no "?" or "!"
def basic_filter(item):
    review_body = item['review_body']
    pattern = r"^(?=[^\.?!]*\.$)(?=.* and )(?!.* and .* and )"
    return bool(re.match(pattern, review_body) and 20 < len(review_body) < 60)

if __name__ == "__main__":
    data_path = "data/train/dataset_en_train.json"

    data = list(filtered_data(data_path, basic_filter))
    
    print(f"Size of filtered dataset: {len(data)}")
    
    nlp = spacy.load("en_core_web_sm")
    docs = [nlp(x['review_body']) for x in data[0:20]]
    displacy.serve(docs, style="dep", port=5005)
    
    # export(data)
