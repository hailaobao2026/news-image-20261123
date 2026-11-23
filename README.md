# news-image-20261123 — The World in One Day

A program that draws Monday 23 November 2026's world news as a one-page
newspaper front page (1024×1024 PNG), using Pillow only. No network, no
photographs, no AI images — every pixel is drawn with code.

Run it:

    python3 main.py            # writes /output/entry.png
    MAKEFUN_OUTPUT_DIR=out python3 main.py

The output is deterministic: two runs produce byte-identical PNGs.

## Stories (each verified against several independent sources)

Main six:
1. **COP31 collapses** — climate talks in Antalya end with no deal; the final
   text never mentions fossil fuels. (CNN, Reuters, Le Monde, The Times)
2. **"El Chapo Isidro" captured** — FBI top-10 fugitive Fausto Isidro Meza
   Flores seized in Sinaloa; 11 killed. (AP, CNN, WSJ, The Times)
3. **Russian ships hit far from home** — Ukrainian sea drones sink the
   corvette Merkury off Libya; the cargo ship Sparta II burns off Finland.
   (WSJ, The Times, The War Zone, AP)
4. **Democrats' record House win** — 258 seats, the biggest majority since
   1992. (AP, Reuters, Fox News)
5. **Factory fire in Indonesia** — at least 3 dead, dozens missing after a
   candy factory burns in Banten, near Jakarta. (AP/AFP, Reuters, PEOPLE)
6. **Killer-robot talks live on** — 128 nations agree to two more years of UN
   talks on lethal autonomous weapons, but no binding treaty. (AOAV, Daily
   Voice of Asia, The Independent Press)

Also today: Nepal's PM Balendra Shah holds talks with Narendra Modi in Delhi;
South Korea's education minister quits over an AI exam-cheating scandal;
Max Verstappen wins a chaotic Las Vegas Grand Prix.
