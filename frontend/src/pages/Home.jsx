import { useState, useRef, useEffect } from "react";
import axios from "axios";
import { Mic } from "lucide-react";
import AuthImagePattern from "../components/AuthImagePattern";
import { toast } from "react-hot-toast";

const HomePage = () => {
  // Form fields state
  // Form fields state
  const [salespersonName, setSalespersonName] = useState("");
  const [salespersonRole, setSalespersonRole] = useState("");
  const [companyName, setCompanyName] = useState("");
  const [companyBusiness, setCompanyBusiness] = useState("");
  const [companyValues, setCompanyValues] = useState("");
  const [conversationPurpose, setConversationPurpose] = useState("");
  const [conversationType, setConversationType] = useState("");
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [audioUrl, setAudioUrl] = useState(null); // State to store the audio URL
  const [isMicActive, setIsMicActive] = useState(false); 
  // Error state
  const [errors, setErrors] = useState({});

  // State to track audio recording status
  const [isRecording, setIsRecording] = useState(false);
  const [isWaitingForAudio, setIsWaitingForAudio] = useState(false);

  const audioRecorderRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);

  // Validate form fields
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

    // If there are validation errors, set them in the state
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
    } else {
      setErrors({}); // Reset errors if form is valid
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
          { withCredentials: true }
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

  // Handle the mic button click to send GET request to /agent route
  const handleMicClick = async () => {
    try {
      setIsMicActive(true);
      // First, get the audio URL from the server
      const response = await axios.get("http://127.0.0.1:5000/agent");
      console.log("Audio URL from server:", response.data.audioUrl);
      setAudioUrl(response.data.audioUrl); // Store the audio URL in state

      // Play the received audio file
      const audio = new Audio(response.data.audioUrl);
      audio.play();

      // After audio finishes, ask the user to speak
      audio.onended = () => {
        setIsWaitingForAudio(true);
        setIsRecording(true); // Start recording after audio finishes
      };
    } catch (error) {
      console.error("Error fetching audio:", error);
      toast.error("Failed to get audio. Please try again.");
    }
  };

  // Start recording the user's voice
  const startRecording = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorderRef.current = new MediaRecorder(stream);
    mediaRecorderRef.current.ondataavailable = (e) => {
      chunksRef.current.push(e.data);
    };
    mediaRecorderRef.current.onstop = async () => {
      const audioBlob = new Blob(chunksRef.current, { type: "audio/wav" });
      const audioUrl = URL.createObjectURL(audioBlob);
      setAudioUrl(audioUrl); // Display the recorded audio

      // Send the audio to the server
      await sendAudioToServer(audioBlob);
    };
    mediaRecorderRef.current.start();
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };
  const sendAudioToServer = async (audioBlob) => {
    const formData = new FormData();
    formData.append("audio", audioBlob, "user-audio.wav");

    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/upload_audio",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      console.log("Server response:", response.data);
      const { audioUrl } = response.data;
      setAudioUrl(audioUrl);

      // Play the audio response
      const audio = new Audio(audioUrl);
      audio.play();
    } catch (error) {
      console.error("Error sending audio to server:", error);
      toast.error("Failed to send audio. Please try again.");
    }
  };
  useEffect(() => {
    if (isRecording && isWaitingForAudio) {
      // Custom silence detection logic (use a timer to check silence duration)
      const silenceTimeout = setTimeout(() => {
        stopRecording(); // Stop recording after silence detected
      }, 3000); // 3 seconds of silence

      return () => clearTimeout(silenceTimeout); // Clear timeout on component unmount
    }
  }, [isRecording, isWaitingForAudio]);

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

            {/* Submit Button */}
            <button type="submit" className="btn btn-primary w-full">
              Submit
            </button>
          </form>
        </div>
      </div>

      {/* Right Side - Image/Pattern */}
      <div className="h-screen flex flex-col items-center justify-center">
        {!isSubmitted ? (
          <AuthImagePattern
            title={"Welcome to the Form"}
            subtitle={"Submit the details on the left panel to proceed."}
          />
        ) : (
          <div className="flex flex-col justify-center items-center">
            <Mic
              onClick={handleMicClick} // Add the click event handler to the mic icon
              className={`w-16 h-16 text-primary cursor-pointer transition-all duration-200 ${
                isMicActive
                  ? "text-red-500 transform scale-110"
                  : "text-primary"
              }`} // Apply dynamic styles based on mic's active state
            />
            <p className="text-xl font-semibold mt-4">Tap to Speak</p>

            {/* Optionally display the audio player if audioUrl is present */}
            {audioUrl && !isRecording && (
              <audio controls autoPlay>
                <source src={audioUrl} type="audio/mpeg" />
                Your browser does not support the audio element.
              </audio>
            )}

            {/* Show "Speak Now" message when waiting for user input */}
            {isWaitingForAudio && !isRecording && (
              <p className="text-xl font-semibold mt-4">Speak Now</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default HomePage;
