# Motion design 3D

Per quando il brief chiede: lancio di prodotto, brand film premium, ident, un oggetto o un mondo come protagonista, una simulazione che spiega. Il 3D si usa quando se lo guadagna: un oggetto o un set come ricompensa finale, un prodotto, un meccanismo da mostrare. Se basta il 2D, si fa in 2D.

Fonti delle regole: riferimenti HyperFrames `types/3d.md` e `story.md` (segnati **HF**), i lavori premiati in [reference.csv](reference.csv), e regole di mestiere della libreria (segnate *mestiere*, da confermare nei test).

## 1. L'idea prima del render
I 3D premiati non sono "belli", hanno un'idea fisica:
- **NOMINT, WWF "In Hot Water"** (Grand Prix Animation Ciclope 2025): stop-motion girato tutto con una termocamera; ogni oggetto e personaggio stampato in 3D veniva scaldato al punto giusto. Il mezzo (il calore) è il messaggio (il mare che si scalda).
- **Tendril, Hublot "Arsham Droplet"** (Motion Awards 2025, spot e campagna): l'acqua non si vede mai direttamente, si sente in onde, increspature e riflessi; live action e CG fusi in un unico flusso.
- **ManvsMachine, Nike Air Max**: macchine cinetiche 3D, minimalismo industriale e movimento coreografato, montato stretto sulla musica; ogni film ha la sua palette.
- **Aardman, Nest** (2025): CG che imita la plastilina per rendere calde le pensioni.

Domanda da farsi: quale materiale, fenomeno fisico o meccanismo **è** il messaggio? Se la risposta è "nessuno", il 3D è decorazione.

## 2. Camera
| Regola | Valore | Fonte |
|---|---|---|
| Un oggetto eroe | uno, non una folla | HF |
| Entrare, non girare intorno | volare dentro o attraverso l'oggetto: un tuffo vale dieci orbite | HF |
| Spiegare | spaccati, esplosi e capitoli con una riga di didascalia ciascuno, etichette con numeri veri | HF |
| UI del prodotto | mai inclinata in 3D; si inclinano solo i contenuti generati | HF |
| Una mossa per inquadratura | una sola: carrellata, dolly-in, orbita breve o tilt. Le mosse si cambiano sul taglio | *mestiere* |
| Ottiche | 35-50 mm per i mondi, 85-135 mm per il prodotto (niente deformazione), macro con profondità di campo stretta per i dettagli | *mestiere* |
| Velocità | prodotto lento e pesante (ease lunghe, 2-4 s per mossa); i tagli danno il ritmo, non la camera | *mestiere* |
| Forme del film | un piano sequenza, una catena oggetto-oggetto, uno zoom infinito, un volo dentro un mondo (vedi spot/SCHEDA, "Forme") | HF |

## 3. Luce e materiali
| Regola | Valore | Fonte |
|---|---|---|
| Schema | luce chiave calda, controluce freddo, ambiente scuro con 2-3 strisce morbide | HF |
| Riflessi che scorrono | ruotare l'ambiente, non l'oggetto, così i riflessi attraversano la superficie | HF |
| Ombra | sempre un'ombra di contatto sotto l'oggetto | HF |
| Bloom | solo sui punti più luminosi, altrimenti mangia il dettaglio | HF |
| Metallo lucido | ruvidezza circa 0,45 o più e intensità ambiente circa 0,5, sennò strisce bianche | HF |
| Pixel neri | un NaN diventa un fotogramma nero col bloom: limitare i valori che possono dividere per zero | HF |
| Imperfezioni | graffi, polvere, impronte, bordi smussati: un 3D senza imperfezioni sembra generato | *mestiere* |
| Palette | una per film, legata al brand o al materiale (ManvsMachine: una palette per ogni film Nike) | reference |

## 4. Movimento e simulazioni
- Simulare una volta al caricamento (fisica, particelle) e leggere lo stato al tempo `t`: ogni fotogramma deve essere riproducibile (**HF**).
- Ogni scelta casuale con un seme fisso, mai `Math.random()` (**HF**).
- Peso: gli oggetti pesanti partono lenti e si fermano con un piccolo assestamento; quelli leggeri rimbalzano (*mestiere*).
- Simulazioni (fluidi, stoffa, particelle) solo se raccontano qualcosa: Tendril usa Houdini per un materiale che "è" acqua.
- Montaggio sul beat della musica, mosse che arrivano sul beat forte (**HF** sound.md).

## 5. Come lo facciamo noi
| Strada | Quando | Strumento |
|---|---|---|
| **3D in codice** | oggetti semplici, tipografia 3D, esplosi, mondi geometrici, data viz 3D | Three.js dentro HyperFrames (vedi `runtimes.md` di HyperFrames) |
| **3D generato** | materiali realistici, prodotti, personaggi, liquidi, ambienti | Kling Image per i fotogrammi chiave, Kling Video per il movimento (5-10 s, un'azione per clip), Element per tenere coerente oggetto o personaggio |
| **Ibrido** (il più forte) | quasi sempre | clip Kling come lastre video dentro HyperFrames, con titoli, transizioni, packshot finale e suono costruiti in codice |

Prompt base Kling per 3D prodotto: "hyperreal CGI product film, [oggetto], single hero object, slow dolly-in, warm key light, cool rim light, dark environment with soft light strips, contact shadow, shallow depth of field, macro detail, no text". Negativo: "text, logo, watermark, extra objects, warped geometry, glossy plastic".

## 6. Errori da evitare
- Un vuoto scuro con piccoli oggetti che galleggiano, glow e particelle ovunque (**HF**, vietato di default).
- Orbite infinite attorno al prodotto senza mai entrarci.
- Logo 3D cromato che ruota: il segno arriva una volta sola, alla fine, con peso.
- Tutto lucido e perfetto, nessuna ombra di contatto.
- Una camera che si muove sempre alla stessa velocità per tutto il film.
- 3D senza idea: se si toglie il 3D e il messaggio resta uguale, il 3D era decorazione.

## Collegamenti
- [3D morbido e clay](../../categorie/03-3d-morbido-clay/SCHEDA.md)
- [Mascotte con Kling](../../categorie/mascotte-kling/SCHEDA.md)
- [Spot pubblicitari](../spot/SCHEDA.md)
- [Metodo HyperFrames](../../manuale/metodo-hyperframes.md)
