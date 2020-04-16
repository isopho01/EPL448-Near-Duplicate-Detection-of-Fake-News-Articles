from snapy import MinHash, LSH
from main import readJsonData, preprocessing
from pprint import pprint as pp

SEED = 3


def find_near_duplicate(query, targets, labels, min_jaccard_value, no_of_bands, n_permutations, n_gram, n_gram_type='char'):
    """Using LSH object finds the near duplicate strings.

    Args:
        query_sentences (dict): Dict with query strings and version of string in lower case and without comma.
        sentences (dict): Dict with target strings and version of string in lower case and without comma.
        min_jaccard_value (float): Minimum value for the Jaccard Distance.
        no_of_bands (int): Number of bands to break minhash signature into before hashing into buckets.
        n_permutations (int): Number of permutations used to create minhash signatures used in LSH model.
        n_gram (int): Size of each overlapping text shingle to break text into prior to hashing.
    """
    # Create MinHash object.
    minhash = MinHash(targets, n_gram=n_gram, n_gram_type=n_gram_type,
                      permutations=n_permutations, hash_bits=64, seed=SEED)

    # Create LSH model.
    lsh = LSH(minhash, labels, no_of_bands=no_of_bands)

    # Query to find near duplicates the string in `search`
    closest_results = lsh.query(labels[0], min_jaccard=min_jaccard_value)

    print("QUERY: {}".format(labels[0]))
    pp(closest_results)


def main():
    # Get data
    data = readJsonData('./dataset/politifact_results.json')

    # Set settings
    min_jaccard_value = float(0.5)
    n_gram = int(30)
    n_gram_type = 'term'
    n_permutations = int(100)
    no_of_bands = int(50)

    # Set query and targets
    query = ' '.join(preprocessing(data['original_article.content'][0]))
    targets = [query]
    labels = [data['original_article.url'][0]]
    for v in data['extracted_articles'][0]:
        # Content must be more than n_grams length
        if not v or not v['content'] or not v['title'] or not v['url']:
            continue

        # Preprocessing
        preprocessed_content = preprocessing(v['content'])
        string_preprocessed_content = ' '.join(preprocessed_content)

        # Content must be more than n_grams length
        if n_gram_type == 'char' and len(string_preprocessed_content) < n_gram:
            continue
        if n_gram_type == 'term' and len(preprocessed_content) < n_gram:
            continue

        targets.append(string_preprocessed_content)
        labels.append(v['url'])

    # find near duplicate sequences to `search_string`
    find_near_duplicate(query, targets, labels,
                        min_jaccard_value, no_of_bands, n_permutations, n_gram, n_gram_type)


if __name__ == "__main__":
    main()
