import { NextResponse } from 'next/server';
import sql from 'mssql';

const configBase = {
  server: 'localhost',
  port: 54791,
  options: {
    trustServerCertificate: true,
    enableArithAbort: true,
    encrypt: false,
  },
  pool: {
    max: 1,
    min: 0,
    idleTimeoutMillis: 30000,
  },
  connectionTimeout: 30000,
  user: 'TestAppUser',
  password: 'TestApp@2024!',
};

export async function POST(request: Request) {
  const body = await request.json();
  const query = (body.query || '').trim();

  if (!query) {
    return NextResponse.json({ success: false, message: 'Search query is required.' }, { status: 400 });
  }

  try {
    const pool = await new sql.ConnectionPool({
      ...configBase,
      database: 'TestApp',
    }).connect();

    const result = await pool
      .request()
      .input('query', sql.NVarChar(256), `%${query}%`)
      .query(`
        SELECT Username, Email, IsActive
        FROM [Users]
        WHERE Username LIKE @query OR Email LIKE @query
        ORDER BY Username
      `);

    await pool.close();

    const users = result.recordset.map((row) => ({
      username: row.Username,
      email: row.Email,
      active: row.IsActive === 1 ? 'Y' : 'N',
    }));

    return NextResponse.json({ success: true, users });
  } catch (error) {
    return NextResponse.json(
      {
        success: false,
        message: 'Search failed.',
        error: error instanceof Error ? error.message : String(error),
      },
      { status: 500 },
    );
  }
}
