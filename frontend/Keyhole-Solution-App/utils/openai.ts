// Keyhole_Automation_Platform\frontend\Keyhole-Solution-App\utils\openai.ts

import axios from 'axios';
import { OPENAI_API_KEY } from '@env';

export const askGPT = async (userMessage: string): Promise<string> => {
  try {
    const res = await axios.post(
      'https://api.openai.com/v1/chat/completions',
      {
        model: 'gpt-4o',
        messages: [
          { role: 'system', content: 'You are a helpful assistant.' },
          { role: 'user', content: userMessage },
        ],
        temperature: 0.7,
      },
      {
        headers: {
          Authorization: `Bearer ${OPENAI_API_KEY}`,
          'Content-Type': 'application/json',
        },
      }
    );

    const reply = res.data.choices[0].message.content;
    return reply.trim();
  } catch (err) {
    console.error('GPT error:', err);
    return 'Sorry, something went wrong.';
  }
};
