// Szablon: OŚWIADCZENIE o wykonaniu i zabezpieczeniu KABLA ZASILAJĄCEGO
// (od złącza kablowo-pomiarowego / licznika do punktu przyłączeniowego na działce).
// UWAGA: dotyczy WYŁĄCZNIE kabla — nie obejmuje instalacji altany ani instalacji na działce (dekret 14.09.2026).
// (krótkie pismo — odpowiednik tego, które działkowcy dostają od swoich elektryków;
//  potrzebne zarządowi przed wydaniem karty danych technicznych / przyłączeniem do Tauronu)
//
// Użycie:
//   node szablony/oswiadczenie_sprawnosc.js dane/sprawnosc_17.json
//
// Pola JSON (puste = kropki do ręcznego wpisania):
// { "data":"14 września 2026 r.", "dzialka":"17", "uzytkownik":"Jan Kowalski",
//   "elektryk":"Tomasz Maksyś", "swiadectwo_e":"", "wazne_e":"", "swiadectwo_d":"", "wazne_d":"",
//   "zakres":"", "plik":"Oswiadczenie_sprawnosc_dzialka_17" }
//
// "zakres" — jeśli puste, wchodzi zdanie domyślne o zabezpieczeniu kabla od licznika do działki.

const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, AlignmentType,
  Table, TableRow, TableCell, WidthType, BorderStyle, ImageRun, VerticalAlign,
} = require('docx');

const BASE = path.resolve(__dirname, '..');
const A = (f) => path.join(BASE, 'assets', f);
const KROPKI = '……………………………';

const daneFile = process.argv[2];
if (!daneFile) { console.error('Podaj plik JSON z danymi.'); process.exit(1); }
const d = JSON.parse(fs.readFileSync(daneFile, 'utf8'));
const outDir = process.argv[3] || path.join(BASE, 'wystawione');
const v = (k, dom) => (d[k] && String(d[k]).trim()) ? String(d[k]).trim() : (dom !== undefined ? dom : KROPKI);

const F = 'Calibri';
const t = (text, o = {}) => new TextRun({ text, font: F, size: 22, ...o });
const p = (children, o = {}) => new Paragraph({ children, spacing: { after: 160, line: 300 }, ...o });
const NONE = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };
const nb = { top: NONE, bottom: NONE, left: NONE, right: NONE, insideHorizontal: NONE, insideVertical: NONE };

const naglowek = new Table({
  columnWidths: [1900, 5270, 1900], borders: nb, width: { size: 9070, type: WidthType.DXA },
  rows: [new TableRow({ children: [
    new TableCell({ width: { size: 1900, type: WidthType.DXA }, borders: nb, verticalAlign: VerticalAlign.CENTER,
      children: [new Paragraph({ spacing: { after: 0 }, children: [new ImageRun({
        type: 'png', data: fs.readFileSync(A('logo_rod.png')), transformation: { width: 78, height: 78 } })] })] }),
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
        transformation: { width: 82, height: 72 } })] }),
      new Paragraph({ alignment: AlignmentType.RIGHT, spacing: { before: 40, after: 0 }, children: [
        new TextRun({ text: 'ELEKTRYK', font: F, size: 16, bold: true, color: '444444' })] }),
      new Paragraph({ alignment: AlignmentType.RIGHT, spacing: { after: 0 }, children: [
        new TextRun({ text: v('elektryk', 'Tomasz Maksyś'), font: F, size: 16, color: '444444' })] }),
    ] }),
  ] })],
});

const ZAKRES_DOMYSLNY = 'Oświadczenie dotyczy wyłącznie kabla zasilającego od licznika do punktu przyłączeniowego. Nie obejmuje instalacji elektrycznej altany (domku) ani pozostałej instalacji na działce.';

const doc = new Document({ sections: [{
  properties: { page: { margin: { top: 1000, bottom: 1134, left: 1418, right: 1418 } } },
  children: [
    naglowek,
    new Paragraph({ spacing: { before: 60, after: 200 }, border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: '1F5130' } }, children: [] }),

    p([t(`Woźniki, dnia ${v('data')}`)], { alignment: AlignmentType.RIGHT, spacing: { after: 300 } }),
    p([t('OŚWIADCZENIE', { bold: true, size: 30 })], { alignment: AlignmentType.CENTER, spacing: { after: 80 } }),
    p([t('o wykonaniu i zabezpieczeniu kabla zasilającego', { italics: true })], { alignment: AlignmentType.CENTER, spacing: { after: 340 } }),

    p([
      t('Oświadczam, że kabel zasilający od złącza kablowo-pomiarowego (licznika) do punktu przyłączeniowego na działce nr '),
      t(v('dzialka', '………'), { bold: true }),
      t(' w Rodzinnym Ogrodzie Działkowym im. Józefa Lompy w Woźnikach (użytkownik działki: '),
      t(v('uzytkownik')),
      t(') został wykonany i zabezpieczony zgodnie z obowiązującymi przepisami i zasadami wiedzy technicznej, jest w pełni sprawny i nadaje się do przyłączenia do sieci energetycznej.'),
    ], { alignment: AlignmentType.JUSTIFIED, spacing: { after: 240 } }),

    p([t(v('zakres', ZAKRES_DOMYSLNY))], { alignment: AlignmentType.JUSTIFIED, spacing: { after: 300 } }),

    p([t('Świadectwa kwalifikacyjne SEP do 1 kV wraz z uprawnieniami do pomiarów ochronnych:')],
      { alignment: AlignmentType.JUSTIFIED, spacing: { after: 120 } }),
    p([t('•  eksploatacja (E) — świadectwo nr ', { bold: true }), t(v('swiadectwo_e')), t(', ważne do dnia '), t(v('wazne_e', '………………………')), t(';')],
      { spacing: { after: 60 }, indent: { left: 360 } }),
    p([t('•  dozór (D) — świadectwo nr ', { bold: true }), t(v('swiadectwo_d')), t(', ważne do dnia '), t(v('wazne_d', '………………………')), t(';')],
      { spacing: { after: 760 }, indent: { left: 360 } }),

    new Paragraph({ alignment: AlignmentType.RIGHT, spacing: { after: 60 }, children: [t('…………………………………………')] }),
    new Paragraph({ alignment: AlignmentType.RIGHT, spacing: { after: 0 }, children: [
      t(`${v('elektryk', 'Tomasz Maksyś')} — podpis i pieczęć elektryka`, { size: 18, italics: true })] }),
  ],
}] });

const nazwa = (v('plik', '') || `Oswiadczenie_kabel_dzialka_${v('dzialka', 'X')}`).replace(/\.docx$/i, '') + '.docx';
fs.mkdirSync(outDir, { recursive: true });
const out = path.join(outDir, nazwa);
Packer.toBuffer(doc).then((b) => { fs.writeFileSync(out, b); console.log('zapisano:', out); });
