import Head from 'next/head'
import Link from 'next/link'
import Stripe from 'stripe'

export async function getServerSideProps({ query }) {
  if (!query.session_id) {
    return { redirect: { destination: '/', permanent: false } }
  }

  try {
    const stripe = new Stripe(process.env.STRIPE_SECRET_KEY)
    const session = await stripe.checkout.sessions.retrieve(query.session_id)

    return {
      props: {
        amount: session.amount_total,
        currency: session.currency,
        email: session.customer_details?.email || null,
      },
    }
  } catch {
    return { redirect: { destination: '/', permanent: false } }
  }
}

export default function Success({ amount, currency, email }) {
  const formatted = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: currency || 'usd',
  }).format((amount || 0) / 100)

  return (
    <>
      <Head>
        <title>Payment Successful — DevStore</title>
      </Head>

      <div className="result-page">
        <div className="result-card">
          <div className="result-icon icon-success">&#10003;</div>
          <h1>Payment Successful!</h1>
          <p>Thank you for your purchase.</p>
          {email && <p>A receipt has been sent to <strong>{email}</strong></p>}
          <div className="amount-display">{formatted}</div>
          <Link href="/" className="back-link">
            Back to Store
          </Link>
        </div>
      </div>
    </>
  )
}
