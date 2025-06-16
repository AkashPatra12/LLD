## ✅ Time and Space Complexity of rankTeams
Let:

* n = number of votes

* m = number of teams (i.e., length of a vote string)

### ⏱ Time Complexity:
* Initialization – O(m)
  * Create rank_count for all m teams, each with m zeros.

* Counting Votes – O(n * m)
  For each of the n votes and each of the m characters, increment position count.

* Sorting Teams:

  * Sorting m teams.

  * Comparison of two teams takes O(m) time (since we compare all m positions).

### Total sorting cost:
### 👉 O(m^2 log m)