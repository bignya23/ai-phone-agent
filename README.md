# AI Phone Agent  

### Note:
The Sales Agent Application is hosted on https://ai-phone-agent-1.onrender.com, with its backend service running at https://ai-phone-agent.onrender.com.

Important Considerations:
Free Instance Latency:
Since the backend is hosted on a free instance, it may spin down due to inactivity. As a result, the first request after inactivity might experience a delay of 50 seconds or more while the instance restarts. Subsequent requests should process faster.

Recommended Browsers:
For optimal performance and compatibility, we recommend using the application on Google Chrome or Microsoft Edge.

Using Tools:
Enabling tools during the conversation may increase latency, as it requires additional processing time to fetch and integrate tool responses.

AI Phone Agent is an innovative application designed to handle cold calls for businesses, hold meaningful conversations, and close sales. Powered by advanced speech-to-text (STT), large language models (LLMs), and text-to-speech (TTS) technology, the agent provides a seamless and natural experience for users.  

## Features  
1. **Cold Call Handling**:  
   - Initiates calls with a greeting and waits for the user's response.  
   - Converts speech to text using the Groq STT model.  

2. **Dynamic Response Generation**:  
   - Leverages the Groq Llama 3.3 70B versatile model for response generation.  
   - Supports tool-based actions for enhanced functionality:  
     - **Knowledge Base**: Retrieve product price, specifications, or availability.  
       - **Arguments**: `[product_name: str]`  (can be used with vector stores)
     - **Schedule Call**: Schedule a call 
       - **Arguments**: `[date: str, time: str]`  
     - **Payment UPI**: Generate a UPI payment request.  
       - **Arguments**: `[amount: float]`  
     - **Payment Link**: Generate a payment link.  
       - **Arguments**: `[amount: float]`  

3. **Text-to-Speech Conversion**:  
   - Converts the generated response back to speech for the user using a TTS engine.  

4. **Full Call Workflow**:  
   - Mimics a real-world call agent, providing a complete conversational experience from greeting to closing.  

---

## Installation  

### Prerequisites  
- Ensure you have Python 3.8+ installed.  
- Install Node.js (for the frontend).  
- Install the required dependencies:  
  ```bash
  pip install -r requirements.txt
  ```  

---

### Backend Setup  
1. Navigate to the project root directory.  
2. Run the backend using:  
   ```bash
   python app_web.py
   ```
3. Optional(app.py is for twilio phone calling)
   ```bash
   python app.py
   ```  

---

### Frontend Setup  
1. Navigate to the `frontend` folder:  
   ```bash
   cd frontend
   ```  
2. Install dependencies:  
   ```bash
   npm install
   ```  
3. Start the development server:  
   ```bash
   npm run dev
   ```  

---


### `.env` File Format  

Create a `.env` file in the project root and add the following environment variables:  

```env
# API key for Groq STT model and LLM Model
GROQ_API_KEY_2=your_api_key_here

# API key for TTS engine
WAVES_API_KEY_1=tts_api_key_here

GEMINI_API_KEY="optional"

```  

Replace `your_api_key_here` with your actual API keys

## Usage  
1. Start the backend and frontend as described above.  
2. The agent initiates the call with a greeting.  
3. User responses are processed through speech-to-text conversion.  
4. The agent generates responses using the LLM and executes supported tools when needed.  
5. Responses are converted back to speech and provided to the user.  

---

## Future Scope  
- **Enhanced Tools**: Add more functionalities to cover a broader range of use cases.  
- **Improved Models**: Upgrade the models for better conversational capabilities.  
- **Custom Integrations**: Expand integrations with other services and tools.  

---

## Usage (Web Interface)  

1. **Fill Out the Form**:  
   - Start by filling out the form on the web interface with the necessary details (e.g., name, contact information, product preferences, etc.).  

2. **Start Speaking**:  
   - Once the form is submitted, the system will prompt you to start recording your response.  
   - Speak clearly into the microphone to ensure accurate transcription.  

3. **Stop Recording**:  
   - After completing your response, click the **arrow button** to stop the recording process.  

4. **Agent Processing**:  
   - The AI Phone Agent will process your input, generate a response using the integrated LLM, and execute any necessary actions or tools.  

5. **Receive Response**:  
   - The system will provide the AI-generated response through text and audio, mimicking a real call experience.  

---

For a seamless experience, ensure that your microphone permissions are enabled in your browser. 
## Contributing  
We welcome contributions! Feel free to fork this repository, submit pull requests, or report issues.  

---

## License  
This project is licensed under the [MIT License](LICENSE).  

---

## Contact  
For questions or collaboration, reach out to [Bignya](https://github.com/bignya23).  

--- 

Feel free to update this as needed!
