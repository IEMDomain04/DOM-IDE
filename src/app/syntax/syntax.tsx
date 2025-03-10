import axios from 'axios';

export const handleSyntaxClick = async (
  input_code: string,
  setTerminalOutput: React.Dispatch<React.SetStateAction<string>>
) => {
  const code = input_code;
  if (code) {
    const text = code;
    console.log('Sending request to /api/syntax with text:', text); // Add logging
    try {
        const url = window.location.hostname === 'localhost' ? 'http://127.0.0.1:5000/api/syntax' : '/api/syntax';
        const response = await axios.post(url, { text });
      console.log('Response from /api/syntax:', response.data); // Add logging
      const { result, error } = response.data;
      if (error){
        setTerminalOutput(error);
      } else {
        setTerminalOutput(result);
      }
    } catch (error) {
      if (axios.isAxiosError(error) && error.response) {
        const errorMessage = error.response.data?.error || 'An error occurred';
        console.error('Error:', errorMessage);
        setTerminalOutput(errorMessage); // Set terminal output to error message
      } else {
        console.error('Error:', error);
        setTerminalOutput('An unexpected error occurred.\n' + error); 
      }
    }
  }
};