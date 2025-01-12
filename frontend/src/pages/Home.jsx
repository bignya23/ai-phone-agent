import { useState, useRef, useEffect } from "react";
import axios from "axios";
import { Mic } from "lucide-react";
import AuthImagePattern from "../components/AuthImagePattern";
import { toast } from "react-hot-toast";

const HomePage = () => {
  const [salespersonName, setSalespersonName] = useState("");
  const [salespersonRole, setSalespersonRole] = useState("");
  const [companyName, setCompanyName] = useState("");
  const [companyBusiness, setCompanyBusiness] = useState("");
  const [companyValues, setCompanyValues] = useState("");
  const [conversationPurpose, setConversationPurpose] = useState("");
  const [conversationType, setConversationType] = useState("");

  const [errors, setErrors] = useState({});
  const [isSubmitted, setIsSubmitted] = useState(false);

  const validateForm = () => {
    const newErrors = {};
    if (!salespersonName.trim())
      newErrors.salespersonName = "This field is required.";
    if (!salespersonRole.trim())
      newErrors.salespersonRole = "This field is required.";
    if (!companyName.trim()) newErrors.companyName = "This field is required.";
    if (!companyBusiness.trim())
      newErrors.companyBusiness = "This field is required.";
    if (!companyValues.trim())
      newErrors.companyValues = "This field is required.";
    if (!conversationPurpose.trim())
      newErrors.conversationPurpose = "This field is required.";
    if (!conversationType.trim())
      newErrors.conversationType = "This field is required.";
    return newErrors;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const newErrors = validateForm();

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
    } else {
      setErrors({});
      const formData = {
        salespersonName,
        salespersonRole,
        companyName,
        companyBusiness,
        companyValues,
        conversationPurpose,
        conversationType,
      };

      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/get_info",
          formData,
          {
            withCredentials: true,
          }
        );

        console.log("Response from server:", response.data);
        toast.success("Form submitted successfully!");
        setIsSubmitted(true);
      } catch (error) {
        console.error("Error submitting form:", error);
        toast.error("Failed to submit the form. Please try again.");
      }
    }
  };

  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [audioContext, setAudioContext] = useState(null);
  const mediaRecorder = useRef(null);
  const audioChunks = useRef([]);
  const silenceTimeout = useRef(null);
  const audioQueue = useRef([]);
  const isPlayingAudio = useRef(false);

  // Silence detection parameters
  const SILENCE_THRESHOLD = -50; // dB
  const SILENCE_DURATION = 2000; // 2 seconds of silence to stop recording

  const initAudioContext = async () => {
    const context = new (window.AudioContext || window.webkitAudioContext)();
    setAudioContext(context);
    return context;
  };

  const detectSilence = (analyser, dataArray) => {
    analyser.getFloatTimeDomainData(dataArray);
    let maxVolume = -Infinity;
    
    for (let i = 0; i < dataArray.length; i++) {
      maxVolume = Math.max(maxVolume, Math.abs(dataArray[i]));
    }
    
    const db = 20 * Math.log10(maxVolume);
    
    if (db < SILENCE_THRESHOLD) {
      if (!silenceTimeout.current) {
        silenceTimeout.current = setTimeout(() => {
          if (mediaRecorder.current && mediaRecorder.current.state === "recording") {
            stopRecording();
          }
        }, SILENCE_DURATION);
      }
    } else {
      if (silenceTimeout.current) {
        clearTimeout(silenceTimeout.current);
        silenceTimeout.current = null;
      }
    }
  };

  const playNextInQueue = async () => {
    if (audioQueue.current.length === 0 || isPlayingAudio.current) {
      return;
    }

    isPlayingAudio.current = true;
    const audioUrl = audioQueue.current.shift();

    try {
      const audio = new Audio(`http://127.0.0.1:5000${audioUrl}`);
      
      audio.onended = () => {
        isPlayingAudio.current = false;
        if (audioQueue.current.length > 0) {
          playNextInQueue();
        } else {
          startRecording(); // Start recording again after playing all responses
        }
      };

      await audio.play();
    } catch (error) {
      console.error("Error playing audio:", error);
      isPlayingAudio.current = false;
      startRecording(); // Start recording even if audio playback fails
    }
  };

  const startRecording = async () => {
    if (isRecording || isProcessing) return;

    try {
      const context = audioContext || await initAudioContext();
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      
      // Set up audio analysis
      const source = context.createMediaStreamSource(stream);
      const analyser = context.createAnalyser();
      analyser.fftSize = 2048;
      source.connect(analyser);
      
      const dataArray = new Float32Array(analyser.fftSize);
      
      // Create and configure MediaRecorder
      mediaRecorder.current = new MediaRecorder(stream);
      audioChunks.current = [];

      mediaRecorder.current.ondataavailable = (event) => {
        audioChunks.current.push(event.data);
      };

      mediaRecorder.current.onstop = async () => {
        setIsProcessing(true);
        const audioBlob = new Blob(audioChunks.current, { type: "audio/wav" });
        await handleAudioUpload(audioBlob);
        setIsProcessing(false);
      };

      // Start recording and silence detection
      mediaRecorder.current.start();
      setIsRecording(true);
      toast.success("Recording started");

      // Continuous silence detection
      const checkSilence = () => {
        if (mediaRecorder.current && mediaRecorder.current.state === "recording") {
          detectSilence(analyser, dataArray);
          requestAnimationFrame(checkSilence);
        }
      };
      checkSilence();

    } catch (error) {
      console.error("Error starting recording:", error);
      toast.error("Failed to start recording");
      setIsRecording(false);
    }
  };

  const stopRecording = () => {
    if (!mediaRecorder.current || mediaRecorder.current.state !== "recording") return;

    mediaRecorder.current.stop();
    mediaRecorder.current.stream.getTracks().forEach(track => track.stop());
    setIsRecording(false);
    
    if (silenceTimeout.current) {
      clearTimeout(silenceTimeout.current);
      silenceTimeout.current = null;
    }
    
    toast.success("Recording stopped");
  };

  const handleAudioUpload = async (audioBlob) => {
    const formData = new FormData();
    formData.append("audio", audioBlob);

    try {
      // Upload audio and get transcription
      await axios.post("http://127.0.0.1:5000/upload-audio", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      // Get agent response
      const response = await axios.post("http://127.0.0.1:5000/agent");
      
      if (response.data.audioUrl) {
        audioQueue.current.push(response.data.audioUrl);
        playNextInQueue();
      }

      if (response.data.isEndOfCall) {
        toast.success("Conversation ended");
        setIsSubmitted(false); // Reset form
      }
    } catch (error) {
      console.error("Error in conversation:", error);
      toast.error("Error processing audio");
      startRecording(); // Restart recording even if there's an error
    }
  };

  const handleMicClick = () => {
    if (!isRecording && !isProcessing) {
      startRecording();
    } else if (isRecording) {
      stopRecording();
    }
  };

  // Clean up on component unmount
  useEffect(() => {
    return () => {
      if (mediaRecorder.current) {
        stopRecording();
      }
      if (audioContext) {
        audioContext.close();
      }
    };
  }, []);

  

  return (
    <div className="h-screen grid lg:grid-cols-2">
      {/* Left Side - Form */}
      <div className="flex flex-col justify-center items-center p-6 sm:p-12">
        <div className="w-full max-w-md space-y-8">
          <div className="flex justify-center">
            <p className="text-2xl font-semibold">VoiceBuddy</p>
          </div>

          {/* Form */}
          <form
            onSubmit={handleSubmit}
            className="space-y-6"
            style={{
              pointerEvents: isSubmitted ? "none" : "auto",
              opacity: isSubmitted ? 0.5 : 1,
            }}
          >
            <div className="form-control">
              <label className="label">
                <span className="label-text font-medium">Salesperson Name</span>
              </label>
              <input
                type="text"
                value={salespersonName}
                onChange={(e) => setSalespersonName(e.target.value)}
                placeholder="Enter salesperson name"
                className={`input input-bordered w-full ${
                  errors.salespersonName ? "input-error" : ""
                }`}
              />
              {errors.salespersonName && (
                <p className="text-red-500 text-sm mt-1">
                  {errors.salespersonName}
                </p>
              )}
            </div>

            <div className="form-control">
              <label className="label">
                <span className="label-text font-medium">Salesperson Role</span>
              </label>
              <input
                type="text"
                value={salespersonRole}
                onChange={(e) => setSalespersonRole(e.target.value)}
                placeholder="Enter salesperson role"
                className={`input input-bordered w-full ${
                  errors.salespersonRole ? "input-error" : ""
                }`}
              />
              {errors.salespersonRole && (
                <p className="text-red-500 text-sm mt-1">
                  {errors.salespersonRole}
                </p>
              )}
            </div>

            <div className="form-control">
              <label className="label">
                <span className="label-text font-medium">Company Name</span>
              </label>
              <input
                type="text"
                value={companyName}
                onChange={(e) => setCompanyName(e.target.value)}
                placeholder="Enter company name"
                className={`input input-bordered w-full ${
                  errors.companyName ? "input-error" : ""
                }`}
              />
              {errors.companyName && (
                <p className="text-red-500 text-sm mt-1">
                  {errors.companyName}
                </p>
              )}
            </div>

            <div className="form-control">
              <label className="label">
                <span className="label-text font-medium">Company Business</span>
              </label>
              <input
                type="text"
                value={companyBusiness}
                onChange={(e) => setCompanyBusiness(e.target.value)}
                placeholder="Enter company business"
                className={`input input-bordered w-full ${
                  errors.companyBusiness ? "input-error" : ""
                }`}
              />
              {errors.companyBusiness && (
                <p className="text-red-500 text-sm mt-1">
                  {errors.companyBusiness}
                </p>
              )}
            </div>

            <div className="form-control">
              <label className="label">
                <span className="label-text font-medium">Company Values</span>
              </label>
              <input
                type="text"
                value={companyValues}
                onChange={(e) => setCompanyValues(e.target.value)}
                placeholder="Enter company values"
                className={`input input-bordered w-full ${
                  errors.companyValues ? "input-error" : ""
                }`}
              />
              {errors.companyValues && (
                <p className="text-red-500 text-sm mt-1">
                  {errors.companyValues}
                </p>
              )}
            </div>

            <div className="form-control">
              <label className="label">
                <span className="label-text font-medium">
                  Conversation Purpose
                </span>
              </label>
              <input
                type="text"
                value={conversationPurpose}
                onChange={(e) => setConversationPurpose(e.target.value)}
                placeholder="Enter purpose of conversation"
                className={`input input-bordered w-full ${
                  errors.conversationPurpose ? "input-error" : ""
                }`}
              />
              {errors.conversationPurpose && (
                <p className="text-red-500 text-sm mt-1">
                  {errors.conversationPurpose}
                </p>
              )}
            </div>

            <div className="form-control">
              <label className="label">
                <span className="label-text font-medium">
                  Conversation Type
                </span>
              </label>
              <input
                type="text"
                value={conversationType}
                onChange={(e) => setConversationType(e.target.value)}
                placeholder="Enter type of conversation"
                className={`input input-bordered w-full ${
                  errors.conversationType ? "input-error" : ""
                }`}
              />
              {errors.conversationType && (
                <p className="text-red-500 text-sm mt-1">
                  {errors.conversationType}
                </p>
              )}
            </div>

            <button type="submit" className="btn btn-primary w-full">
              Submit
            </button>
          </form>
        </div>
      </div>

      {/* Right Side - Image/Pattern */}
      {!isSubmitted ? (
        <AuthImagePattern
          title={"Welcome to the Form"}
          subtitle={"Submit the details on the left panel to proceed."}
        />
      ) : (
        <div className="flex flex-col justify-center items-center">
          <button 
            onClick={handleMicClick} 
            className="focus:outline-none"
            disabled={isProcessing}
          >
            <Mic
              className={`w-16 h-16 ${
                isRecording ? "text-red-500" : 
                isProcessing ? "text-gray-400" : "text-primary"
              }`}
            />
          </button>
          <p className="text-xl font-semibold mt-4">
            {isRecording ? "Recording..." : 
             isProcessing ? "Processing..." : "Tap to Speak"}
          </p>
        </div>
      )}
    </div>
  );
};

export default HomePage;
