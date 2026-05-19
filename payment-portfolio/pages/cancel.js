import Head from 'next/head'
import Link from 'next/link'

export default function Cancel() {
  return (
    <>
      <Head>
        <title>Payment Cancelled — DevStore</title>
      </Head>

      <div className="result-page">
        <div className="result-card">
          <div className="result-icon icon-cancel">&#x2715;</div>
          <h1>Payment Cancelled</h1>
          <p>Your payment was not completed.</p>
          <p>No charge was made to your card.</p>
          <Link href="/" className="back-link">
            Back to Store
          </Link>
        </div>
      </div>
    </>
  )
}
