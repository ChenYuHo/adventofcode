#!/usr/bin/env python
from os.path import join, dirname
from collections import Counter


print("--- Advent of Code 2023 day 7 ---")

"""
--- Day 7: Camel Cards ---
Your all-expenses-paid trip turns out to be a one-way, five-minute ride in an airship. (At least it's a cool airship!) It drops you off at the edge of a vast desert and descends back to Island Island.

"Did you bring the parts?"

You turn around to see an Elf completely covered in white clothing, wearing goggles, and riding a large camel.

"Did you bring the parts?" she asks again, louder this time. You aren't sure what parts she's looking for; you're here to figure out why the sand stopped.

"The parts! For the sand, yes! Come with me; I will show you." She beckons you onto the camel.

After riding a bit across the sands of Desert Island, you can see what look like very large rocks covering half of the horizon. The Elf explains that the rocks are all along the part of Desert Island that is directly above Island Island, making it hard to even get there. Normally, they use big machines to move the rocks and filter the sand, but the machines have broken down because Desert Island recently stopped receiving the parts they need to fix the machines.

You've already assumed it'll be your job to figure out why the parts stopped when she asks if you can help. You agree automatically.

Because the journey will take a few days, she offers to teach you the game of Camel Cards. Camel Cards is sort of similar to poker except it's designed to be easier to play while riding a camel.

In Camel Cards, you get a list of hands, and your goal is to order them based on the strength of each hand. A hand consists of five cards labeled one of A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2. The relative strength of each card follows this order, where A is the highest and 2 is the lowest.

Every hand is exactly one type. From strongest to weakest, they are:

Five of a kind, where all five cards have the same label: AAAAA
Four of a kind, where four cards have the same label and one card has a different label: AA8AA
Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
High card, where all cards' labels are distinct: 23456
Hands are primarily ordered based on type; for example, every full house is stronger than any three of a kind.

If two hands have the same type, a second ordering rule takes effect. Start by comparing the first card in each hand. If these cards are different, the hand with the stronger first card is considered stronger. If the first card in each hand have the same label, however, then move on to considering the second card in each hand. If they differ, the hand with the higher second card wins; otherwise, continue with the third card in each hand, then the fourth, then the fifth.

So, 33332 and 2AAAA are both four of a kind hands, but 33332 is stronger because its first card is stronger. Similarly, 77888 and 77788 are both a full house, but 77888 is stronger because its third card is stronger (and both hands have the same first and second card).

To play Camel Cards, you are given a list of hands and their corresponding bid (your puzzle input). For example:

32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
This example shows five hands; each hand is followed by its bid amount. Each hand wins an amount equal to its bid multiplied by its rank, where the weakest hand gets rank 1, the second-weakest hand gets rank 2, and so on up to the strongest hand. Because there are five hands in this example, the strongest hand will have rank 5 and its bid will be multiplied by 5.

So, the first step is to put the hands in order of strength:

32T3K is the only one pair and the other hands are all a stronger type, so it gets rank 1.
KK677 and KTJJT are both two pair. Their first cards both have the same label, but the second card of KK677 is stronger (K vs T), so KTJJT gets rank 2 and KK677 gets rank 3.
T55J5 and QQQJA are both three of a kind. QQQJA has a stronger first card, so it gets rank 5 and T55J5 gets rank 4.
Now, you can determine the total winnings of this set of hands by adding up the result of multiplying each hand's bid with its rank (765 * 1 + 220 * 2 + 28 * 3 + 684 * 4 + 483 * 5). So the total winnings in this example are 6440.

Find the rank of every hand in your set. What are the total winnings?
"""


def adventofcode_day7_1(file):
    with open(file) as f:
        hand_to_bid = {fields[0]: fields[1] for line in f if (fields := line.split())}

    hand_types = [[] for _ in range(7)]
    # classify hands to the seven types from weakest to strongest
    for hand in hand_to_bid.keys():
        most_commons = Counter(hand).most_common(2)
        most_common = most_commons[0]
        if len(most_commons) > 1:
            second_most_common = most_commons[1]
        if most_common[1] == 5:
            # Five of a kind
            hand_types[6].append(hand)
        elif most_common[1] == 4:
            # Four of a kind
            hand_types[5].append(hand)
        elif most_common[1] == 3 and second_most_common[1] == 2:
            # Full house
            hand_types[4].append(hand)
        elif most_common[1] == 3 and second_most_common[1] != 2:
            # Three of a kind
            hand_types[3].append(hand)
        elif most_common[1] == 2 and second_most_common[1] == 2:
            # Two pair
            hand_types[2].append(hand)
        elif most_common[1] == 2 and second_most_common[1] != 2:
            # One pair
            hand_types[1].append(hand)
        else:
            # High card
            hand_types[0].append(hand)

    # for easier ordering of cards in later "sort"
    mapping = {
        "1": "01",
        "2": "02",
        "3": "03",
        "4": "04",
        "5": "05",
        "6": "06",
        "7": "07",
        "8": "08",
        "9": "09",
        "T": "10",
        "J": "11",
        "Q": "12",
        "K": "13",
        "A": "14",
    }

    current_rank = 1
    ans = 0
    # from weakest to strongest hand type
    for hands in hand_types:
        hands.sort(key=lambda hand: "".join(mapping[char] for char in hand))
        # from lowest to highest rank
        for rank, hand in enumerate(hands, start=current_rank):
            ans += int(hand_to_bid[hand]) * rank
        current_rank += len(hands)

    return ans


print(adventofcode_day7_1(join(dirname(__file__), "day07_input.txt")))

"""
--- Part Two ---
To make things a little more interesting, the Elf introduces one additional rule. Now, J cards are jokers - wildcards that can act like whatever card would make the hand the strongest type possible.

To balance this, J cards are now the weakest individual cards, weaker even than 2. The other cards stay in the same order: A, K, Q, T, 9, 8, 7, 6, 5, 4, 3, 2, J.

J cards can pretend to be whatever card is best for the purpose of determining hand type; for example, QJJQ2 is now considered four of a kind. However, for the purpose of breaking ties between two hands of the same type, J is always treated as J, not the card it's pretending to be: JKKK2 is weaker than QQQQ2 because J is weaker than Q.

Now, the above example goes very differently:

32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
32T3K is still the only one pair; it doesn't contain any jokers, so its strength doesn't increase.
KK677 is now the only two pair, making it the second-weakest hand.
T55J5, KTJJT, and QQQJA are now all four of a kind! T55J5 gets rank 3, QQQJA gets rank 4, and KTJJT gets rank 5.
With the new joker rule, the total winnings in this example are 5905.

Using the new joker rule, find the rank of every hand in your set. What are the new total winnings?
"""


def adventofcode_day7_2(file):
    with open(file) as f:
        hand_to_bid = {fields[0]: fields[1] for line in f if (fields := line.split())}

    hand_types = [[] for _ in range(7)]
    # classify hands to the seven types from weakest to strongest
    for hand in hand_to_bid.keys():
        counter = Counter(hand)
        most_commons = counter.most_common(2)
        most_common = most_commons[0]
        second_most_common = most_commons[1] if len(most_commons) > 1 else None
        num_Js = counter["J"]
        J_in_hand = num_Js > 0
        if most_common[1] >= 4 and J_in_hand:
            # transform existing "J"s and make Five of a kind
            hand_types[6].append(hand)
        elif most_common[1] == 4:  # 4 1
            # Four of a kind
            hand_types[5].append(hand)
        elif most_common[1] == 3:
            base_type = 3  # at worst "Three of a kind" type
            if second_most_common[1] == 2:  # 3 2
                base_type += 1  # now at worst "Full house" type
            if J_in_hand:
                # for "Three of a kind" (3), having J makes it "Four of a kind" (5)
                # for "Full house" (4), having J makes it "Five of a kind" (6)
                base_type += 2
            hand_types[base_type].append(hand)
        elif most_common[1] == 2:
            base_type = 1  # at worst "One pair" type
            if second_most_common[1] == 2:  # 2 2 1
                base_type += 1  # now at worst "Two pair" type
                # for "Two pair" (2), having one J makes it "Full house" (4), having 2 Js makes it "Four of a kind" (5)
                if num_Js == 2:
                    base_type += 3
                elif num_Js == 1:
                    base_type += 2
            elif J_in_hand:
                # for "One pair" (1), having J (either 1 or 2) makes it "Three of a kind" (3)
                base_type += 2
            hand_types[base_type].append(hand)
        else:
            if J_in_hand:
                # transform all "J"s and make One pair
                hand_types[1].append(hand)
            else:
                # High card
                hand_types[0].append(hand)

    mapping = {
        "1": "01",
        "2": "02",
        "3": "03",
        "4": "04",
        "5": "05",
        "6": "06",
        "7": "07",
        "8": "08",
        "9": "09",
        "T": "10",
        "J": "00",
        "Q": "12",
        "K": "13",
        "A": "14",
    }

    current_rank = 1
    ans = 0
    # from weakest to strongest hand type
    for hands in hand_types:
        hands.sort(key=lambda hand: "".join(mapping[char] for char in hand))
        # from lowest to highest rank
        for rank, hand in enumerate(hands, start=current_rank):
            ans += int(hand_to_bid[hand]) * rank
        current_rank += len(hands)

    return ans


print(adventofcode_day7_2(join(dirname(__file__), "day07_input.txt")))
