# Neural Interface v2.1

A retro terminal-style chat interface that connects to n8n webhooks.

## Features

- 🖥️ Retro terminal aesthetic with CRT effects
- 💬 Real-time chat interface
- 🔗 n8n webhook integration
- 🎨 Matrix rain background effect
- 📱 Responsive design

## Local Development

### Prerequisites

- Python 3.9+
- Node.js (for Vercel deployment)

### Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd <repo-name>
```

2. Create a `.env` file (for local development):
```bash
N8N_WEBHOOK_URL=https://your-n8n-webhook-url
```

3. Run the local server:
```bash
python3 server.py
```

4. Open `http://localhost:8000` in your browser

## Deployment to Vercel

### Prerequisites

- Vercel account
- Vercel CLI installed (`npm i -g vercel`)

### Steps

1. **Set Environment Variable in Vercel:**
   - Go to your Vercel project settings
   - Navigate to "Environment Variables"
   - Add: `N8N_WEBHOOK_URL` = `https://your-n8n-webhook-url`

2. **Deploy:**
   ```bash
   vercel
   ```

   Or connect your GitHub repo to Vercel for automatic deployments.

### Environment Variables

- `N8N_WEBHOOK_URL` - Your n8n webhook URL (required)

## Security

- ✅ No API keys or webhooks are exposed in the code
- ✅ All sensitive data is stored in environment variables
- ✅ `.env` files are excluded from git via `.gitignore`

## Project Structure

```
.
├── index.html          # Main frontend interface
├── server.py           # Local development server
├── api/
│   └── webhook.js      # Vercel serverless function
├── vercel.json         # Vercel configuration
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## License

MIT
