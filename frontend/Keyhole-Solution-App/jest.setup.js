import 'setimmediate';
import 'whatwg-fetch';
// Your mocks
jest.mock('@react-native-async-storage/async-storage', () =>
  require('@react-native-async-storage/async-storage/jest/async-storage-mock')
);
