/**
 * Vercel serverless function to proxy requests to n8n webhook.
 * This handles CORS and converts POST requests to GET requests with query parameters.
 */

export default async function handler(req, res) {
  // Handle CORS preflight
  if (req.method === 'OPTIONS') {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS, GET');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    return res.status(200).end();
  }

  // Only handle POST requests
  if (req.method !== 'POST') {
    res.setHeader('Access-Control-Allow-Origin', '*');
    return res.status(405).json({ error: 'Method not allowed' });
  }

  // Get n8n webhook URL from environment variable
  const n8nWebhookUrl = process.env.N8N_WEBHOOK_URL;

  if (!n8nWebhookUrl) {
    res.setHeader('Access-Control-Allow-Origin', '*');
    return res.status(500).json({ error: 'N8N_WEBHOOK_URL environment variable not set' });
  }

  try {
    // Get message from request body
    const { message } = req.body || {};
    
    // Build URL with message as query parameter
    let webhookUrl;
    if (message) {
      const encodedMessage = encodeURIComponent(message);
      webhookUrl = `${n8nWebhookUrl}?message=${encodedMessage}`;
    } else {
      webhookUrl = n8nWebhookUrl;
    }

    // Send GET request to n8n webhook
    const response = await fetch(webhookUrl, {
      method: 'GET',
    });

    const responseData = await response.text();
    let jsonData;
    
    try {
      jsonData = JSON.parse(responseData);
    } catch {
      jsonData = { text: responseData };
    }

    // Return response
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Content-Type', 'application/json');
    return res.status(response.status).json(jsonData);

  } catch (error) {
    res.setHeader('Access-Control-Allow-Origin', '*');
    return res.status(500).json({ error: error.message });
  }
}
