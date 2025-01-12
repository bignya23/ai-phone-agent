import { useState } from "react";
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
    if (!salespersonName.trim()) newErrors.salespersonName = "This field is required.";
    if (!salespersonRole.trim()) newErrors.salespersonRole = "This field is required.";
    if (!companyName.trim()) newErrors.companyName = "This field is required.";
    if (!companyBusiness.trim()) newErrors.companyBusiness = "This field is required.";
    if (!companyValues.trim()) newErrors.companyValues = "This field is required.";
    if (!conversationPurpose.trim()) newErrors.conversationPurpose = "This field is required.";
    if (!conversationType.trim()) newErrors.conversationType = "This field is required.";
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
        const response = await axios.post("http://127.0.0.1:5000/agent", formData, {
          headers: {
            "Content-Type": "application/json",
          },
        });

        console.log("Response from server:", response.data);
        toast.success("Form submitted successfully!");
        setIsSubmitted(true);
      } catch (error) {
        console.error("Error submitting form:", error);
        toast.error("Failed to submit the form. Please try again.");
      }
    }
  };

  return (
    <div className="h-screen grid lg:grid-cols-2">
      {/* Left Side - Form */}
      <div className="flex flex-col justify-center items-center p-6 sm:p-12">
        <div className="w-full max-w-md space-y-8">
          <div className="flex justify-center">
            <p className="text-2xl font-semibold">VoiceBuddy</p>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="form-control">
              <label className="label">
                <span className="label-text font-medium">Salesperson Name</span>
              </label>
              <input
                type="text"
                value={salespersonName}
                onChange={(e) => setSalespersonName(e.target.value)}
                placeholder="Enter salesperson name"
                className={`input input-bordered w-full ${errors.salespersonName ? "input-error" : ""}`}
              />
              {errors.salespersonName && <p className="text-red-500 text-sm mt-1">{errors.salespersonName}</p>}
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
                className={`input input-bordered w-full ${errors.salespersonRole ? "input-error" : ""}`}
              />
              {errors.salespersonRole && <p className="text-red-500 text-sm mt-1">{errors.salespersonRole}</p>}
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
                className={`input input-bordered w-full ${errors.companyName ? "input-error" : ""}`}
              />
              {errors.companyName && <p className="text-red-500 text-sm mt-1">{errors.companyName}</p>}
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
                className={`input input-bordered w-full ${errors.companyBusiness ? "input-error" : ""}`}
              />
              {errors.companyBusiness && <p className="text-red-500 text-sm mt-1">{errors.companyBusiness}</p>}
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
                className={`input input-bordered w-full ${errors.companyValues ? "input-error" : ""}`}
              />
              {errors.companyValues && <p className="text-red-500 text-sm mt-1">{errors.companyValues}</p>}
            </div>

            <div className="form-control">
              <label className="label">
                <span className="label-text font-medium">Conversation Purpose</span>
              </label>
              <input
                type="text"
                value={conversationPurpose}
                onChange={(e) => setConversationPurpose(e.target.value)}
                placeholder="Enter purpose of conversation"
                className={`input input-bordered w-full ${errors.conversationPurpose ? "input-error" : ""}`}
              />
              {errors.conversationPurpose && <p className="text-red-500 text-sm mt-1">{errors.conversationPurpose}</p>}
            </div>

            <div className="form-control">
              <label className="label">
                <span className="label-text font-medium">Conversation Type</span>
              </label>
              <input
                type="text"
                value={conversationType}
                onChange={(e) => setConversationType(e.target.value)}
                placeholder="Enter type of conversation"
                className={`input input-bordered w-full ${errors.conversationType ? "input-error" : ""}`}
              />
              {errors.conversationType && <p className="text-red-500 text-sm mt-1">{errors.conversationType}</p>}
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
          <Mic className="w-16 h-16 text-primary" />
          <p className="text-xl font-semibold mt-4">Tap to Speak</p>
        </div>
      )}
    </div>
  );
};

export default HomePage;
