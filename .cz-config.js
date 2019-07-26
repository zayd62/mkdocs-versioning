module.exports = {
  types: [
    { value: 'feat',     name: 'A new feature'},
    { value: 'fix',      name: 'A bug fix'},
    { value: 'docs',     name: 'Documentation only changes'},
    { value: 'style',    name: 'Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)'},
    { value: 'refactor', name: 'A code change that neither fixes a bug nor adds a feature'},
    { value: 'perf',     name: 'A code change that improves performance'},
    { value: 'test',     name: 'Adding missing tests or correcting existing tests'},
    { value: 'build',    name: 'Changes that affect the build system or external dependencies (example scopes: gulp, broccoli, npm)'},
    { value: 'ci',       name: 'Changes to our CI configuration files and scripts (example scopes: Travis, Circle, BrowserStack, SauceLabs)'},
    { value: 'chore',    name: 'Other changes that don\'t modify src or test files'}
    { value: 'WIP',      name: 'Work in progress' },
    ],

  scopes: [{ name: 'accounts' }, { name: 'admin' }, { name: 'exampleScope' }, { name: 'changeMe' }],
  allowCustomScopes: true,
};
