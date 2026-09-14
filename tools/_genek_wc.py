import subprocess
import os

print("--- START ---")
# Krok 1
cmd1 = [
    "python3", "tools/gemini_edytuj.py",
    "--wejscie", "data/remont_wc/kadry/k3.jpg",
    "--prompt", "Usuń zieloną płytę gipsowo-kartonową i zakryj ten obszar popielatymi płytkami, jako przedłużenie tych z dołu. Ściana nad płytkami idealnie biała, gładka w licu. Na górze biały sufit podwieszany. Nie dodawaj miski, nie ruszaj drzwi.",
    "--wyjscie", "data/remont_wc/k3_test_krok1.png",
    "--zaplac"
]
subprocess.run(cmd1, check=True)

# Krok 2
cmd2 = [
    "python3", "tools/gemini_edytuj.py",
    "--wejscie", "data/remont_wc/k3_test_krok1.png",
    "--prompt", "Dodaj białą wiszącą miskę WC Geberit na szarych płytkach, tuż pod czarnym przyciskiem. Drzwi, podłoga i przycisk bez zmian. Nie dodawaj nowej ściany.",
    "--wyjscie", "data/remont_wc/k3_test_krok2.png",
    "--zaplac"
]
subprocess.run(cmd2, check=True)
print("--- END ---")
