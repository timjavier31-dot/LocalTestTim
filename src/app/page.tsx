'use client';

import { FormEvent, useState } from 'react';
import { useRouter } from 'next/navigation';

const roles = [
  { value: '1', label: 'Admin' },
  { value: '2', label: 'Manager' },
  { value: '3', label: 'Employee' },
  { value: '4', label: 'Guest' },
];

export default function Home() {
  const router = useRouter();
  const [userName, setUserName] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [roleId, setRoleId] = useState('4');
  const [mode, setMode] = useState<'login' | 'create'>('login');
  const [status, setStatus] = useState('Ready to log in');
  const [result, setResult] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setResult(null);
    setStatus(mode === 'create' ? 'Creating account...' : 'Checking credentials...');

    try {
      const response = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action: mode,
          userName,
          password,
          email,
          roleId,
        }),
      });
      const data = await response.json();

      setStatus(data.message || (data.success ? (mode === 'create' ? 'Account created.' : 'Login successful.') : 'Operation failed.'));
      setResult(JSON.stringify(data, null, 2));

      if (data.success && mode === 'login') {
        router.push('/finder');
        return;
      }

      if (data.success && mode === 'create') {
        setMode('login');
        setUserName('');
        setPassword('');
        setEmail('');
        setRoleId('4');
      }
    } catch (error) {
      setStatus(mode === 'create' ? 'Account creation failed.' : 'Login failed.');
      setResult(error instanceof Error ? error.message : String(error));
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen flex items-center justify-center bg-slate-100 px-6 py-12">
      <div className="w-full max-w-3xl rounded-3xl border border-slate-200 bg-white p-10 shadow-xl shadow-slate-200/50">
        <div className="space-y-4">
          <h1 className="text-4xl font-semibold text-slate-900">{mode === 'create' ? 'Create Account' : 'Login'}</h1>
          <p className="text-slate-600">
            {mode === 'create'
              ? 'Enter the details for the new user account.'
              : 'Enter your username and password to sign in.'}
          </p>
        </div>

        <div className="mt-8 flex flex-wrap items-center gap-4">
          <button
            type="button"
            onClick={() => setMode('login')}
            className={`rounded-2xl px-5 py-3 text-sm font-semibold transition ${
              mode === 'login' ? 'bg-sky-600 text-white' : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
            }`}
          >
            Log In
          </button>
          <button
            type="button"
            onClick={() => setMode('create')}
            className={`rounded-2xl px-5 py-3 text-sm font-semibold transition ${
              mode === 'create' ? 'bg-sky-600 text-white' : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
            }`}
          >
            Create Account
          </button>
        </div>

        <form onSubmit={handleSubmit} className="mt-8 grid gap-6">
          <div>
            <label className="mb-2 block text-sm font-medium text-slate-700">Username</label>
            <input
              value={userName}
              onChange={(event) => setUserName(event.target.value)}
              className="w-full rounded-2xl border border-slate-300 bg-slate-50 px-4 py-3 text-slate-900 focus:border-sky-500 focus:outline-none focus:ring-2 focus:ring-sky-200"
            />
          </div>

          <div>
            <label className="mb-2 block text-sm font-medium text-slate-700">Password</label>
            <input
              value={password}
              type="password"
              onChange={(event) => setPassword(event.target.value)}
              placeholder="Enter your password"
              className="w-full rounded-2xl border border-slate-300 bg-slate-50 px-4 py-3 text-slate-900 focus:border-sky-500 focus:outline-none focus:ring-2 focus:ring-sky-200"
            />
          </div>

          {mode === 'create' ? (
            <>
              <div>
                <label className="mb-2 block text-sm font-medium text-slate-700">Email</label>
                <input
                  value={email}
                  type="email"
                  onChange={(event) => setEmail(event.target.value)}
                  placeholder="Enter the user email"
                  className="w-full rounded-2xl border border-slate-300 bg-slate-50 px-4 py-3 text-slate-900 focus:border-sky-500 focus:outline-none focus:ring-2 focus:ring-sky-200"
                />
              </div>

              <div>
                <label className="mb-2 block text-sm font-medium text-slate-700">Role</label>
                <select
                  value={roleId}
                  onChange={(event) => setRoleId(event.target.value)}
                  className="w-full rounded-2xl border border-slate-300 bg-slate-50 px-4 py-3 text-slate-900 focus:border-sky-500 focus:outline-none focus:ring-2 focus:ring-sky-200"
                >
                  {roles.map((role) => (
                    <option key={role.value} value={role.value}>
                      {role.label}
                    </option>
                  ))}
                </select>
              </div>
            </>
          ) : null}

          <button
            type="submit"
            disabled={loading}
            className="inline-flex items-center justify-center rounded-2xl bg-sky-600 px-6 py-3 text-sm font-semibold text-white transition hover:bg-sky-700 disabled:cursor-not-allowed disabled:bg-slate-400"
          >
            {loading
              ? mode === 'create'
                ? 'Creating...'
                : 'Logging in...'
              : mode === 'create'
              ? 'Create Account'
              : 'Log In'}
          </button>
        </form>

        <div className="mt-8 rounded-3xl border border-slate-200 bg-slate-50 p-6">
          <p className="text-sm font-semibold uppercase tracking-[0.24em] text-slate-500">Status</p>
          <p className="mt-2 text-slate-800">{status}</p>
          {result ? (
            <pre className="mt-4 overflow-x-auto rounded-2xl bg-slate-900 p-4 text-sm text-emerald-200">{result}</pre>
          ) : null}
        </div>
      </div>
    </main>
  );
}
