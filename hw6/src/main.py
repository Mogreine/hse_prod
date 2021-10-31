import numpy as np

from typing import List
from spylls.hunspell import Dictionary
from functools import partial
from textdistance import hamming, needleman_wunsch, damerau_levenshtein, jaro


class SpellChecker:
    def __init__(self):
        self.dictionary = Dictionary.from_files("en_US")
        self.distances = [
            damerau_levenshtein.normalized_distance,
            jaro.normalized_distance,
            hamming.normalized_distance,
            needleman_wunsch.normalized_distance
        ]

    def _get_candidates(self, word: str, n_candidates: int) -> List[str]:
        return list(self.dictionary.suggest(word))[:n_candidates]

    def _calc_features(self, word: str, candidates: List[str]) -> np.ndarray:
        features = np.array([[dist(word, c) for dist in self.distances] for c in candidates])
        return features

    def _rank_candidates(self, word: str, candidates: List[str]) -> List[str]:
        features = self._calc_features(word, candidates)
        c_idx_sorted = np.mean(features, axis=1).argsort()
        res = [candidates[idx] for idx in c_idx_sorted]

        return res

    def get_suggestions(self, word: str, n_candidates: int = 5) -> List[str]:
        candidates = self._get_candidates(word, n_candidates)
        return self._rank_candidates(word, candidates)

    def fix(self, word: str) -> str:
        if self.dictionary.lookup(word):
            return word
        else:
            return self._get_candidates(word, 1)[0]


def main():
    wrong_word = "sammer"
    checker = SpellChecker()

    candidates = checker.get_suggestions(wrong_word, 5)

    print(f"Word: {wrong_word}")
    print(f"Candidates: ")

    for w in candidates:
        print(f"\t{w}")


if __name__ == "__main__":
    main()
