import numpy as np

from typing import List
from tqdm import tqdm
from src.spellcheck import SpellChecker


def read_data(n_words: int = None):
    examples = []
    correction = []
    with open("../data/spell_check_test.txt", "r") as f:
        for line in f:
            word_inc, word_cor = line.lower().strip().split("\t")
            examples.append(word_inc)
            correction.append(word_cor)

    return examples[:n_words], correction[:n_words]


def acc_at_k(preds: List[List[str]], target: List[str], k: int) -> float:
    for pred in preds:
        if len(pred) != k:
            pred.extend([""] * (k - len(pred)))

    msk = np.array(target).reshape(-1, 1) == np.array(preds)
    preds_in_range = np.sum(np.count_nonzero(msk, axis=1))

    return preds_in_range / len(target)


def main():
    words_inc, words_cor = read_data()
    checker = SpellChecker()
    n_suggestions = 10

    preds = []
    for w in tqdm(words_inc, desc="Predicting"):
        preds.append(checker.get_suggestions(w, n_suggestions))

    print(f"Acc@{n_suggestions}: {acc_at_k(preds, words_cor, n_suggestions): .3f}")


if __name__ == "__main__":
    main()
