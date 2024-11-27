def calcular_dificuldade(tempo_total):
    if tempo_total <= 30:
        return "Fácil"
    elif tempo_total <= 60:
        return "Média"
    return "Difícil"
