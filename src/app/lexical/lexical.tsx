import axios from 'axios';

interface Token {
  lexeme: string;
  token: string;
}

// In-memory cache to store responses
const cache = new Map<string, { tokens: Token[]; errors: string[] }>();

export const handleTokenizerClick = async (
  textareaRef: React.RefObject<HTMLTextAreaElement>,
  setOutputData: React.Dispatch<React.SetStateAction<Token[]>>,
  setTerminalOutput: React.Dispatch<React.SetStateAction<string>>
) => {
  const textarea = textareaRef.current;
  if (textarea) {
    const text = textarea.value;
    const cacheKey = text;

    // Check if the response is already in the cache
    if (cache.has(cacheKey)) {
      const cachedResponse = cache.get(cacheKey);
      if (cachedResponse) {
        const { tokens, errors } = cachedResponse;
        const newOutputData = tokens.map((token) => ({
          lexeme: token.lexeme,
          token: token.token,
        }));
        setOutputData(newOutputData);
        if (errors && errors.length > 0) {
          setTerminalOutput(errors.join('\n'));
        } else {
          setTerminalOutput('');
        }
        return;
      }
    }

    console.log('Sending request to /run with text:', text);
    try {
      const url = window.location.hostname === 'localhost' ? 'http://127.0.0.1:5000/api/lexer' : '/api/lexer';
      const response = await axios.post(url, { text });
      const { tokens, errors } = response.data;
      const newOutputData = tokens.map((token: { type: string; value: string }) => {
        let lexeme = token.value;
        if (token.type === 'float_literal' && parseFloat(token.value) % 1 === 0) { 
          lexeme = `${token.value}.0`;
        }
        return {
          lexeme,
          token: token.type,
        };
      });
      if (errors) {
        setTerminalOutput(errors.join('\n'));
        setOutputData(newOutputData);
        // Store the error response in cache
        cache.set(cacheKey, { tokens: newOutputData, errors });
      } else {
        setOutputData(newOutputData);
        setTerminalOutput('');
        // Store the successful response in cache
        cache.set(cacheKey, { tokens: newOutputData, errors: [] });
      }
    } catch (error) {
      if (axios.isAxiosError(error) && error.response) {
        console.error('Error:', error.response.data.errors);
        setTerminalOutput(error.response.data.errors.join('\n'));
        // Store the error response in cache
        cache.set(cacheKey, { tokens: [], errors: error.response.data.errors });
      } else {
        console.error('Error:', error);
        setTerminalOutput('An unexpected error occurred.');
      }
    }
  }
};