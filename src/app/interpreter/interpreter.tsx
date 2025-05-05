import axios from 'axios';

export const handleRunClick = async (
  text: string,
  setTerminalOutput: React.Dispatch<React.SetStateAction<string>>
) => {
  console.log('Sending request to /api/interpreter'); // Add logging
  try {
    const url = window.location.hostname === 'localhost' ? 'http://127.0.0.1:5000/api/interpreter' : '/api/interpreter';
    const response = await axios.post(url, { text });
    console.log('Response from /api/interpreter:', response.data); // Add logging
    const { result, error, error_pos} = response.data;
    if (error) {
      setTerminalOutput(error);
      console.log('Error position:', error_pos); 
          /* TO EMMAN: Nasa loob ng error_pos object yung position supposedly ng squiggly lines
          TAKE NOTE: error_pos here in interpreter is always single object, so you can access it directly (coz lagi lang isa error d2)
          Example Use: 
          error_pos.idx_start, error_pos.idx_end, // For index start and index end
          error_pos.ln_start, error_pos.ln_end,  // For line start and line end
          error_pos.col_start, error_pos.col_end  // For column start and column end
          */ 
    } else {
      // Replace literal \n with actual newline character
      if (window.location.hostname !== 'localhost') {
        const formattedResult = String(result).replace(/\\n/g, '\n').replace(/\\t/g, '\t');
        setTerminalOutput(formattedResult);
      }
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
};