# Principi di movimento

Regole numeriche da applicare a ogni clip. Dove c'è scritto "da verificare" il valore viene dalla pratica comune e non da una fonte aperta.

## Curve di easing

| Uso | Curva | Fonte |
| --- | --- | --- |
| Elemento che entra | `cubic-bezier(0.05, 0.7, 0.1, 1)` (Material 3 emphasized decelerate) | [Material Components](https://github.com/material-components/material-components-android/blob/master/docs/theming/Motion.md) |
| Elemento che esce | `cubic-bezier(0.3, 0, 0.8, 0.15)` (Material 3 emphasized accelerate) | idem |
| Elemento che si sposta restando a schermo | `cubic-bezier(0.2, 0, 0, 1)` (Material 3 standard) | idem |
| Momento importante | `cubic-bezier(0.4, 0.14, 0.3, 1)` (Carbon expressive) | [IBM Carbon](https://carbondesignsystem.com/elements/motion/overview/) |
| Entrata espressiva | `cubic-bezier(0, 0, 0.3, 1)` (Carbon expressive entrance) | idem |
| Lineare | solo rotazioni continue, ticker, dissolvenze di opacità | [Fluent 2](https://fluent2.microsoft.design/motion) |

Nel codice delle clip: `oE` (esponenziale in uscita) per gli slam, `oC` (cubica in uscita) per entrate morbide, `ioC` per spostamenti, `oB` (back) per overshoot.

## Durate

Le durate UI dei design system vanno da 50 a 1000 ms, quasi tutte tra 150 e 400 ms. Nel video si possono allungare di 1,5-2 volte, perché il movimento è il contenuto (inferenza, da confermare).

| ms | frame a 24 fps | a 30 fps | a 60 fps | Uso tipico |
| --- | --- | --- | --- | --- |
| 100 | 2,4 | 3 | 6 | dissolvenza, cambio colore |
| 200 | 4,8 | 6 | 12 | bottone, chip |
| 300 | 7,2 | 9 | 18 | pannello, card |
| 500 | 12 | 15 | 30 | cambio di schermata |
| 700 | 16,8 | 21 | 42 | reveal importante |

- Le uscite durano meno delle entrate, circa il 70-80% (da verificare).
- Più lontano va un oggetto, più dura il movimento (Carbon, Fluent).

## Ritmo e coreografia

- Sfalsa gli elementi di 2-4 frame: due elementi principali non arrivano mai nello stesso frame (da verificare).
- Anticipazione: 2-4 frame di rinculo prima di un movimento grande.
- Overshoot: al massimo il 10% per un brand serio, 10-15% per un brand giocoso. Ogni rimbalzo è più piccolo del precedente.
- Pausa su una posa: almeno 6-8 frame a 24 fps perché si registri.
- Un'azione principale alla volta. Niente assestamenti esponenziali lunghi (IBM).
- Motion blur con otturatore a 180°.

## Gli errori che fanno sembrare un video economico

- Keyframe lineari o con l'easing di default.
- Niente motion blur, maschere con bordi duri.
- Tutto che si muove insieme.
- Color grading fatto senza scope.
- Testo animato come un blocco unico invece che per parola o per lettera.

Fonte: [PremiumBeat](https://www.premiumbeat.com/blog/10-after-effects-mistakes-avoid), [IBM classic principles](https://www.ibm.com/design/language/animation/classic-principles).
