# DevStore — Payment Processing Portfolio Project

A sample e-commerce web application demonstrating Stripe Checkout integration using Next.js. Built as a portfolio project to showcase full-stack payment processing.

---

## Tech Stack

| Layer      | Technology                                          |
|------------|-----------------------------------------------------|
| Framework  | [Next.js 14](https://nextjs.org) (Pages Router)     |
| Payments   | [Stripe Checkout](https://stripe.com/docs/payments/checkout) |
| Styling    | Plain CSS (no framework)                            |
| Hosting    | [Vercel](https://vercel.com) (recommended)          |

---

## How It Works

```
User clicks "Buy Now"
        |
        v
POST /api/checkout  <-- sends product name, description, price
        |
        v
Server creates a Stripe Checkout Session (secret key used here, never on client)
        |
        v
Client redirected to Stripe's hosted payment page
        |
        +--[Payment success]--> /success?session_id=...  (fetches session details server-side)
        |
        +--[User cancels]-----> /cancel
```

---

## Prerequisites

- Node.js 18 or higher
- A free [Stripe account](https://stripe.com)

---

## Local Setup

### 1. Clone and install dependencies

```bash
git clone https://github.com/timjavier31-dot/LocalTestTim.git
cd LocalTestTim/payment-portfolio
npm install
```

### 2. Get your Stripe API keys

1. Sign up or log in at [dashboard.stripe.com](https://dashboard.stripe.com)
2. Go to **Developers → API Keys**
3. Make sure you are in **Test mode** (toggle in the top right)
4. Copy your **Secret key** (starts with `sk_test_`)

### 3. Set up environment variables

```bash
cp .env.local.example .env.local
```

Edit `.env.local` and fill in your values:

```env
STRIPE_SECRET_KEY=<paste your sk_test_... key here>
NEXT_PUBLIC_BASE_URL=http://localhost:3000
```

> **Important:** Never commit `.env.local` to version control. It is already listed in `.gitignore`.

### 4. Start the development server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## Test Payments

Stripe provides test card numbers that simulate real payment scenarios. **No real money is charged.**

| Card Number           | Scenario                  |
|-----------------------|---------------------------|
| `4242 4242 4242 4242` | Payment succeeds          |
| `4000 0000 0000 0002` | Card declined             |
| `4000 0025 0000 3155` | 3D Secure authentication  |

For all test cards, use:
- Any **future** expiry date (e.g. `12/26`)
- Any 3-digit CVC (e.g. `123`)
- Any ZIP code (e.g. `10001`)

---

## Project Structure

```
payment-portfolio/
├── pages/
│   ├── _app.js          # Wraps all pages, imports global CSS
│   ├── index.js         # Product listing page (main storefront)
│   ├── success.js       # Shown after successful payment
│   ├── cancel.js        # Shown when user cancels checkout
│   └── api/
│       └── checkout.js  # API route: creates Stripe Checkout Session
├── styles/
│   └── globals.css      # All styles
├── .env.local.example   # Template for environment variables
├── .gitignore
├── next.config.js
└── package.json
```

---

## Key Files Explained

### `pages/api/checkout.js`

This is the only server-side route. It receives a product object from the client, uses the Stripe secret key to create a Checkout Session, and returns the session URL. The secret key is never exposed to the browser.

```js
const session = await stripe.checkout.sessions.create({
  line_items: [{ price_data: { ... }, quantity: 1 }],
  mode: 'payment',
  success_url: `${BASE_URL}/success?session_id={CHECKOUT_SESSION_ID}`,
  cancel_url: `${BASE_URL}/cancel`,
})
```

### `pages/success.js`

Uses `getServerSideProps` to retrieve the Checkout Session from Stripe server-side (using the `session_id` query param), then displays the payment amount and customer email.

### `pages/index.js`

The storefront. Each "Buy Now" button calls `/api/checkout` with the product details, then redirects the browser to Stripe's hosted payment page using the returned URL.

---

## Deployment (Vercel)

1. Push this repo to GitHub
2. Go to [vercel.com](https://vercel.com) → **Add New Project** → import your repo
3. In the Vercel dashboard, add these **Environment Variables**:
   - `STRIPE_SECRET_KEY` → your `sk_test_...` key
   - `NEXT_PUBLIC_BASE_URL` → your Vercel URL (e.g. `https://your-project.vercel.app`)
4. Click **Deploy**

To accept real payments, replace the test keys with live keys (`sk_live_...`) and update `NEXT_PUBLIC_BASE_URL` to your live domain.

---

## Security Notes

- The Stripe **secret key** is only used in `pages/api/checkout.js` (server-side). It is never sent to the browser.
- Input validation is applied in the API route before creating any session.
- `.env.local` is excluded from git via `.gitignore`.
- This app uses Stripe's **hosted checkout page** — no card data ever touches your server, making it PCI compliant by default.

---

## License

MIT
