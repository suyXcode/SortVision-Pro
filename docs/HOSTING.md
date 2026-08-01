# Hosting Guide — SortVision Pro

This app is a stateless Flask service (no database), so it can be deployed
almost anywhere that runs Python or Docker. Below are complete, step-by-step
instructions for the three paths already wired into the repo: **Render**
(easiest, free tier available), **Railway** (also easy, usage-based
pricing), and **Docker on any VPS** (most control, e.g. DigitalOcean,
Hetzner, AWS Lightsail, a home server).

Whichever you choose, set the `SITE_URL` environment variable to your final
domain (e.g. `https://sortvisionpro.com`) — it's used to build canonical
links, the sitemap, and Open Graph tags, so search engines and social
previews resolve correctly instead of pointing at `localhost`.

---

## Option 1 — Render (recommended for most people)

Render offers a free web service tier, automatic HTTPS, and zero server
management.

1. **Push the code to GitHub.**
   ```bash
   cd sortvision-pro
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/<your-username>/sortvision-pro.git
   git push -u origin main
   ```

2. **Create the service.**
   - Go to [render.com](https://render.com) and sign in (GitHub login is
     fastest).
   - Click **New → Blueprint**, select your repository. Render reads
     `render.yaml` automatically and pre-fills the build/start commands.
   - If you'd rather configure it by hand instead of the blueprint: **New
     → Web Service** → select the repo →
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `gunicorn --bind 0.0.0.0:$PORT --workers 3 --threads 2 --timeout 60 app:app`
     - **Instance type:** Free (or Starter for always-on, no cold starts)

3. **Set environment variables** (Render dashboard → your service →
   **Environment**):
   | Key | Value |
   |---|---|
   | `SECRET_KEY` | a random string (Render can auto-generate one) |
   | `APP_CONFIG` | `production` |
   | `SITE_URL` | `https://<your-service-name>.onrender.com` (update after step 4) |
   | `CORS_ORIGINS` | `*` (or your domain once you have one) |

4. **Deploy.** Render builds and starts the service automatically. You'll
   get a URL like `https://sortvision-pro.onrender.com` — copy it back into
   `SITE_URL` (step 3) and let it redeploy so canonical links are correct.

5. **Custom domain (optional).** Render dashboard → **Settings → Custom
   Domain** → add your domain → follow the CNAME/A-record instructions at
   your DNS provider. Render provisions a free TLS certificate
   automatically once DNS propagates. Update `SITE_URL` to the custom
   domain afterward.

Free-tier services spin down after inactivity and take ~30–60s to wake on
the next request — upgrade to a paid instance type if you need it always
warm.

---

## Option 2 — Railway

Railway auto-detects the included `Procfile`.

1. Push the repo to GitHub (same as step 1 above, if not done already).
2. Go to [railway.app](https://railway.app) → **New Project → Deploy from
   GitHub repo** → select `sortvision-pro`.
3. Railway detects `Procfile` and builds automatically — no build/start
   command configuration needed.
4. **Variables tab** → add:
   - `SECRET_KEY` — a random string
   - `APP_CONFIG` — `production`
   - `SITE_URL` — the Railway-generated domain (Settings → Networking →
     **Generate Domain**), e.g. `https://sortvision-pro-production.up.railway.app`
5. Once the domain is generated, redeploy (or it will auto-redeploy on the
   next variable change) so `SITE_URL` takes effect.
6. **Custom domain (optional):** Settings → Networking → **Custom Domain**
   → add your domain → set the CNAME record Railway shows you at your DNS
   provider. Update `SITE_URL` once it's live.

---

## Option 3 — Docker on your own VPS (full control)

Use this if you want a fixed IP, no cold starts, and full control over the
environment — e.g. a $5–6/mo DigitalOcean droplet, Hetzner CX, or AWS
Lightsail instance running Ubuntu 22.04+.

### 1. Provision the server and install Docker

```bash
ssh root@your-server-ip

curl -fsSL https://get.docker.com | sh
apt-get install -y docker-compose-plugin
```

### 2. Get the code onto the server

```bash
git clone https://github.com/<your-username>/sortvision-pro.git
cd sortvision-pro
```

### 3. Configure environment variables

Edit `docker-compose.yml` (or create a `.env` file next to it) and set:

```yaml
environment:
  - APP_CONFIG=production
  - PORT=8000
  - SECRET_KEY=<a long random string>
  - SITE_URL=https://your-domain.com
  - CORS_ORIGINS=https://your-domain.com
```

### 4. Build and run

```bash
docker compose up -d --build
```

The app is now listening on port 8000 on the server. Verify with
`curl http://localhost:8000` from the server itself.

### 5. Put Nginx in front (reverse proxy + HTTPS)

```bash
apt-get install -y nginx certbot python3-certbot-nginx
```

Create `/etc/nginx/sites-available/sortvision-pro`:

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable it and get a free TLS certificate:

```bash
ln -s /etc/nginx/sites-available/sortvision-pro /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx

certbot --nginx -d your-domain.com -d www.your-domain.com
```

Certbot edits the Nginx config to redirect HTTP → HTTPS and auto-renews
the certificate. Point your domain's A record at the server's IP before
running `certbot` (DNS needs to resolve for the certificate challenge to
succeed).

### 6. Keep it running / redeploying

```bash
# Pull latest code and rebuild after changes:
git pull
docker compose up -d --build

# View logs:
docker compose logs -f

# Restart:
docker compose restart
```

---

## Post-deploy SEO checklist

Once your domain is live, do these once:

1. Confirm `SITE_URL` is set to your **final HTTPS domain** everywhere the
   app is deployed — this drives canonical URLs, `sitemap.xml`,
   `robots.txt`, and Open Graph/Twitter previews.
2. Visit `https://your-domain.com/robots.txt` and
   `https://your-domain.com/sitemap.xml` to confirm they resolve with the
   correct domain.
3. Submit the sitemap in [Google Search
   Console](https://search.google.com/search-console) (Sitemaps → enter
   `sitemap.xml`) and [Bing Webmaster
   Tools](https://www.bing.com/webmasters) — this gets pages indexed much
   faster than waiting for organic crawling.
4. Test social previews with the [Facebook Sharing
   Debugger](https://developers.facebook.com/tools/debug/) and
   [Twitter/X Card
   Validator](https://cards-dev.twitter.com/validator) to confirm the OG
   image and description render correctly.
5. Run the page through [Google's Rich Results
   Test](https://search.google.com/test/rich-results) to confirm the
   JSON-LD structured data is picked up without errors.
