import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
    let disposable = vscode.commands.registerCommand('mcp.requestSuggestions', async () => {
        vscode.window.showInformationMessage('Hello from MCP Code Suggester!');
        // your actual implementation here...
    });

    context.subscriptions.push(disposable);
}

export function deactivate() {}
