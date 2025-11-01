from gridworld import Gridworld, getDiscountGrid
from valueIterationAgents import ValueIterationAgent

def searchQuestion3b():
    """
    Brute-force search for the correct (discount, noise, livingReward)
    that yields the expected policy for question 3b (prudence maximale).
    La logique de bouclage et d'indexation est corrigée pour la grille 5x5.
    """

    mdp = getDiscountGrid() 

    # Define search ranges ÉLARGIES (pas de 0.1)
    # Discounts (Gamma): 0.0, 0.1, ..., 1.0 (11 valeurs)
    discounts = [round(i * 0.1, 1) for i in range(11)]
    # Noises (n): 0.0, 0.1, ..., 1.0 (11 valeurs)
    noises = [round(i * 0.1, 1) for i in range(11)]
    # Living Rewards (R_vie): -1.0, -0.9, ..., 1.0 (21 valeurs)
    living_rewards = [round(i * 0.1, 1) for i in range(-10, 11)]

    # Expected policy pour Q3b (5 lignes, y=4 à y=0)
    # Remarque: La ligne 4 (y=0, index 4) contient la falaise (-10)
    expected_policy = [
        ["E", "E", "S", "_", "_"], # Index 0 (y=4, Top row)
        ["N", "_", "S", "_", "_"], # Index 1 (y=3)
        ["N", "_", "_", "_", "_"], # Index 2 (y=2)
        ["N", "_", "_", "_", "_"], # Index 3 (y=1, Start row)
        ["_", "_", "_", "_", "_"]  # Index 4 (y=0, Cliff row)
    ]

    # Définition des indices des lignes à vérifier (y=4, y=3, y=2, y=1)
    y_match_indices = [0, 1, 2, 3]

    tested = 0
    for noise in noises:
        for discount in discounts:
            for living in living_rewards:
                tested += 1
                print(f"Testing combination #{tested}: discount={discount}, noise={noise}, living={living}")

                mdp.setNoise(noise)
                mdp.setLivingReward(living)

                agent = ValueIterationAgent(mdp, discount, iterations=100)

                # Construire la politique pour toute la grille (y=4 à y=0)
                policy = []
                for y in reversed(range(5)): # Boucle pour les 5 lignes (0 à 4)
                    row = []
                    for x in range(5):
                        state = (x, y)
                        if state in mdp.getStates():
                            action = agent.getAction(state)
                            action_char = action[0].upper() if action is not None and action != "exit" else "_"
                            row.append(action_char)
                        else:
                            row.append("_")
                    policy.append(row)

                # Comparer avec expected
                match = True
                for y_index in y_match_indices:
                    for x in range(5):
                        expected = expected_policy[y_index][x]
                        if expected != "_":
                            if policy[y_index][x] != expected:
                                match = False
                                break
                    if not match:
                        break

                if match:
                    print("\n✅ MATCH FOUND!")
                    print(f"Discount = {discount}, Noise = {noise}, LivingReward = {living}\n")
                    print("Resulting policy (5 lignes, de y=4 à y=0):")
                    for row in policy:
                        print(row)
                    return discount, noise, living

    print("\n❌ No match found in tested ranges.")
    return None


if __name__ == "__main__":
    searchQuestion3b()