import tkinter as tk
from typing import List, Tuple, Dict
from queue import PriorityQueue
from data_structures import PrioritizedItem
from word_utils import (
    get_feedback, get_letter_frequencies, filter_words,
    calculate_heuristic, calculate_g_cost
)

def best_first_search(words: List[str], secret: str) -> Tuple[List[str], int]:
    letter_freq = get_letter_frequencies(words)
    pq = PriorityQueue()
    possible_words = words.copy()
    guesses = []
    for word in possible_words:
        pq.put((calculate_heuristic(word, letter_freq), word))
    while not pq.empty() and len(guesses) < 6:
        _, guess = pq.get()
        guesses.append(guess)
        feedback = get_feedback(secret, guess)
        if feedback == 'ggggg':
            return guesses, len(guesses)
        possible_words = filter_words(possible_words, guess, feedback)
        while not pq.empty():
            pq.get()
        for word in possible_words:
            pq.put((calculate_heuristic(word, letter_freq), word))
    return guesses, len(guesses)

def astar_search(words: List[str], secret: str) -> Tuple[List[str], int]:
    letter_freq = get_letter_frequencies(words)
    pq = PriorityQueue()
    possible_words = words.copy()
    guesses = []
    for word in possible_words:
        h_cost = calculate_heuristic(word, letter_freq)
        g_cost = 0
        f_cost = g_cost - h_cost
        pq.put(PrioritizedItem(f_cost, g_cost, word))
    while not pq.empty() and len(guesses) < 6:
        current = pq.get()
        guesses.append(current.word)
        feedback = get_feedback(secret, current.word)
        if feedback == 'ggggg':
            return guesses, len(guesses)
        possible_words = filter_words(possible_words, current.word, feedback)
        while not pq.empty():
            pq.get()
        g_cost = calculate_g_cost(guesses)
        for word in possible_words:
            h_cost = calculate_heuristic(word, letter_freq)
            f_cost = g_cost - h_cost
            pq.put(PrioritizedItem(f_cost, g_cost, word))
    return guesses, len(guesses)

def dfs_search(words: List[str], secret: str) -> Tuple[List[str], int]:
    possible_words = words.copy()
    guesses = []
    def dfs_recursive(words: List[str], depth: int) -> bool:
        if depth >= 6:
            return False
        for word in words:
            guesses.append(word)
            feedback = get_feedback(secret, word)
            if feedback == 'ggggg':
                return True
            remaining = filter_words(words, word, feedback)
            if remaining and dfs_recursive(remaining, depth + 1):
                return True
            guesses.pop()
        return False
    dfs_recursive(possible_words, 0)
    return guesses, len(guesses)

def aostar_search(words: List[str], secret: str) -> Tuple[List[str], int]:
    letter_freq = get_letter_frequencies(words)
    possible_words = words.copy()
    guesses = []
    costs: Dict[str, float] = {}
    solved: Dict[str, bool] = {}
    def get_cost(word: str) -> float:
        if word not in costs:
            costs[word] = calculate_heuristic(word, letter_freq)
        return costs[word]
    while possible_words and len(guesses) < 6:
        current = min(possible_words, key=get_cost)
        guesses.append(current)
        feedback = get_feedback(secret, current)
        if feedback == 'ggggg':
            solved[current] = True
            return guesses, len(guesses)
        possible_words = filter_words(possible_words, current, feedback)
        solved[current] = False
        for word in possible_words:
            costs[word] = calculate_heuristic(word, letter_freq) + len(guesses)
    return guesses, len(guesses)