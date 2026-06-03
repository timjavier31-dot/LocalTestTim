import { useState } from 'react'
import Head from 'next/head'

const products = [
  {
    id: 1,
    name: 'Web Design Template',
    description: 'A premium, fully responsive website template with modern layout components and clean typography.',
    price: 29,
    initials: 'WDT',
    badgeClass: 'badge-purple',
  },
  {
    id: 2,
    name: 'UI Component Pack',
    description: 'Over 50 reusable React components — buttons, modals, forms, cards — ready to drop into any project.',
    price: 49,
    initials: 'UCP',
    badgeClass: 'badge-teal',
  },
  {
    id: 3,
    name: 'Full Stack Course',
    description: 'Complete Next.js and Node.js course covering authentication, databases, APIs, and deployment.',
    price: 99,
    initials: 'FSC',
    badgeClass: 'badge-orange',
  },
]

export default function Home() {
  const [loading, setLoading] = useState(null)
  const [error, setError] = useState(null)

  const handleCheckout = async (product) => {
    setLoading(product.id)
    setError(null)

    try {
      const res = await fetch('/api/checkout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product }),
      })

      const data = await res.json()

      if (!res.ok) throw new Error(data.error || 'Checkout failed')

      window.location.href = data.url
    } catch (err) {
      setError(err.message)
      setLoading(null)
    }
  }

  return (
    <>
      <Head>
        <title>DevStore — Portfolio Project</title>
        <meta name="description" content="Sample e-commerce site demonstrating Stripe Checkout with Next.js" />
      </Head>

      <header className="site-header">
        <div className="container">
          <h1>DevStore</h1>
          <p>Next.js + Stripe Checkout — Portfolio Demo</p>
        </div>
      </header>

      <main>
        <div className="container">
          <div className="test-banner">
            Test mode active — use card <code>4242 4242 4242 4242</code> with any future date and any CVC
          </div>

          {error && (
            <div style={{ background: '#fee2e2', color: '#991b1b', padding: '12px 20px', borderRadius: '8px', marginBottom: '24px' }}>
              Error: {error}
            </div>
          )}

          <div className="product-grid">
            {products.map((product) => (
              <div key={product.id} className="product-card">
                <div className={`product-badge ${product.badgeClass}`}>{product.initials}</div>
                <h2>{product.name}</h2>
                <p>{product.description}</p>
                <div className="card-footer">
                  <span className="price">${product.price}</span>
                  <button
                    className="btn-buy"
                    onClick={() => handleCheckout(product)}
                    disabled={loading === product.id}
                  >
                    {loading === product.id ? 'Redirecting...' : 'Buy Now'}
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </main>

      <footer className="site-footer">
        <p>Built with Next.js &amp; Stripe &mdash; Portfolio project by <a href="https://github.com/timjavier31-dot" target="_blank" rel="noreferrer">timjavier31</a></p>
      </footer>
    </>
  )
}
