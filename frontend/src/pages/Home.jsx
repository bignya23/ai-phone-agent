import { useState, useRef, useEffect } from "react";
import axios from "axios";
import { Mic, Send } from "lucide-react";
import AuthImagePattern from "../components/AuthImagePattern";
import { toast } from "react-hot-toast";

const HomePage = () => {
  // Form states
  const [salespersonName, setSalespersonName] = useState("");
  const [salespersonRole, setSalespersonRole] = useState("");
  const [companyName, setCompanyName] = useState("");
  const [companyBusiness, setCompanyBusiness] = useState("");
  const [companyValues, setCompanyValues] = useState("");
  const [conversationPurpose, setConversationPurpose] = useState("");
  const [conversationType, setConversationType] = useState("");
  const [withTools, setWithTools] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [isCallEnded,setIsCallEnded] = useState(false);
  const [errors, setErrors] = useState({});

  // Audio states
  const [audioUrl, setAudioUrl] = useState(null);
  const [isRecording, setIsRecording] = useState(false);
  const [isMicActive, setIsMicActive] = useState(false);

  // Refs for audio handling
  const mediaRecorderRef = useRef(null);
  const streamRef = useRef(null);
  const audioChunksRef = useRef([]);

  const validateForm = () => {
    const newErrors = {};
    if (!salespersonName.trim()) newErrors.salespersonName = "Required";
    if (!salespersonRole.trim()) newErrors.salespersonRole = "Required";
    if (!companyName.trim()) newErrors.companyName = "Required";
    if (!companyBusiness.trim()) newErrors.companyBusiness = "Required";
    if (!companyValues.trim()) newErrors.companyValues = "Required";
    if (!conversationPurpose.trim()) newErrors.conversationPurpose = "Required";
    if (!conversationType.trim()) newErrors.conversationType = "Required";
    return newErrors;
  };
const handleSubmit = async (e) => {
  e.preventDefault();
  const newErrors = validateForm();
  if (Object.keys(newErrors).length > 0) {
    setErrors(newErrors);
    return;
  }

  try {
    const response = await axios.post(
      "https://ai-phone-agent.onrender.com/get_info",
      {
        salespersonName,
        salespersonRole,
        companyName,
        companyBusiness,
        companyValues,
        conversationPurpose,
        conversationType,
        withTools,
      },
      {
       
        withCredentials: true
      }
    );
    
    setIsSubmitted(true);
    toast.success("Form submitted successfully!");
    handleMicClick();
  } catch (error) {
    console.error('Submission error:', error);
    toast.error("Failed to submit form. Please try again.");
  }
};
  const startRecording = async () => {
    try {
      if (!streamRef.current) {
        const stream = await navigator.mediaDevices.getUserMedia({
          audio: true,
        });
        streamRef.current = stream;
      }

      audioChunksRef.current = [];
      mediaRecorderRef.current = new MediaRecorder(streamRef.current);

      mediaRecorderRef.current.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorderRef.current.start();
      setIsRecording(true);
      setIsMicActive(true);
    } catch (error) {
      console.error("Error starting recording:", error);
      toast.error("Failed to start recording");
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      setIsMicActive(false);
    }
  };

  const handleSendAudio = async () => {
    if (!isRecording) return;

    stopRecording();

    // Wait for the last chunk to be processed
    setTimeout(async () => {
      const audioBlob = new Blob(audioChunksRef.current, { type: "audio/wav" });
      await sendAudioToServer(audioBlob);
    }, 100);
  };

  // const sendAudioToServer = async (audioBlob) => {
  //   const formData = new FormData();
  //   formData.append("audio", audioBlob, "user-audio.wav");

  //   try {
  //     const response = await axios.post(
  //       "https://ai-phone-agent.onrender.com/upload_audio",
  //       formData,
  //       {
  //         headers: { "Content-Type": "multipart/form-data" },
  //       }
  //     );
  //     setAudioUrl(response.data.audioUrl);
  //   } catch (error) {
  //     console.error("Error sending audio:", error);
  //     toast.error("Failed to send audio");
  //   }
  // };

  const sendAudioToServer = async (audioBlob) => {
  const formData = new FormData();
  formData.append("audio", audioBlob, "user-audio.wav");

  try {
    const response = await axios.post(
      "https://ai-phone-agent.onrender.com/upload_audio",
      formData,
      {
        headers: { "Content-Type": "multipart/form-data" },
        withCredentials: true, // Include credentials like cookies
      }
    );
    if(response.data.isEndOfCall){
      setIsCallEnded(true);
    }
    setAudioUrl(response.data.audioUrl);
  } catch (error) {
    console.error("Error sending audio:", error);
    toast.error("Failed to send audio");
  }
};


  const handleMicClick = async () => {
    try {
      setIsMicActive(true);
      const response = await axios.get("https://ai-phone-agent.onrender.com/agent");
      setAudioUrl(response.data.audioUrl);
    } catch (error) {
      console.error("Error fetching initial audio:", error);
      toast.error("Failed to start conversation");
      setIsMicActive(false);
    }
  };

  useEffect(() => {
    if (audioUrl) {
      const audio = new Audio(audioUrl);

      audio.onended = () => {
        startRecording();
      };

      audio.play().catch((error) => {
        console.error("Error playing audio:", error);
        toast.error("Failed to play audio");
      });
    }
  }, [audioUrl]);

  // Cleanup effect
  useEffect(() => {
    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((track) => track.stop());
      }
    };
  }, []);

  return (
    <div className="h-screen grid lg:grid-cols-2">
      {/* Left Side - Form */}
      <div className="flex flex-col justify-center items-center p-6 sm:p-12">
        <div className="w-full max-w-md space-y-8">
          <div className="flex justify-center">
            <p className="text-2xl font-semibold">CallMate</p>
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
            {/* Salesperson Name */}
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

            {/* Salesperson Role */}
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

            {/* Company Name */}
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

            {/* Company Business */}
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

            {/* Company Values */}
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

            {/* Conversation Purpose */}
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

            {/* Conversation Type */}
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

            <div className="form-control">
              <label className="label cursor-pointer">
                <span className="label-text font-medium">With Tools</span>
                <input
                  type="checkbox"
                  checked={withTools}
                  onChange={(e) => setWithTools(e.target.checked)} // Toggle between true/false
                  className="checkbox checkbox-primary ml-2"
                />
              </label>
            </div>

            {/* Submit Button */}
            <button type="submit" className="btn btn-primary w-full">
              Submit
            </button>
          </form>
        </div>
      </div>

      
      {/* Right Side - Conversation Interface */}
      <div className="h-screen flex flex-col items-center justify-center">
        {!isSubmitted ? (
          <AuthImagePattern
            title="Welcome to CallMate"
            subtitle="Submit the form to start your conversation"
          />
        ) : isCallEnded ? (
          <div className="text-center">
            <h2 className="text-3xl font-bold text-primary mb-4">Call Ended</h2>
            <p className="text-gray-600">Thank you for using CallMate!</p>
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center space-y-6">
            <audio autoPlay loop>
              <source src="/bg.wav" type="audio/mpeg" />
              Your browser does not support the audio element.
            </audio>

            <div className="flex gap-4 items-center">
              <Mic
                onClick={startRecording}
                className={`w-16 h-16 cursor-pointer transition-all duration-200 ${
                  isMicActive ? "text-red-500 scale-110" : "text-primary"
                }`}
              />
              {isRecording && (
                <Send
                  onClick={handleSendAudio}
                  className="w-12 h-12 cursor-pointer text-primary hover:scale-110 transition-all duration-200"
                />
              )}
            </div>

            {isRecording && (
              <div className="flex flex-col items-center">
                <div className="text-red-500 text-lg font-semibold animate-pulse">
                  Recording...
                </div>
                <p className="text-gray-500 text-sm mt-2">
                  Click send when you're done speaking
                </p>
              </div>
            )}

            {audioUrl && !isRecording && (
              <div className="flex flex-col items-center">
                <div className="text-blue-500 text-lg font-semibold">
                  Playing response...
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default HomePage;
