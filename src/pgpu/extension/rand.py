import random, pygame
from .pmath import inside_range


def rand_sign() -> int:
    return random.choice([1, -1])


def rand_offset(max_value: int) -> int:
    return random.randint(-int(max_value), int(max_value))


def rand_offset_vec(max_value: int) -> pygame.Vector2:
    return pygame.Vector2(
        random.randint(-int(max_value), int(max_value)),
        random.randint(-int(max_value), int(max_value)),
    )


def weighted_choice(sequence, weights):
    weightssum = sum(weights)
    chosen = random.randint(0, weightssum)
    cweight = 0
    i = 0
    for w in weights:
        if inside_range(chosen, cweight, cweight + w):
            return sequence[i]
        cweight += w
        i += 1


def weighted_choice_combined(sequence_and_weights):
    sequence = [s_a_w[0] for s_a_w in sequence_and_weights]
    weights = [saw[1] for saw in sequence_and_weights]
    weightssum = sum(weights)
    chosen = random.randint(0, weightssum)
    cweight = 0
    i = 0
    for w in weights:
        if inside_range(chosen, cweight, cweight + w):
            return sequence[i]
        cweight += w
        i += 1
