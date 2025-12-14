# test_manuale.py
from modelli import Risorsa, Progetto
from motore import assegna_risorse

print("--- 🧪 INIZIO TEST ISOLATO ---")

# 1. Creiamo dati finti (Mock Data) direttamente in memoria
# Non serve il database!
mario = Risorsa("Mario", "Developer", 100) # 100 ore totali
luca  = Risorsa("Luca", "Tester", 100)

team = [mario, luca]

# Creiamo un progetto che richiede 20 ore Dev e 80 ore Tester
# Totale 100 ore.
requisiti = {
    'Developer': {'qty': 1, 'perc': 20}, # 20 ore
    'Tester':    {'qty': 1, 'perc': 80}  # 80 ore
}

progetto_test = Progetto(
    nome="Test Unitario",
    priorita=1,
    data_consegna="2025-12-31",
    ore_stimate=100,
    margine_percentuale=0, # Nessun margine per semplificare
    requisiti=requisiti
)

lista_progetti = [progetto_test]

# 2. Lanciamo il motore
# Notare: il motore non sa che questi dati sono finti.
assegna_risorse(lista_progetti, team)

# 3. Verifichiamo i risultati (Asserzioni)
print("\n--- 📊 VERIFICA RISULTATI ---")

# Verifica Mario (Developer)
# Doveva prendere il 20% di 100h = 20h
if mario.ore_impegnate == 20:
    print("✅ TEST MARIO SUPERATO: Ha preso esattamente 20 ore.")
else:
    print(f"❌ ERRORE MARIO: Ha {mario.ore_impegnate} ore invece di 20.")

# Verifica Luca (Tester)
# Doveva prendere l'80% di 100h = 80h
if luca.ore_impegnate == 80:
    print("✅ TEST LUCA SUPERATO: Ha preso esattamente 80 ore.")
else:
    print(f"❌ ERRORE LUCA: Ha {luca.ore_impegnate} ore invece di 80.")

# Verifica Progetto
if progetto_test.fattibile:
    print("✅ TEST PROGETTO SUPERATO: Risulta fattibile.")
else:
    print("❌ ERRORE PROGETTO: Risulta non fattibile.")