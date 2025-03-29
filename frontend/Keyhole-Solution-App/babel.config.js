// Keyhole_Automation_Platform/frontend/Keyhole-Solution-App/babel.config.js

module.exports = function (api) {
    api.cache(true);
    return {
      presets: ['babel-preset-expo'],
      plugins: [
        [
          'module:react-native-dotenv',
          {
            moduleName: '@env',
            path: '../../.env', // ✅ Centralized .env at project root
            blocklist: null,
            allowlist: null,
            safe: false,
            allowUndefined: true
          }
        ]
      ]
    };
  };
  