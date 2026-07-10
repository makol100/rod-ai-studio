package pl.rod.fabryka;

import android.app.Activity;
import android.content.Intent;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.os.Bundle;
import android.util.TypedValue;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;

public class MainActivity extends Activity {

    private int dp(int v) {
        return Math.round(TypedValue.applyDimension(
                TypedValue.COMPLEX_UNIT_DIP, v, getResources().getDisplayMetrics()));
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        ScrollView scroll = new ScrollView(this);
        scroll.setBackgroundColor(Color.parseColor("#F4F6F4"));
        scroll.setFillViewport(true);

        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        scroll.addView(root, new ScrollView.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.WRAP_CONTENT));

        // Header
        LinearLayout header = new LinearLayout(this);
        header.setOrientation(LinearLayout.VERTICAL);
        header.setBackgroundResource(R.drawable.header_bg);
        header.setPadding(dp(22), dp(32), dp(22), dp(26));

        TextView title = new TextView(this);
        title.setText("Fabryka Rolek");
        title.setTextColor(Color.WHITE);
        title.setTextSize(TypedValue.COMPLEX_UNIT_SP, 26);
        title.setTypeface(title.getTypeface(), Typeface.BOLD);
        header.addView(title);

        TextView sub = new TextView(this);
        sub.setText("Panel ROD Woźniki");
        sub.setTextColor(Color.parseColor("#CDE6CF"));
        sub.setTextSize(TypedValue.COMPLEX_UNIT_SP, 14);
        sub.setPadding(0, dp(4), 0, 0);
        header.addView(sub);

        root.addView(header, new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.WRAP_CONTENT));

        // Cards
        LinearLayout list = new LinearLayout(this);
        list.setOrientation(LinearLayout.VERTICAL);
        list.setPadding(dp(14), dp(18), dp(14), dp(6));
        root.addView(list);

        addCard(list, "\uD83C\uDFAC", "#E8F3E9", "Nowa rolka", "Wygeneruj rolkę od tematu", "01");
        addCard(list, "\uD83C\uDF9E", "#EAF0FB", "Ostatnie rolki", "Podgląd, poprawki, publikacja", "02");
        addCard(list, "\uD83C\uDF31", "#EAF6EC", "Tematy sezonowe", "Kategorie i baza tematów", "03");
        addCard(list, "\uD83E\uDD16", "#F3EDFB", "Asystent promptu", "Rozbuduj słaby temat (Claude)", "00");
        addCard(list, "\uD83D\uDCCA", "#FBF1E6", "Diagnostyka", "RAM, CPU, dysk, stan serwera", "04");
        addCard(list, "\uD83D\uDDC2", "#EEF1EF", "Cały panel", "Otwórz pełny widok", null);

        // Footer
        TextView footer = new TextView(this);
        footer.setText("v1.1 · panel.157-90-155-155.sslip.io");
        footer.setTextColor(Color.parseColor("#9AA69E"));
        footer.setTextSize(TypedValue.COMPLEX_UNIT_SP, 11);
        footer.setGravity(Gravity.CENTER);
        footer.setPadding(0, dp(12), 0, dp(24));
        root.addView(footer);

        setContentView(scroll);
    }

    private void addCard(LinearLayout parent, String emoji, String tintBg,
                         String titleText, String subtitleText, final String section) {

        LinearLayout card = new LinearLayout(this);
        card.setOrientation(LinearLayout.HORIZONTAL);
        card.setGravity(Gravity.CENTER_VERTICAL);
        card.setBackgroundResource(R.drawable.card_ripple);
        card.setClickable(true);
        card.setFocusable(true);
        card.setPadding(dp(14), dp(14), dp(16), dp(14));
        card.setElevation(dp(2));

        LinearLayout.LayoutParams cp = new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT);
        cp.bottomMargin = dp(12);
        card.setLayoutParams(cp);

        TextView icon = new TextView(this);
        icon.setText(emoji);
        icon.setTextSize(TypedValue.COMPLEX_UNIT_SP, 22);
        icon.setGravity(Gravity.CENTER);
        GradientDrawable chip = new GradientDrawable();
        chip.setShape(GradientDrawable.RECTANGLE);
        chip.setCornerRadius(dp(14));
        chip.setColor(Color.parseColor(tintBg));
        icon.setBackground(chip);
        LinearLayout.LayoutParams ip = new LinearLayout.LayoutParams(dp(50), dp(50));
        ip.rightMargin = dp(14);
        icon.setLayoutParams(ip);
        card.addView(icon);

        LinearLayout texts = new LinearLayout(this);
        texts.setOrientation(LinearLayout.VERTICAL);
        texts.setLayoutParams(new LinearLayout.LayoutParams(
                0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f));

        TextView t = new TextView(this);
        t.setText(titleText);
        t.setTextColor(Color.parseColor("#1B2420"));
        t.setTextSize(TypedValue.COMPLEX_UNIT_SP, 16);
        t.setTypeface(t.getTypeface(), Typeface.BOLD);
        texts.addView(t);

        TextView st = new TextView(this);
        st.setText(subtitleText);
        st.setTextColor(Color.parseColor("#5F6B63"));
        st.setTextSize(TypedValue.COMPLEX_UNIT_SP, 13);
        st.setPadding(0, dp(2), 0, 0);
        texts.addView(st);

        card.addView(texts);

        TextView chev = new TextView(this);
        chev.setText("\u203A");
        chev.setTextColor(Color.parseColor("#B5C0B8"));
        chev.setTextSize(TypedValue.COMPLEX_UNIT_SP, 24);
        chev.setPadding(dp(8), 0, 0, 0);
        card.addView(chev);

        card.setOnClickListener(new View.OnClickListener() {
            @Override public void onClick(View v) {
                Intent i = new Intent(MainActivity.this, WebActivity.class);
                if (section != null) i.putExtra(WebActivity.EXTRA_SECTION, section);
                startActivity(i);
            }
        });

        parent.addView(card);
    }
}
