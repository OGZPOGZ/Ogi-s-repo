from random import randint

suits = ['H', 'D', 'C', 'S']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

rank_to_number = {r: i for i, r in enumerate(ranks, 2)}
number_to_rank = {v: k for k, v in rank_to_number.items()}
number_to_rank[1] = 'A'  # Add 1 for Ace as low
suit_to_emoji = {'H': '♥️', 'D': '♦️', 'C': '♣️', 'S': '♠️'}

def deck(broj_kartica=7):
    cards = []
    straight_cards = []
    i = 0
    print_cards = "CARDS:"
    emoji_suits = []

    while i < broj_kartica:
        suit = randint(0, 3)
        rank = randint(0, 12)
        card = [ranks[rank], suits[suit]]
        if card not in cards:
            cards.append(card)
            straight_cards.append(rank_to_number[card[0]])
            i += 1


    straight_cards = [rank_to_number[card[0]] for card in cards]


    for i in range(broj_kartica):
        emoji_suits.append(suit_to_emoji[cards[i][1]])
        print_cards += f" {cards[i][0]}{emoji_suits[i]} ,"

    print(print_cards.strip(" ,"))

    best_hand = "High Card"
    best_score = 1
    best_detail = ""

    # Group cards by suit
    suit_groups = {'H': [], 'D': [], 'C': [], 'S': []}
    for card in cards:
        suit_groups[card[1]].append(rank_to_number[card[0]])

    # ---- ROYAL FLUSH ----
    royal = [10, 11, 12, 13, 14]
    for suit, group in suit_groups.items():
        if all(rank in group for rank in royal):
            best_hand = "Royal Flush"
            best_score = 10
            best_detail = f"in {suit}"
            break

    # ---- STRAIGHT FLUSH ----
    if best_score < 10:
        for suit, group in suit_groups.items():
            if len(group) >= 5:
                group = sorted(set(group))
                if 14 in group:
                    group.append(1)
                group = sorted(set(group))
                for i in range(len(group) - 4):
                    window = group[i:i+5]
                    if window == list(range(window[0], window[0] + 5)):
                        best_hand = "Straight Flush"
                        best_score = 9
                        best_detail = f"{[number_to_rank[n] for n in window]} of {suit}"
                        break

    # ---- FOUR/FULL/THREE/PAIR ----
    ranks_only = [card[0] for card in cards]
    counts = {}
    for rank in ranks_only:
        counts[rank] = counts.get(rank, 0) + 1

    pairs = 0
    has_three = False
    has_four = False

    for count in counts.values():
        if count == 4:
            has_four = True
        elif count == 3:
            has_three = True
        elif count == 2:
            pairs += 1

    if has_four and best_score < 8:
        best_hand = "Four of a Kind"
        best_score = 8
    elif has_three and pairs >= 1 and best_score < 7:
        best_hand = "Full House"
        best_score = 7

    # ---- FLUSH ----
    if best_score < 6:
        for suit, group in suit_groups.items():
            if len(group) >= 5:
                best_hand = "Flush"
                best_score = 6
                break

    # ---- STRAIGHT ----
    if best_score < 5:
        straight_cards = sorted(set(straight_cards))
        if 14 in straight_cards:
            straight_cards.append(1)
        straight_cards = sorted(set(straight_cards))
        for i in range(len(straight_cards) - 4):
            window = straight_cards[i:i+5]
            if window == list(range(window[0], window[0] + 5)):
                best_hand = "Straight"
                best_score = 5
                best_detail = f"{[number_to_rank[n] for n in window]}"
                break

    # ---- THREE/PAIR/TWO PAIR ----
    if has_three and best_score < 4:
        best_hand = "Three of a Kind"
        best_score = 4
    elif pairs >= 2 and best_score < 3:
        best_hand = "Two Pair"
        best_score = 3
    elif pairs == 1 and best_score < 2:
        best_hand = "One Pair"
        best_score = 2

    # ---- HIGH CARD ----
    if best_score == 1:
        high = max(straight_cards)
        best_detail = number_to_rank[high]

    # ---- RESULT ----
    print(f"BEST HAND: {best_hand}", f"({best_detail})" if best_detail else "")

deck()
