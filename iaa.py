import conllu

def read_annotation_file(filepath):
    '''Read a .conllu file and return a list of sentences, and a list of sets of dependencies.'''

    sentences = []
    annotations = []
    with open(filepath, "r") as data_file:
        for tokenlist in conllu.parse_incr(data_file):
            # assemble sentence from tokens
            sentence = ' '.join(str(token) for token in tokenlist)
            sentences.append(sentence)
            # assemble the set of dependencies
            dependencies = set([(x['head'], x['deprel'], x['id']) for x in tokenlist if not x['deprel'] == '_'])
            annotations.append(dependencies)

    return sentences, annotations

def sentence_level_agreement(a_deps, b_deps):
    '''Calculate the sentence-level agreement between two sets of dependencies.'''

    # count the number of agreed dependency relations between the two annotators
    agreed = len(a_deps.intersection(b_deps))
    # divide by the total number of unique dependency relations
    return agreed / len(a_deps.union(b_deps))

def total_agreement(file_a, file_b):
    '''Calculate the total agreement between two .conllu files representing the same data.'''

    a_sentences, a_annotations = read_annotation_file(file_a)
    b_sentences, b_annotations = read_annotation_file(file_b)

    if not set(a_sentences) == set(b_sentences):
        raise ValueError(f"{file_a} and {file_b} do not represent the same data!")

    n = len([(a, b) for a, b in zip(a_annotations, b_annotations) if len(a) > 0 and len(b) > 0])
    # average agreement over all sentences
    agreement = sum([sentence_level_agreement(a_annotations[i], b_annotations[i]) for i in range(n)]) / n
    return agreement

if __name__ == "__main__":
    file_a = "annotations/external/ds1-huiyu.txt.conllu"
    file_b = "annotations/external/ds1-kimmy.txt.conllu"

    agreement = total_agreement(file_a, file_b)

    print(agreement)