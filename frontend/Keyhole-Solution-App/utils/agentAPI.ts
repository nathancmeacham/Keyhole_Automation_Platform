// Keyhole_Automation_Platform\frontend\Keyhole-Solution-App\utils\agentAPI.ts

const sendMessageToAgent = async (userMessage: string) => {
  try {
    const response = await fetch('http://127.0.0.1:8000/mcp/agent', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ user_message: userMessage }),
    });

    const data = await response.json();
    console.log("📦 Agent API response:", data);

    return data.response ?? "⚠️ No response from agent.";
  } catch (error) {
    console.error('Error sending message to agent:', error);
    return "⚠️ Something went wrong!";
  }
};

export default sendMessageToAgent;
