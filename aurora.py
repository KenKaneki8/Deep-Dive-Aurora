# -*- coding: utf-8 -*-
"""Aurora.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1pGZvPyCqqrNWDvCx2ZP9Ako4IHon6WQe
"""

import threading
import random
import collections
from collections import  Counter
import re

class MemoryNode:
  def __init__(self, data, weight=1):
    self.data = data # The memory content
    self.weight = weight # Importance score
    self.next = None # Pointer to the next memory

class MemoryManager:
  def __init__(self, stm_capacity=5):
    self.stm_capacity = stm_capacity # Limit for short-term memory
    self.stm_head = None # Current STM size
    self.stm_size = 0 # Current STM size
    self.ltm = [] # Long-term memory storage
    self.mutex = threading.Lock() # Mutex for seamless access
    self.adaptive_weights = {} # Adaptive learning storage

  def add_to_memory(self, data, weight=1):
    """Adds a memory to STM, and moves it to LTM if it meets reinforcement criteria"""
    new_node = MemoryNode(data, weight)
    with self.mutex:
      if data in self.adaptive_weights:
        weight += self.adaptive_weights[data] # Adjust weight based on past occurences

      if self.stm_size < self.stm_capacity:
        new_node.next = self.stm_head
        self.stm_head = new_node
        self.stm_size += 1
      else:
        self.reinforce_memory()
        self.stm_head = new_node

  def reinforce_memory(self, weight_threshold=5):  # Adjusted weight threshold to 2 or lower
    """Moves important STM memories to LTM if weight exceeds threshold."""
    with self.mutex:
        current = self.stm_head
        while current:
            # Reinforce memory if it meets the weight threshold
            if current.weight >= weight_threshold:  # You can make this a dynamic value based on usage
                self.ltm.append((current.data, current.weight))
                self.adaptive_weights[current.data] = self.adaptive_weights.get(current.data, 0) + 1
            current = current.next

        self.stm_head = None  # Clear STM
        self.stm_size = 0


  def display_memory(self):
    """Displays STM and LTM contents."""
    with self.mutex:
      print("Short-Term Memort:")
      current = self.stm_head
      while current:
        print(f"Data: {current.data}, Weight: {current.weight}")
        current = current.next

      print("\nLong-Term Memory:")

      for data, weight in self.ltm:
        print(f"Data: {data}, Weight: {weight}")

  def analyze_patterns(self):
    """Detects recurring spike patterns in long-term memory."""
    with self.mutex:
      spike_patterns = [data for data, _ in self.ltm]
      pattern_counts = Counter(spike_patterns)
      print("\nDetected Patterns:")
      for pattern, count in pattern_counts.items():
        if count > 1: #Only show repeating patterns
          print(f"Pattern: {pattern}, Occurences: {count}")

class EEGSimulator:
  def __init__(self, memory_manager, neurons=10):
    self.memory_manager = memory_manager
    self.neurons = neurons

  def generate_spike_activity(self):
    """Simulates EEG-like brain wave spikes."""
    for _ in range(self.neurons):
      activity = random.randint(1,5) # Simulated spike intensity
      self.memory_manager.add_to_memory(f"Neuron Spike {activity}", weight=activity)

class SymbolicBrain:
  def __init__(self):
    self.stm = [] # Short-term memory (STM)
    self.ltm = {} # Long-term memory (LTM), storing reinforced patterns
    self.learned_words = set() #Stores dynamically learned words
    self.lock = threading.Lock() # A Mutex needed for thread safe operations

  def process_input(self, text):
    """Processes input and updates memory."""
    words = text.split()
    for word in words:
      self.stm.append(word)
      if len(self.stm) > 5:
        self.stm.pop(0)
      self.update_memory(word)

  def update_memory(self, word):
        """Updates memory with the word."""
        # Update LTM with the word and increase its count
        if word in self.ltm:
            self.ltm[word] += 1  # Increment the count of occurrences
        else:
            self.ltm[word] = 1  # Start the count at 1 if the word is new
        print(f"Updated LTM: {self.ltm}")  # Debug print
        if self.ltm[word] >= 3:  # If a word has been seen 3 or more times, consider it learned
            self.check_learned_words(word)

  def decay_memory(self, decay_rate=0.1):
    """Decay the memory values to simulate forgetting."""
    for word in list(self.ltm.keys()):
        if word not in self.learned_words:  # Skip words that are learned
            self.ltm[word] = max(0, self.ltm[word] - decay_rate)
        if self.ltm[word] == 0:
            del self.ltm[word]  # Remove unneeded words





  def check_learned_words(self, word, reinforcement_threshold=3):
    """Reinforce words based on their frequency."""
    if word not in self.learned_words and self.ltm.get(word, 0) >= reinforcement_threshold:
        print(f"Learning word: {word} (Reinforced {self.ltm.get(word, 0)} times)")  # Debug line
        self.learned_words.add(word)


  def recall_words(self):
    with self.lock:
      return ' '.join(self.learned_words) if self.learned_words else "No full words recalled."

  def get_memory_state(self):
    return {
        "STM (recent letters)": self.stm,
        "LTM (reinforced patterns)": self.ltm,
        "Learned Words": list(self.learned_words)
    }

# Example usage:
brain = SymbolicBrain()
inputs = "a a a b b b c c c d d d e e e f f f g g g h h h i i i j j j k k k l l l m m m n n n o o o p p p q q q r r r s s s t t t u u u v v v w w w x x x y y y z z z"


for word in inputs.split(): # Process input as words instead of characters
    brain.process_input(word)

# Decay memory after learning
brain.decay_memory()

print("Recalled Word:", brain.recall_words())
print("Memory State:", brain.get_memory_state())