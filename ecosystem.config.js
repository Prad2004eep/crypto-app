module.exports = {
  apps: [{
    name: 'crypto-app',
    script: './index.js', // or your main entry file
    instances: 'max',
    exec_mode: 'cluster',
    autorestart: true,
    watch: false,
    max_memory_restart: '500M',
    env: {
      NODE_ENV: 'production'
    }
  }]
};
