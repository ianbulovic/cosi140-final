import conllu

def read_annotation_file(filepath):
    '''Read a .conllu file and return a list of sentences, and a list of sets of dependencies.'''

    sentences = []
    annotations = []
    with open(filepath, "r") as data_file:
        for tokenlist in conllu.parse_incr(data_file):
            # assemble sentence from tokens
            sentence = tuple([str(token) for token in tokenlist])
            sentences.append(sentence)
            # assemble the set of dependencies
            dependencies = set([(x['head'], x['deprel'], x['id']) for x in tokenlist if not x['deprel'] == '_'])
            annotations.append(dependencies)

    return sentences, annotations

def has_conflict(a_deps, b_deps):
    '''Calculate the sentence-level agreement between two sets of dependencies.'''
    return not a_deps == b_deps

def print_annotated_sentence(sentence, deps):
    for first, deprel, second in deps:
        if second < first:
            first, second = second, first
        print(" ".join([" " * len(word) for word in sentence[:first-1]]), end="")
        print(" ", end="")
        print("-".join(["-" * len(word) for word in sentence[first-1:second]]), end="")
        print(f" {deprel}")
        
    print(" ".join(sentence))
    print()


def find_conflicts(file_a, file_b):
    a_sen, a_ann = read_annotation_file(file_a)
    b_sen, b_ann = read_annotation_file(file_b)

    if not set(a_sen) == set(b_sen):
        sym_diff = set(a_sen).symmetric_difference(set(b_sen))
        for sen in sym_diff:
            print(" ".join(sen))
        raise ValueError(f"{file_a} and {file_b} do not represent the same data! ({len(sym_diff)} mismatched sentences)")
    
    n_a = len([a for a in a_ann if len(a) > 0])
    print(f"{file_a} has {n_a} completed annotations.")
    n_b = len([b for b in b_ann if len(b) > 0])
    print(f"{file_b} has {n_b} completed annotations.")

    input("Press enter to find conflicts.")

    for i, pair in enumerate(zip(a_ann, b_ann)):
        if has_conflict(*pair):
            print(f"Sentence {i+1}:")
            print_annotated_sentence(a_sen[i], a_ann[i])
            print_annotated_sentence(b_sen[i], b_ann[i])
            input()

if __name__ == "__main__":
    file_a = "annotations/external/ds2-tabitha.txt.conllu"
    file_b = "annotations/external/ds2-alicia.txt.conllu"

    find_conflicts(file_a, file_b)