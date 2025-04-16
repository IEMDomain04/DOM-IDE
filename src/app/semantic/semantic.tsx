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
        const { semantic_result, errors /*, tree_str*/, error_pos } = response.data;
        if (errors) {
          setTerminalOutput(errors);
          if (error_pos) {
            console.log('Error position:', error_pos); 
            /* TO EMMAN: Nasa loob ng error_pos object yung position supposedly ng squiggly lines
            TAKE NOTE: error_pos here in semantic may be a list/array of error positions, so you might need to iterate over it
            You can check the console log to see the structure of error_pos
            Example Use:
            error_pos.idx_start, error_pos.idx_end, // For index start and index end
            error_pos.ln_start, error_pos.ln_end,  // For line start and line end
            error_pos.col_start, error_pos.col_end  // For column start and column end
            */ 
          }
        } else {
          // setTerminalOutput(semantic_result + '\n\nAbstract Syntax Tree (For Debugging):\n' + tree_str);
          setTerminalOutput(semantic_result);
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