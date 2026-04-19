import { NextResponse } from 'next/server';
import sql from 'mssql';

const DB_CONNECTION_DOMAIN = 'DESKTOP-5IK0H2G';
const DB_CONNECTION_USERNAME = 'Lirj';
const DB_CONNECTION_PASSWORD = 'sonydell';

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
};

const TEST_DATABASE = 'TestApp';
const USERS_TABLE = '[Users]';
const validRoleIds = [1, 2, 3, 4];

export async function POST(request: Request) {
  const body = await request.json();
  const action = body.action === 'create' ? 'create' : 'login';
  const userName = (body.userName || '').trim();
  const password = body.password || '';
  const email = (body.email || '').trim();
  const roleId = Number(body.roleId || 0);

  if (!userName || !password) {
    return NextResponse.json(
      {
        success: false,
        message: 'Username and password are required.',
      },
      { status: 400 },
    );
  }

  if (action === 'create') {
    if (!email) {
      return NextResponse.json(
        {
          success: false,
          message: 'Email is required to create an account.',
        },
        { status: 400 },
      );
    }

    if (!validRoleIds.includes(roleId)) {
      return NextResponse.json(
        {
          success: false,
          message: 'A valid roleId is required (1=admin, 2=manager, 3=employee, 4=guest).',
        },
        { status: 400 },
      );
    }
  }

  const config = {
    ...configBase,
    authentication: {
      type: 'ntlm' as const,
      options: {
        domain: DB_CONNECTION_DOMAIN,
        userName: DB_CONNECTION_USERNAME,
        password: DB_CONNECTION_PASSWORD,
      },
    },
  };

  try {
    const masterPool = await new sql.ConnectionPool({
      ...config,
      database: 'master',
    }).connect();

    const dbResult = await masterPool
      .request()
      .input('dbName', sql.NVarChar(128), TEST_DATABASE)
      .query(`SELECT CASE WHEN DB_ID(@dbName) IS NOT NULL THEN 1 ELSE 0 END AS dbExists`);

    await masterPool.close();

    if (!dbResult.recordset?.[0]?.dbExists) {
      return NextResponse.json({
        success: false,
        message: `Database ${TEST_DATABASE} does not exist.`,
      });
    }

    const appPool = await new sql.ConnectionPool({
      ...config,
      database: TEST_DATABASE,
    }).connect();

    const tableResult = await appPool
      .request()
      .input('tableName', sql.NVarChar(128), 'Users')
      .query(`SELECT CASE WHEN OBJECT_ID(@tableName, 'U') IS NOT NULL THEN 1 ELSE 0 END AS tableExists`);

    if (!tableResult.recordset?.[0]?.tableExists) {
      await appPool.close();
      return NextResponse.json({
        success: false,
        message: 'Table Users does not exist in TestApp.',
      });
    }

    if (action === 'create') {
      const duplicateQuery = await appPool
        .request()
        .input('username', sql.NVarChar(256), userName)
        .input('email', sql.NVarChar(256), email)
        .query(`
          SELECT TOP (1) UserID
          FROM ${USERS_TABLE}
          WHERE Username = @username OR Email = @email
        `);

      if (duplicateQuery.recordset?.[0]) {
        await appPool.close();
        return NextResponse.json({
          success: false,
          message: 'A user with that username or email already exists.',
        });
      }

      const insertResult = await appPool
        .request()
        .input('username', sql.NVarChar(256), userName)
        .input('email', sql.NVarChar(256), email)
        .input('password', sql.NVarChar(256), password)
        .input('roleId', sql.Int, roleId)
        .query(`
          INSERT INTO ${USERS_TABLE} (Username, Email, PasswordRaw, RoleId, IsActive, CreatedAt)
          OUTPUT INSERTED.UserID AS NewUserId
          VALUES (@username, @email, @password, @roleId, 1, GETDATE())
        `);

      const createdUserId = insertResult.recordset?.[0]?.NewUserId ?? null;

      await appPool.close();

      return NextResponse.json({
        success: true,
        message: 'Account created successfully.',
        database: TEST_DATABASE,
        user: { id: createdUserId, username: userName },
      });
    }

    const userQuery = await appPool
      .request()
      .input('username', sql.NVarChar(256), userName)
      .query(`
        SELECT TOP (1) UserID, Username, PasswordRaw
        FROM ${USERS_TABLE}
        WHERE Username = @username
      `);

    const userRecord = userQuery.recordset?.[0];
    let success = false;
    let message = '';

    if (!userRecord) {
      message = 'User does not exist in TestApp.Users.';
    } else if (userRecord.PasswordRaw !== password) {
      message = 'Incorrect password for existing user.';
    } else {
      success = true;
      message = 'Login successful.';
    }

    await appPool.close();

    return NextResponse.json({
      success,
      message,
      database: TEST_DATABASE,
      user: userRecord ? { id: userRecord.UserID, username: userRecord.Username } : null,
    });
  } catch (error) {
    return NextResponse.json(
      {
        success: false,
        message: 'Connection failed.',
        error: error instanceof Error ? error.message : String(error),
      },
      { status: 500 },
    );
  }
}
