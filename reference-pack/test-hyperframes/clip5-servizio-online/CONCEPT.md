# Spot "Peso" per un servizio online (20 s)

Seguito del test `clip4-blender-impatto`, stesso linguaggio (vuoto nero, luce di taglio, "dopo il disastro"), ma applicato a un servizio digitale che non ha un prodotto fisico da mostrare.

## Brief (inventato)
- **Brand:** PRATICA, servizio online che gestisce la burocrazia (730, bollette, documenti, ricorsi) al posto tuo, da telefono.
- **Messaggio unico:** la burocrazia pesa, con PRATICA diventa leggera.
- **Pubblico:** 25-45 anni, odiano code e moduli.
- **Formato:** 16:9, 1920×1080, 60 fps, 20 s. Taglio da 6 s ricavabile dai secondi 6-12.

## Idea
Il servizio non si vede, quindi si mostra il suo contrario: il **peso**. Un monolite fatto di fogli, raccoglitori e timbri cade nel buio e sfonda il pavimento. Dopo l'impatto, nel cratere, i fogli si alzano, si piegano e si ricompongono in un'unica card luminosa: l'interfaccia di PRATICA con la spunta "Pratica inviata". Il peso diventa un tocco.

Perché funziona (vedi `fondamenti/efficacia-pubblicitaria.md`): emozione prima della funzione, una sola metafora, asset distintivo (la card arancione con la spunta) che può tornare in ogni spot della serie. Rischio "emisfero sinistro" (oggetto nel vuoto, testo): lo bilanciamo con un'azione che si sviluppa e un suono con carattere. La prossima versione può mettere il monolite in un luogo vero (una cucina, un ufficio postale).

## Reference
- Bullpadel Xplo (Kutuko): il cratere invece dell'urto, ritmo che accelera.
- Nike Air Max Dn8: vuoto nero, luce di taglio.
- Airbnb "Same Room": la trasformazione dentro un solo piano.
- Notion "What is Notion?": l'interfaccia che nasce da un oggetto, senza stacchi.

## Scaletta (secondi)
| s | Beat | Inquadratura | Strumento |
|---|---|---|---|
| 0-2.5 | gancio | buio; una luce di taglio scopre un monolite alto 3 m di fogli e raccoglitori, sospeso | Blender |
| 2.5-4.5 | tensione | macro lenta sui bordi dei fogli, un timbro "URGENTE", una graffetta. Sub che sale | Blender |
| 4.5-6 | caduta | campo basso, il monolite cade; impatto a 6.0 s, scossa di camera, poi 4 frame di nero | Blender |
| 6-8.5 | dopo il disastro | vista dall'alto: cratere, crepe, fogli sparsi (rigid body + frattura) | Blender |
| 8.5-12 | rivelazione | i fogli si sollevano e girano verso il centro, si piegano uno nell'altro e diventano una card sottile e luminosa | Blender (animazione) |
| 12-15.5 | prova | la card si avvicina in camera: sopra appare l'interfaccia "730 · Inviata ✓ · 3 min" | HyperFrames sopra il render |
| 15.5-17.5 | claim | "PESANTE PER NOI." / "LEGGERA PER TE." | HyperFrames |
| 17.5-20 | end card | logo PRATICA, "La burocrazia, dal telefono." | HyperFrames |

## Look
- Fondo nero, pavimento cemento scuro (roughness 0.8), key calda da destra, rim fredda, ombra di contatto.
- Fogli bianco carta (non bianco puro, #EDEAE3), raccoglitori grigio e un solo blu scuro.
- Unico colore d'accento: arancione #FF5A1F, solo sulla card e sulla spunta.
- Tipografia: la stessa famiglia del test Impatto per continuità.

## Suono
Sub che sale da 2.5 a 6 s, silenzio di 4 frame, colpo con coda di carta che ricade, poi fruscio di fogli che salgono e un "tic" pulito quando appare la spunta (il suono-asset del brand). Effetti CC0 da Freesound o sintetici in ffmpeg. Mix −14 LUFS, picco −1 dBTP.

## Limiti dichiarati
- Brand e interfaccia inventati.
- Il primo render è un test di linguaggio: frattura e polvere migliorano rispetto a Impatto ma restano semplici.
