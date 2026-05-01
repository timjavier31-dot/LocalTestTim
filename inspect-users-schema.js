const sql = require('mssql');

const config = {
  server: 'localhost',
  port: 54791,
  options: {
    trustServerCertificate: true,
    enableArithAbort: true,
    encrypt: false,
  },
  authentication: {
    type: 'ntlm',
    options: {
      domain: 'DESKTOP-5IK0H2G',
      userName: 'Lirj',
      password: 'sonydell',
    },
  },
  pool: {
    max: 1,
    min: 0,
    idleTimeoutMillis: 30000,
  },
  connectionTimeout: 30000,
  database: 'TestApp',
};

(async () => {
  try {
    const pool = await new sql.ConnectionPool(config).connect();
    const result = await pool.request().query("SELECT c.name, t.name AS type_name FROM sys.columns c JOIN sys.types t ON c.user_type_id = t.user_type_id WHERE object_id = OBJECT_ID('dbo.Users') ORDER BY c.column_id");
    console.log(result.recordset);
    await pool.close();
  } catch (error) {
    console.error(error);
    process.exit(1);
  }
})();
