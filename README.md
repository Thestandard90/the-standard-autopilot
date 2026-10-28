# The Standard — gratis autogenerator och Instagram-autopublicering

**Status:** Detta paket är färdig kod, inte installerat på dina konton. Daglig produktion fungerar med de medföljande fem manusen; utan en AI-tjänst skapas inga helt nya manus automatiskt. Det roterar mellan fem videor. Repetitiv publicering kan påverka räckvidden negativt, så fyll på med originellt material.

## Installation (engångssteg)

1. Logga in på GitHub och skapa ett **public** repository, exempelvis `the-standard-autopilot`. Lägg upp filerna i det här paketet i repositoryns rot, inklusive `.github/workflows/daily.yml`. Lägg **aldrig tokens i källkoden**.
2. Gå till **Settings → Pages**, välj **Source: GitHub Actions**. GitHub Actions kan köras inom gratisgränser. Allt i den publicerade webbplatsens `site/` blir offentligt; ladda därför aldrig upp den betalda produkten.
3. Under **Actions**, öppna `The Standard daily video` och välj **Run workflow**. När körningen är klar finns filerna under **Artifacts → video-and-caption**. Öppna din GitHub Pages-adress för att se videon. Schemat körs normalt kl. 08:15 UTC varje dag, med möjlig GitHub-fördröjning.
4. Vill du ha automatisk Instagram-publicering: se till att Instagram-kontot är **Business/Creator** och att du har korrekt kopplat Meta-konto, app och behörighet för innehållspublicering. Hämta ditt Instagram user ID och giltig access token via Metas officiella developer-flöde. Tokenförnyelse måste också lösas för verkligt kontinuerlig drift.
5. I repositoryt, välj **Settings → Secrets and variables → Actions**. Lägg till två secrets: `IG_USER_ID` och `IG_ACCESS_TOKEN`. Skapa repository variable `AUTO_PUBLISH_INSTAGRAM` med värdet `true` **först när du testat med en säker testpublicering**. Då försöker arbetsflödet publicera dagens Reel via officiella Meta API. Om publicering misslyckas visas fel i Actions-loggen. Kontrollera tidigare publicering innan manuellt försök så inga dubletter skapas.
6. Ange din Whop-länk i Instagram-profilens URL-fält: `https://whop.com/the-standard-90/the-standard-90-days-to-rebuild-yourself/`. Captions säger `Link in bio` eftersom Instagram normalt inte gör länkar i vanliga captions klickbara.

## TikTok

Ingen automatisk publik TikTok-postning ingår. TikToks Direct Post API kräver auktorisering och audit för offentlig publicering och deras riktlinjer tillåter inte enbart interna uppladdningsverktyg för egna konton. Använd en godkänd tredjepartsintegration eller TikToks egna schemaläggare om du vill ha publik TikTok-publicering.

## Vad kostar det?

Paketet behöver inga betalda AI-API:er. GitHub Free ger en kvot för privata projekt och fria standardkörningar för publika repos. GitHub Pages har användningsgränser och är **inte** en obegränsad videohosting- eller CDN-tjänst. Dagliga videor på runt 0,2 MB är små, men kontrollera faktisk användning och villkor. Du ansvarar för kontoverifiering och eventuell extra tjänstekostnad.

## Begränsningar

- Behöver manuella engångssteg för konton och access. Kan inte anslutas av ChatGPT utan behörighet.
- Hårdvarufri render: FFmpeg + Pillow, originalillustrerad grafik och syntetiskt ljud.
- Just nu 5 manus och ingen internetbaserad trendagent eller försäljningsanalys.
- Instagram publicerar endast om Meta app/behörigheter/token fungerar. Token kan förfalla.
- Schemalagda GitHub Actions kan bli fördröjda eller inaktiveras efter lång inaktivitet.
- Ingen garanti för trafik, intäkter eller plattformsgodkännande.

## Anpassning

Ändra `scripts.json` för att lägga till originella videomanus: `slug`, `seed`, `frames` (4 scener), `caption`. Varje körning väljer manus via dagindex. För lokal testning:

```bash
python -m pip install pillow==12.0.0
python daily.py
```

FFmpeg och DejaVu Sans-font behöver vara installerade. Videon hamnar i `site/daily.mp4`.
