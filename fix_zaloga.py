with open("tools/zaloga.py", "r") as f:
    content = f.read()

prefix = content.split("print(\"kto ja zrobil (luke wskazal Zenek 30.07: 'straznikiem objeci tylko wywolani wykonawcy').\")")[0]

new_suffix = """print("kto ja zrobil (luke wskazal Zenek 30.07: 'straznikiem objeci tylko wywolani wykonawcy').")

    # Hans kontroluje narade dopiero po zapisaniu wszystkich glosow. Jego awaria nie moze
    # zmienic kodu wyjscia narady ani zniszczyc odebranych wynikow.
    try:
        sys.path.insert(0, os.path.join(REPO, "tools"))
        import hans
        sys.path.pop(0)

        print("\\n" + "=" * 25 + " HANS (KONTROLA NARADY) " + "=" * 25)
        meldunek_path = os.path.join(REPO, ".scratch", "_meldunek_ostatni.txt")
        raport = hans.sprawdz_narade(a.katalog, meldunek_path)
        print(json.dumps(raport, ensure_ascii=False, indent=2))
        print("=" * 74)
    except Exception as e:
        print("\\n" + "=" * 25 + " HANS (AWARIA KONTROLI) " + "=" * 25)
        print(f"Hans nie zakonczyl kontroli: {type(e).__name__}: {e}")
        print("=" * 74)

    return 0

if __name__ == "__main__":
    sys.exit(main())
"""

with open("tools/zaloga.py", "w") as f:
    f.write(prefix + new_suffix)
