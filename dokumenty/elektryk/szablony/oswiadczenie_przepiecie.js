// Szablon: OŚWIADCZENIE ELEKTRYKA o odłączeniu działki od sieci wewnętrznej ROD
// i przyłączeniu do przyłącza indywidualnego (TAURON).
//
// Użycie:
//   node szablony/oswiadczenie_przepiecie.js dane.json
//   node szablony/oswiadczenie_przepiecie.js dane/dzialka_23.json wystawione/
//
// Plik dane.json (wszystkie pola tekstowe; brak pola => kropki do ręcznego wpisania):
// {
//   "data":            "14 września 2026 r.",
//   "dzialka":         "23",
//   "uzytkownik":      "Zofia Zachariasz",
//   "elektryk":        "Tomasz Maksyś",
//   "swiadectwo_e":    "",            // nr świadectwa E
//   "wazne_e":         "",            // data ważności E
//   "swiadectwo_d":    "",            // nr świadectwa D
//   "wazne_d":         "",            // data ważności D
//   "licznik_typ":     "PAFAL typ A52",
//   "licznik_nr":      "24785695",
//   "licznik_stan":    "17 377 kWh",
//   "plik":            "Oswiadczenie_dzialka_23_Zachariasz"   // nazwa pliku wyjściowego (bez .docx)
// }
//
// ZASADY (dekret Tomasza 14.09.2026):
//  - nagłówek: logo ROD po LEWEJ, znak elektryczny ISO 7010 W012 po PRAWEJ + "ELEKTRYK <imię nazwisko>"
//  - znak wstawiany WEKTOROWO (svg + fallback png) — nie rozciągać, proporcje 600x524
//  - żadnych danych wrażliwych z TAURONA (nr umowy, nr licznika Tauronu, PPE)
//  - uprawnienia: osobno E, osobno D + pomiary ochronne do 1 kV

// DANE ELEKTRYKA (pieczątka Tomasza, dekret 19.09.2026 „To są moje dane. Wpisuj za każdym razem"):
//   Tomasz Maksyś – Elektryk, Uprawnienia SEP G1 (E + D + Pomiary)
//   Nr G1/E/470/1081/2025   (eksploatacja)
//   Nr G1/D/470/1082/2025   (dozór)
// Numery wchodzą automatycznie; pola swiadectwo_e / swiadectwo_d w JSON tylko je nadpisują.
// Daty ważności drukują się TYLKO gdy podane w JSON (wazne_e / wazne_d) — na pieczątce ich nie ma.

const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, AlignmentType, LevelFormat, TabStopType,
  Table, TableRow, TableCell, WidthType, BorderStyle, ImageRun, VerticalAlign,
} = require('docx');

const BASE = path.resolve(__dirname, '..');
const A = (f) => path.join(BASE, 'assets', f);
const KROPKI = '……………………………';

const daneFile = process.argv[2];
if (!daneFile) { console.error('Podaj plik JSON z danymi. Przykład: node szablony/oswiadczenie_przepiecie.js dane/dzialka_23.json'); process.exit(1); }
const d = JSON.parse(fs.readFileSync(daneFile, 'utf8'));
const outDir = process.argv[3] || path.join(BASE, 'wystawione');
const v = (k, dom) => (d[k] && String(d[k]).trim()) ? String(d[k]).trim() : (dom !== undefined ? dom : KROPKI);

const F = 'Calibri';
const t = (text, opts = {}) => new TextRun({ text, font: F, size: 22, ...opts });
const p = (children, opts = {}) => new Paragraph({ children, spacing: { after: 160, line: 300 }, ...opts });
const NONE = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };
const nb = { top: NONE, bottom: NONE, left: NONE, right: NONE, insideHorizontal: NONE, insideVertical: NONE };

const naglowek = new Table({
  columnWidths: [1900, 5270, 1900], borders: nb, width: { size: 9070, type: WidthType.DXA },
  rows: [new TableRow({ children: [
    new TableCell({ width: { size: 1900, type: WidthType.DXA }, borders: nb, verticalAlign: VerticalAlign.CENTER,
      children: [new Paragraph({ spacing: { after: 0 }, children: [new ImageRun({
        type: 'png', data: fs.readFileSync(A('logo_rod.png')), transformation: { width: 78, height: 78 },
      })] })] }),
    new TableCell({ width: { size: 5270, type: WidthType.DXA }, borders: nb, verticalAlign: VerticalAlign.CENTER, children: [
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 0 }, children: [
        new TextRun({ text: 'Rodzinny Ogród Działkowy im. Józefa Lompy', font: F, size: 21, bold: true, color: '1F5130' })] }),
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 0 }, children: [
        new TextRun({ text: 'ul. Młyńska 40c, 42-289 Woźniki', font: F, size: 18, color: '444444' })] }),
    ] }),
    new TableCell({ width: { size: 1900, type: WidthType.DXA }, borders: nb, verticalAlign: VerticalAlign.CENTER, children: [
      new Paragraph({ alignment: AlignmentType.RIGHT, spacing: { after: 0 }, children: [new ImageRun({
        type: 'svg', data: fs.readFileSync(A('znak_elektryk.svg')),
        fallback: { type: 'png', data: fs.readFileSync(A('znak_elektryk.png')) },
        transformation: { width: 82, height: 72 },
      })] }),
      new Paragraph({ alignment: AlignmentType.RIGHT, spacing: { before: 40, after: 0 }, children: [
        new TextRun({ text: 'ELEKTRYK', font: F, size: 16, bold: true, color: '444444' })] }),
      new Paragraph({ alignment: AlignmentType.RIGHT, spacing: { after: 0 }, children: [
        new TextRun({ text: v('elektryk', 'Tomasz Maksyś'), font: F, size: 16, color: '444444' })] }),
    ] }),
  ] })],
});

const doc = new Document({
  numbering: { config: [{ reference: 'lista', levels: [{
    level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT,
    style: { paragraph: { indent: { left: 360, hanging: 360 } } } }] }] },
  sections: [{
    properties: { page: { margin: { top: 1000, bottom: 1134, left: 1418, right: 1418 } } },
    children: [
      naglowek,
      new Paragraph({ spacing: { before: 60, after: 200 }, border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: '1F5130' } }, children: [] }),

      p([t(`Woźniki, dnia ${v('data')}`)], { alignment: AlignmentType.RIGHT, spacing: { after: 260 } }),
      p([t('OŚWIADCZENIE ELEKTRYKA', { bold: true, size: 30 })], { alignment: AlignmentType.CENTER, spacing: { after: 80 } }),
      p([t('o odłączeniu działki od sieci wewnętrznej ROD i przyłączeniu do przyłącza indywidualnego', { italics: true })],
        { alignment: AlignmentType.CENTER, spacing: { after: 300 } }),

      p([
        t('Ja, niżej podpisany '),
        t(v('elektryk', 'Tomasz Maksyś'), { bold: true }),
        t(', posiadający świadectwa kwalifikacyjne SEP dla urządzeń, instalacji i sieci elektroenergetycznych o napięciu do 1 kV, wraz z uprawnieniami do wykonywania pomiarów ochronnych (kontrolno-pomiarowych) do 1 kV:'),
      ], { alignment: AlignmentType.JUSTIFIED, spacing: { after: 120 } }),

      p([t('•  eksploatacja (E) — świadectwo nr ', { bold: true }), t(v('swiadectwo_e', 'G1/E/470/1081/2025'), { bold: true }),
         ...(v('wazne_e', '') ? [t(', ważne do dnia '), t(v('wazne_e'))] : []), t(';')],
        { alignment: AlignmentType.LEFT, spacing: { after: 60 }, indent: { left: 360 } }),
      p([t('•  dozór (D) — świadectwo nr ', { bold: true }), t(v('swiadectwo_d', 'G1/D/470/1082/2025'), { bold: true }),
         ...(v('wazne_d', '') ? [t(', ważne do dnia '), t(v('wazne_d'))] : []), t(';')],
        { alignment: AlignmentType.LEFT, spacing: { after: 200 }, indent: { left: 360 } }),

      p([
        t('oświadczam, że w dniu '),
        t(v('data'), { bold: true }),
        t(' na terenie Rodzinnego Ogrodu Działkowego im. Józefa Lompy w Woźnikach, ul. Młyńska 40c, na działce nr '),
        t(v('dzialka', '………'), { bold: true }),
        t(' (użytkownik działki: '),
        t(v('uzytkownik'), { bold: true }),
        t(') wykonałem następujące prace:'),
      ], { alignment: AlignmentType.JUSTIFIED, spacing: { after: 240 } }),

      p([t('trwale odłączyłem instalację elektryczną działki (altany) od wewnętrznej sieci elektroenergetycznej ROD;')],
        { numbering: { reference: 'lista', level: 0 }, alignment: AlignmentType.JUSTIFIED }),
      p([
        t(`odpiąłem podlicznik ogrodowy ${v('licznik_typ', '')}`.replace(/\s+$/, '') + ', nr '),
        t(v('licznik_nr'), { bold: true }),
        t('; stan podlicznika na dzień odłączenia: '),
        t(v('licznik_stan', '………………… kWh'), { bold: true }),
        t(' — do rozliczenia końcowego z Zarządem ROD;'),
      ], { numbering: { reference: 'lista', level: 0 }, alignment: AlignmentType.JUSTIFIED }),
      p([t('przyłączyłem instalację działki do indywidualnego przyłącza elektroenergetycznego (złącze kablowo-pomiarowe w granicy działki, sieć TAURON Dystrybucja S.A.), objętego indywidualną umową zawartą przez użytkownika działki ze sprzedawcą energii;')],
        { numbering: { reference: 'lista', level: 0 }, alignment: AlignmentType.JUSTIFIED }),
      p([t('odłączone przewody sieci wewnętrznej zaizolowałem — są zabezpieczone przed porażeniem; wewnętrzna sieć działkowa pozostaje pod napięciem i zasila pozostałe działki;')],
        { numbering: { reference: 'lista', level: 0 }, alignment: AlignmentType.JUSTIFIED }),
      p([t('od dnia przełączenia działka nie pobiera energii elektrycznej z sieci ogólnoogrodowej ROD.')],
        { numbering: { reference: 'lista', level: 0 }, alignment: AlignmentType.JUSTIFIED, spacing: { after: 300 } }),

      p([t('Prace wykonałem zgodnie z obowiązującymi przepisami oraz zasadami wiedzy technicznej. Po przełączeniu sprawdziłem poprawność działania instalacji — instalacja jest sprawna i nadaje się do dalszej eksploatacji.')],
        { alignment: AlignmentType.JUSTIFIED, spacing: { after: 700 } }),

      new Paragraph({ tabStops: [{ type: TabStopType.RIGHT, position: 9070 }], spacing: { after: 60 },
        children: [t('…………………………………………'), new TextRun({ text: '\t', font: F, size: 22 }), t('…………………………………………')] }),
      new Paragraph({ tabStops: [{ type: TabStopType.RIGHT, position: 9070 }], spacing: { after: 0 }, children: [
        t('podpis użytkownika działki', { size: 18, italics: true }),
        new TextRun({ text: '\t', font: F, size: 18 }),
        t(`${v('elektryk', 'Tomasz Maksyś')} — podpis i pieczęć elektryka`, { size: 18, italics: true }),
      ] }),
      new Paragraph({ spacing: { before: 40 }, children: [t('(potwierdzam odczyt podlicznika)', { size: 18, italics: true })] }),
    ],
  }],
});

const nazwa = (v('plik', '') || `Oswiadczenie_dzialka_${v('dzialka', 'X')}`).replace(/\.docx$/i, '') + '.docx';
fs.mkdirSync(outDir, { recursive: true });
const out = path.join(outDir, nazwa);
Packer.toBuffer(doc).then((b) => { fs.writeFileSync(out, b); console.log('zapisano:', out); });
