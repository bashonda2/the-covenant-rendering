module.exports = {
  apps: [{
    name: 'tcr-search',
    script: 'server.js',
    env: {
      NODE_ENV: 'production',
      PORT: 3847
    }
  }]
};
