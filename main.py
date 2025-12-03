from modelli import Risorsa, Progetto
from motore import assegna_risorse

def main():
    print("==================================================")
    print("      SIMULATORE DI PIANIFICAZIONE PROGETTI       ")
    print("==================================================\n")

    # --- 1. CREAZIONE DELLE RISORSE (Il Team) ---
    # Abbiamo 2 Sviluppatori e 1 Tester
    alice = Risorsa("Alice Senior", "Developer", 100) 
    bob   = Risorsa("Bob Junior",   "Developer", 100) 
    carla = Risorsa("Carla Test",   "Tester",    120) 
    
    # Mettiamoli in una lista
    team = [alice, bob, carla]

    # --- 2. CREAZIONE DEI PROGETTI (Lo Scenario) ---
    
    lista_progetti = []

    # SCENARIO A: La "Landing Page" scade prestissimo (10 Dic), 
    # ma il "Refactoring" è vitale (Priorità 1).
    # Il sistema DEVE fare prima il Refactoring anche se scade a fine anno.
    
    p1 = Progetto(
        nome="Refactoring Core",
        priorita=1,             
        data_consegna="2025-12-31", 
        ore_stimate=50, 
        margine_percentuale=10, 
        skill_richiesta="Developer",
        max_risorse=1
    )
    lista_progetti.append(p1)

    p2 = Progetto(
        nome="Landing Page",
        priorita=1,             
        data_consegna="2025-12-10", 
        ore_stimate=40, 
        margine_percentuale=0, 
        skill_richiesta="Developer",
        max_risorse=1
    )
    lista_progetti.append(p2)

    # SCENARIO B: Il "Progetto Rischioso".
    # Richiede 80 ore. Bob ha 100 ore totali.
    # Matematicamente ci starebbe (100 > 80).
    # MA c'è un margine del 30%. Buffer richiesto = 80 + 30% = 104 ore.
    # Bob ha solo 100 ore. Il sistema DEVE scartare Bob e darlo ad Alice (se libera).
    
    p3 = Progetto(
        nome="Progetto Rischioso",
        priorita=1,
        data_consegna="2026-01-15",
        ore_stimate=80, 
        margine_percentuale=15, # Margine alto!
        skill_richiesta="Tester",
        max_risorse=1
    )
    lista_progetti.append(p3)

    # --- 3. ESECUZIONE DEL MOTORE ---
    assegna_risorse(lista_progetti, team)

    # --- 4. REPORT FINALE ---
    print("\n==================================================")
    print("               REPORT FINALE                      ")
    print("==================================================")
    
    print("\n--- STATO PROGETTI ---")
    for p in lista_progetti:
        stato = "✅ APPROVATO" if p.fattibile else "⛔ NON FATTIBILE"
        risorse_usate = ", ".join([r.nome for r in p.risorse_assegnate])
        print(f"{stato} -> {p.nome} (Assegnato a: {risorse_usate if risorse_usate else 'Nessuno'})")

    print("\n--- STATO RISORSE ---")
    for r in team:
        print(f"{r.nome}: {r.ore_impegnate}h impegnate / {r.ore_totali_disponibili}h totali (Residuo: {r.ore_residue}h)")

if __name__ == "__main__":
    main()