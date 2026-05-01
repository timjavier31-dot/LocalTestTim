const sql = require('mssql');

const config = {
  server: 'localhost',
  options: {
    instanceName: 'SQLEXPRESS',
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
  database: 'master',
};

(async () => {
  try {
    console.log('Connecting with config:', config.server, config.options.instanceName);
    const pool = await sql.connect(config);
    const result = await pool.request().query('SELECT 1 AS value');
    console.log('Connected, result:', result.recordset);
    await pool.close();
  } catch (error) {
    console.error('Connection error:', error);
    process.exit(1);
  }
})();
