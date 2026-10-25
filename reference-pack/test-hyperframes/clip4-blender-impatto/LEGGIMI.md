# Test Blender "Impatto" (15 s)

Primo test 3D vero in Blender 5.2 (Eevee), fatto sul Mac il 2026-10-24. Prodotto: la scarpa [MaterialsVariantsShoe](../../risorse-commerciali/modelli-3d/) di Shopify (CC BY 4.0). Credito obbligatorio se si pubblica: "Modello 3D: Materials Variants Shoe di Shopify, CC BY 4.0".

## Da quali reference
- **Bullpadel Xplo 02** (Kutuko): l'espediente "dopo il disastro", cioè si vede il cratere e non l'impatto; ritmo che accelera (16 tagli in 31 s, misurato).
- **Nike Air Max Dn8**: prodotto nel vuoto nero, luce di taglio.
- **Studio River / Hublot**: immobilità tenuta a lungo sull'inquadratura finale.

## Scaletta (secondi, 25 fps)
| s | Inquadratura |
|---|---|
| 0-3 | scarpa sospesa al buio, una luce di taglio gira e la rivela |
| 3-5 | macro sulla tomaia, fuoco corto |
| 5-6 | campo basso vuoto, la scarpa cade dall'alto; impatto a 5.96 s con scossa di camera |
| 7-8.5 | vista dall'alto: cratere, crepe e schegge (la conseguenza, non l'urto) |
| 8.5-10 | tre dettagli rapidi da 0.5 s: tallone, lacci, schegge |
| 10-12.5 | eroe: orbita lenta sulla scarpa nel cratere |
| 12.5-15 | cartello "LEGGERA. / FINO ALL'IMPATTO." |

## File
- `impatto-test.mp4`: il test, 1920x1080, 25 fps, con suono sintetico fatto in ffmpeg (sub che sale, silenzio, colpo, coda).
- `spot_impatto.py`: scena completa, si rigenera con
  `~/Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup -P spot_impatto.py -- <scarpa.glb> <studio.exr> <cartella/f_> final`
  (HDRI `studio_small_09` di Poly Haven, CC0). Modalità `stills` per 10 fotogrammi di prova in 10 s.
- `card.filter`: cartello finale per ffmpeg.
- Render: 312 fotogrammi in 20 min 43 s su M1 (circa 4 s a fotogramma), costo zero.

## Cosa va migliorato
- Le schegge sono poliedri semplici e il cratere è una macchia piatta: servono frattura vera (Cell Fracture), polvere e particelle.
- Manca un suono vero: un sound design da libreria CC0 o da ElevenLabs.
- La scarpa ha la scritta del modello sulla suola: per un cliente si usa il suo prodotto.
- Il dettaglio a 9.4 s è poco leggibile: va spostato o tolto.
