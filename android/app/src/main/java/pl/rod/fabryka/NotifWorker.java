package pl.rod.fabryka;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Build;

import androidx.annotation.NonNull;
import androidx.core.app.NotificationCompat;
import androidx.work.Worker;
import androidx.work.WorkerParameters;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

/**
 * Sprawdza co ~15 min, czy pojawiła się NOWA GOTOWA rolka.
 * Bez Firebase, bez kont — zwykłe odpytanie /reels i lokalne powiadomienie.
 */
public class NotifWorker extends Worker {

    private static final String API = "https://panel.157-90-155-155.sslip.io/reels";
    private static final String PREFS = "fabryka";
    private static final String KEY_LAST = "ostatnia_gotowa";
    private static final String CHANNEL = "rolki";

    public NotifWorker(@NonNull Context c, @NonNull WorkerParameters p) {
        super(c, p);
    }

    @NonNull
    @Override
    public Result doWork() {
        try {
            HttpURLConnection con = (HttpURLConnection) new URL(API).openConnection();
            con.setConnectTimeout(10000);
            con.setReadTimeout(10000);

            StringBuilder sb = new StringBuilder();
            try (BufferedReader r = new BufferedReader(
                    new InputStreamReader(con.getInputStream(), "UTF-8"))) {
                String l;
                while ((l = r.readLine()) != null) sb.append(l);
            }

            JSONObject root = new JSONObject(sb.toString());
            JSONArray reels = root.optJSONArray("reels");
            if (reels == null || reels.length() == 0) return Result.success();

            // najnowsza GOTOWA rolka (lista idzie od najnowszej)
            int noweId = -1;
            String tytul = "";
            for (int i = 0; i < reels.length(); i++) {
                JSONObject x = reels.getJSONObject(i);
                if ("gotowa".equals(x.optString("status"))) {
                    noweId = x.optInt("id", -1);
                    tytul = x.optString("title", "");
                    break;
                }
            }
            if (noweId < 0) return Result.success();

            SharedPreferences sp = getApplicationContext()
                    .getSharedPreferences(PREFS, Context.MODE_PRIVATE);
            int znane = sp.getInt(KEY_LAST, -1);

            if (znane == -1) {
                // pierwszy przebieg — zapamiętaj stan, nie strasz starą rolką
                sp.edit().putInt(KEY_LAST, noweId).apply();
                return Result.success();
            }
            if (noweId <= znane) return Result.success();

            sp.edit().putInt(KEY_LAST, noweId).apply();
            powiadom(noweId, tytul);
            return Result.success();

        } catch (Exception e) {
            return Result.retry();
        }
    }

    private void powiadom(int id, String tytul) {
        Context ctx = getApplicationContext();
        NotificationManager nm =
                (NotificationManager) ctx.getSystemService(Context.NOTIFICATION_SERVICE);

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            nm.createNotificationChannel(new NotificationChannel(
                    CHANNEL, "Gotowe rolki", NotificationManager.IMPORTANCE_DEFAULT));
        }

        Intent i = new Intent(ctx, WebActivity.class);
        i.putExtra(WebActivity.EXTRA_SECTION, "02"); // Ostatnie rolki
        i.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TOP);
        PendingIntent pi = PendingIntent.getActivity(ctx, id, i,
                PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);

        String krotki = tytul.length() > 70 ? tytul.substring(0, 67) + "…" : tytul;

        Notification n = new NotificationCompat.Builder(ctx, CHANNEL)
                .setSmallIcon(android.R.drawable.stat_sys_download_done)
                .setContentTitle("Rolka #" + String.format("%06d", id) + " gotowa 🎬")
                .setContentText(krotki)
                .setStyle(new NotificationCompat.BigTextStyle().bigText(krotki))
                .setContentIntent(pi)
                .setAutoCancel(true)
                .build();

        nm.notify(id, n);
    }
}
