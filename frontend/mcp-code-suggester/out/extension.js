"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.activate = activate;
exports.deactivate = deactivate;
const vscode = require("vscode");
function activate(context) {
    let disposable = vscode.commands.registerCommand('mcp.requestSuggestions', async () => {
        vscode.window.showInformationMessage('Hello from MCP Code Suggester!');
        // your actual implementation here...
    });
    context.subscriptions.push(disposable);
}
function deactivate() { }
//# sourceMappingURL=extension.js.map