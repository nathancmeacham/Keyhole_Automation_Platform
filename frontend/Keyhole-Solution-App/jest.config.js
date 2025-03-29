// Keyhole_Automation_Platform/frontend/Keyhole-Solution-App/jest.config.js

module.exports = {
  preset: 'jest-expo',
  testEnvironment: 'jsdom',

  setupFiles: ['<rootDir>/jest.setup.js'], // ✅ Mock setup
  setupFilesAfterEnv: [
    '<rootDir>/jest.setup.js',
    '<rootDir>/jest-extend-expect.js',
  ], // ✅ Additional matchers and behavior

  transform: {
    '^.+\\.(js|jsx|ts|tsx)$': 'babel-jest',
  },

  transformIgnorePatterns: [
    'node_modules/(?!(jest-)?react-native' +
      '|@react-native' +
      '|@react-navigation' +
      '|expo' +
      '|expo-router' +
      '|expo-status-bar' +
      '|expo-asset' +
      '|expo-constants' +
      '|expo-file-system' +
      '|expo-font' +
      '|expo-crypto' +
      '|expo-modules-core' +
      '|uuid/.*)', // ✅ explicitly allow ESM uuid
  ],

  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json', 'node'],
};
