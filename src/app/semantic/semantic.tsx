import axios from 'axios';

export const handleSemanticClick = async (
    code_input: string,
    setTerminalOutput: React.Dispatch<React.SetStateAction<string>>
  ) => {
    const code = code_input;
    if (code) {
      const text = code;
      console.log('Sending request to /api/semantic with text:', text); // Add logging
      try {
          const url = window.location.hostname === 'localhost' ? 'http://127.0.0.1:5000/api/semantic' : '/api/semantic';
          const response = await axios.post(url, { text });
        console.log('Response from /api/semantic:', response.data); // Add logging
        const { semantic_result, errors , tree_str } = response.data;
        if (errors) {
          setTerminalOutput(errors);
        } else {
          //setTerminalOutput(semantic_result + '\n\nAbstract Syntax Tree (For Debugging):\n' + tree_str);
          setTerminalOutput(semantic_result);
          console.log(tree_str);
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