# PawaPay Integration

This project demonstrates integration with PawaPay's payment API, including deposit creation and callback handling.

## Setup Instructions

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd pawapay
   ```

2. **Create and activate virtual environment**

   ```bash
   # Create virtual environment
   python -m venv venv

   # Activate virtual environment
   # On Windows:
   .\venv\Scripts\activate
   # On Unix or MacOS:
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file in the root directory with the following content:

   ```
   PAWAPAY_API_TOKEN=your_api_token_here
   PAWAPAY_API_URL=https://api.sandbox.pawapay.io/deposits
   ```

## Project Structure

- `app.py` - Main application for creating deposits
- `callback_server.py` - Flask server for handling PawaPay callbacks
- `requirements.txt` - Project dependencies
- `.env` - Environment variables (not tracked in git)

## Testing Process

### 1. Testing Deposit Creation

Run the deposit creation script:

```bash
python app.py
```

This will:

- Generate a unique deposit ID
- Create a deposit request to PawaPay
- Print the API response

### 2. Testing Callback Server

1. Start the callback server:

   ```bash
   python callback_server.py
   ```

2. The server will be available at:

   - Local: `http://localhost:5000`
   - Network: `http://your-ip:5000`

3. Available endpoints:
   - View all callbacks: `GET http://localhost:5000/view`
   - Deposit callback: `POST http://localhost:5000/deposits`
   - Payout callback: `POST http://localhost:5000/payouts`
   - Refund callback: `POST http://localhost:5000/refunds`

### 3. Testing Callbacks Locally

You can test the callback endpoints using curl or Postman:

```bash
# Test deposit callback
curl -X POST http://localhost:5000/deposits \
  -H "Content-Type: application/json" \
  -d '{"depositId": "test-123", "status": "SUCCESS"}'

# View all callbacks
curl http://localhost:5000/view
```

## Making Callbacks Publicly Accessible

To make the callback server accessible to PawaPay:

1. Install ngrok:

   ```bash
   pip install pyngrok
   ```

2. Start ngrok:

   ```bash
   ngrok http 5000
   ```

3. Use the provided ngrok URL in your PawaPay dashboard:
   - Deposit callback: `https://your-ngrok-url/deposits`
   - Payout callback: `https://your-ngrok-url/payouts`
   - Refund callback: `https://your-ngrok-url/refunds`

## Security Notes

- Never commit the `.env` file to version control
- Keep your API token secure
- In production, use proper authentication for callback endpoints
- Consider using a database instead of in-memory storage for callbacks

## Error Handling

The callback server will:

- Log all incoming callbacks
- Store them in memory (in production, use a database)
- Return 200 status for successful receipt
- Print detailed information to the console

## Support

For issues or questions:

1. Check the PawaPay API documentation
2. Review the error messages in the console
3. Contact PawaPay support for API-related issues
