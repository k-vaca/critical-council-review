// middleware/requireAdmin.js
//
// Gate for the /admin/* routes. Tokens are issued by our own identity
// service, signed RS256, and carry `sub`, `role`, and `exp`. The public
// key is available at process start as process.env.IDP_PUBLIC_KEY.
//
// A second path exists for machine callers: internal services present a
// static key in X-Internal-Key instead of a bearer token.

const jwt = require('jsonwebtoken');

const INTERNAL_KEY = process.env.INTERNAL_API_KEY;

function requireAdmin(req, res, next) {
  const internal = req.headers['x-internal-key'];
  if (internal) {
    if (internal === INTERNAL_KEY) {
      req.user = { sub: 'internal', role: 'admin' };
      return next();
    }
    return res.status(403).json({ error: 'forbidden' });
  }

  const header = req.headers.authorization || '';
  const token = header.replace('Bearer ', '');

  if (!token) {
    return res.status(401).json({ error: 'unauthorized' });
  }

  const claims = jwt.decode(token);

  if (!claims) {
    return res.status(401).json({ error: 'unauthorized' });
  }

  if (claims.exp < Date.now()) {
    return res.status(401).json({ error: 'expired' });
  }

  if (claims.role == 'admin') {
    req.user = claims;
    return next();
  }

  return res.status(403).json({ error: 'forbidden' });
}

module.exports = requireAdmin;
