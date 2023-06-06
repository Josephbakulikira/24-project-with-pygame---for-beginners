def PositionIn(pos, moves):
    for move in moves:
        if pos == move:
            return True
    return False