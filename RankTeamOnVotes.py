def rankTeams(votes):
    if not votes:
        return ""

    num_positions = len(votes[0])
    teams = list(votes[0])
    rank_count = {}

    for team in teams:
        rank_count[team] = [0] * num_positions

    for vote in votes:
        for i, team in enumerate(vote):
            rank_count[team][i] += 1

    # returns a tuple of rank in negatives so it would come at top, and if it is same next order alphabetically as in team
    def sort_key(tm):
        return [-c for c in rank_count[tm]], tm

    teams.sort(key=sort_key)

    return ''.join(teams)


votes = ["ABC","ACB","ABC","ACB","ACB"]
print(rankTeams(votes))

import unittest


class TestRankTeams(unittest.TestCase):

    def test_example1(self):
        votes = ["ABC", "ACB", "ABC", "ACB", "ACB"]
        self.assertEqual(rankTeams(votes), "ACB")

    def test_example2(self):
        votes = ["AXYZ", "XYZA"]
        self.assertEqual(rankTeams(votes), "XAYZ")

    def test_single_vote(self):
        votes = ["WXYZ"]
        self.assertEqual(rankTeams(votes), "WXYZ")

    def test_tiebreak_by_second_place(self):
        votes = ["AB", "BA"]
        self.assertEqual(rankTeams(votes), "AB")

    def test_tiebreak_alphabetical(self):
        votes = ["ABC", "BAC", "CAB"]
        self.assertEqual(rankTeams(votes), "ABC")

    def test_empty_votes(self):
        votes = []
        self.assertEqual(rankTeams(votes), "")

    def test_same_team_all_positions(self):
        votes = ["A", "A", "A"]
        self.assertEqual(rankTeams(votes), "A")

if __name__ == '__main__':
    unittest.main()