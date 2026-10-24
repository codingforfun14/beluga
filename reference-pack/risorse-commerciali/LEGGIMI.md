# Risorse per uso commerciale

Materiale gratuito che si può usare negli spot dei clienti. Per ogni fonte: cosa c'è, licenza, se serve il credito. Licenze lette sulle pagine ufficiali il 2026-10-24; prima di consegnare un lavoro ricontrollare la pagina del singolo file.

## Modelli 3D di prodotto

| Fonte | Cosa | Licenza | Credito |
|---|---|---|---|
| [Khronos glTF Sample Assets](https://github.com/KhronosGroup/glTF-Sample-Assets/tree/main/Models) | modelli di prodotto pronti in glTF/GLB, materiali PBR curati | per modello, scritta nel `metadata.json` di ogni cartella (CC0 o CC-BY 4.0) | sì per i CC-BY |
| [Poly Haven modelli](https://polyhaven.com/models) | oggetti di scena: macchina fotografica, boombox, sveglia, trapano, vasi, cibo | CC0 ([licenza](https://polyhaven.com/license)) | no |
| [ambientCG](https://ambientcg.com) | materiali PBR (cemento, metalli, tessuti), qualche modello | CC0 ([licenza](https://ambientcg.com/license)) | no |

Modelli Khronos già scaricati e provati in Blender 5.2 (cartella `modelli-3d/`, quelli più grandi solo come link):

| Modello | Licenza (da metadata.json) | Note | Nel repo |
|---|---|---|---|
| [MaterialsVariantsShoe](https://github.com/KhronosGroup/glTF-Sample-Assets/tree/main/Models/MaterialsVariantsShoe) | CC-BY 4.0, © 2021 Shopify | scarpa da corsa, render pulito; usata nel test `test-hyperframes/clip4-blender-impatto` | sì |
| [SunglassesKhronos](https://github.com/KhronosGroup/glTF-Sample-Assets/tree/main/Models/SunglassesKhronos) | CC-BY 4.0, Eric Chadwick / DGG | occhiali, design modificato apposta per non copiare marchi | sì |
| [ChronographWatch](https://github.com/KhronosGroup/glTF-Sample-Assets/tree/main/Models/ChronographWatch) | CC-BY 4.0; contiene il logo DGG (protetto) | orologio; in Blender il quadrante non si vede (usa estensioni glTF non supportate), da sistemare | no |
| [WaterBottle](https://github.com/KhronosGroup/glTF-Sample-Assets/tree/main/Models/WaterBottle) | CC0, Microsoft | borraccia | no |
| [BoomBox](https://github.com/KhronosGroup/glTF-Sample-Assets/tree/main/Models/BoomBox) | CC0, Microsoft | radio | no |
| [ToyCar](https://github.com/KhronosGroup/glTF-Sample-Assets/tree/main/Models/ToyCar) | CC0 | macchinina giocattolo | no |
| [CarConcept](https://github.com/KhronosGroup/glTF-Sample-Assets/tree/main/Models/CarConcept) | CC-BY 4.0 | auto concept | no |
| [IridescenceLamp](https://github.com/KhronosGroup/glTF-Sample-Assets/tree/main/Models/IridescenceLamp) | CC-BY 4.0, Wayfair | lampada iridescente | no |

Credito per i CC-BY, da mettere nei titoli di coda o nella descrizione: "Modello 3D: <nome> di <autore>, CC BY 4.0, via Khronos glTF Sample Assets".

## Luci e ambienti (HDRI)

| Fonte | Cosa | Licenza |
|---|---|---|
| [Poly Haven HDRI](https://polyhaven.com/hdris/studio) | studi fotografici per riflessi e luce (usati: `studio_small_09`, `brown_photostudio_02`) | CC0 |

## Video di stock

| Fonte | Licenza | Limiti principali |
|---|---|---|
| [Pexels](https://www.pexels.com/license/) | uso commerciale gratuito, credito non obbligatorio, si può modificare | niente rivendita del file così com'è; non far sembrare che persone o marchi raffigurati sostengano il prodotto; non usarli come marchio |
| [Pixabay](https://pixabay.com/service/license-summary/) | uso gratuito, credito non obbligatorio, si può modificare (vale anche per musica ed effetti) | niente uso commerciale di contenuti con marchi o loghi riconoscibili; niente rivendita del file così com'è |
| [Mixkit](https://mixkit.co/license/) | ha licenze diverse per video (Free e Restricted), musica ed effetti | controllare su ogni file quale licenza vale |

Elenco già pronto di clip Pexels per la finanza: `../categorie/11-corporate-finanza/stock_commerciale_finanza.csv`.

## Animazioni e suoni

| Fonte | Licenza | Note |
|---|---|---|
| [LottieFiles](https://lottiefiles.com/page/license) | animazioni gratuite utilizzabili anche per scopi commerciali, alle condizioni della Lottie Simple License | chi le ridistribuisce deve mantenere la stessa licenza |
| [Freesound](https://freesound.org) | licenza per singolo suono (CC0, CC-BY, CC-BY-NC) | usare solo CC0 o CC-BY per i clienti; evitare NC |
| [Google Fonts](https://fonts.google.com) | per lo più SIL Open Font License | vedi anche `../fonts/` |

## Cosa non usare

- Video e fotogrammi delle reference premiate (`../test-hyperframes/frames/`): servono solo per studio interno, sono diritti riservati.
- Modelli Sketchfab "free" senza aver letto la licenza del singolo modello (molti sono NC o "editorial").
- File con marchi o persone riconoscibili presi da Pexels/Pixabay in spot che potrebbero sembrare sponsorizzati da loro.
