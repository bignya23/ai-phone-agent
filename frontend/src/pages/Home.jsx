import { useState } from "react";
import axios from "axios";
import { Mic } from "lucide-react";
import AuthImagePattern from "../components/AuthImagePattern";
import { toast } from "react-hot-toast";

const HomePage = () => {
  const [salesperson_name, setSalespersonName] = useState("");
  const [salesperson_role, setSalespersonRole] = useState("");
  const [company_name, setCompanyName] = useState("");
  const [company_business, setCompanyBusiness] = useState("");
  const [company_values, setCompanyValues] = useState("");
  const [conversation_purpose, setConversationPurpose] = useState("");
  const [conversation_type, setConversationType] = useState("");

  const [errors, setErrors] = useState({});
  const [isSubmitted, setIsSubmitted] = useState(false);

  const validateForm = () => {
    const newErrors = {};
    if (!salesperson_name.trim()) newErrors.salesperson_name = "This field is required.";
    if (!salesperson_role.trim()) newErrors.salesperson_role = "This field is required.";
    if (!company_name.trim()) newErrors.company_name = "This field is required.";
    if (!company_business.trim()) newErrors.company_business = "This field is required.";
    if (!company_values.trim()) newErrors.company_values = "This field is required.";
    if (!conversation_purpose.trim()) newErrors.conversation_purpose = "This field is required.";
    if (!conversation_type.trim()) newErrors.conversation_type = "This field is required.";
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
        salesperson_name,
        salesperson_role,
        company_name,
        company_business,
        company_values,
        conversation_purpose,
        conversation_type,
      };

      try {
        const response = await axios.post("http://127.0.0.1:5000/get_info", formData, {
          withCredentials: true,
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
                value={salesperson_name}
                onChange={(e) => setSalespersonName(e.target.value)}
                placeholder="Enter salesperson name"
                className={`input input-bordered w-full ${errors.salesperson_name ? "input-error" : ""}`}
              />
              {errors.salesperson_name && <p className="text-red-500 text-sm mt-1">{errors.salesperson_name}</p>}
            </div>

            <div className="form-control">
              <label className="label">
                <span className="label-text font-medium">Salesperson Role</span>
              </label>
              <input
                type="text"
                value={salesperson_role}
                onChange={(e) => setSalespersonRole(e.target.value)}
                placeholder="Enter salesperson role"
                className={`input input-bordered w-full ${errors.salesperson_role ? "input-error" : ""}`}
              />
              {errors.salesperson_role && <p className="text-red-500 text-sm mt-1">{errors.salesperson_role}</p>}
            </div>

            <div className="form-control">
              <label className="label">
                <span className="label-text font-medium">Company Name</span>
              </label>
              <input
                type="text"
                value={company_name}
                onChange={(e) => setCompanyName(e.target.value)}
                placeholder="Enter company name"
                className={`input input-bordered w-full ${errors.company_name ? "input-error" : ""}`}
              />
              {errors.company_name && <p className="text-red-500 text-sm mt-1">{errors.company_name}</p>}
            </div>

            <div className="form-control">
              <label className="label">
                <span className="label-text font-medium">Company Business</span>
              </label>
              <input
                type="text"
                value={company_business}
                onChange={(e) => setCompanyBusiness(e.target.value)}
                placeholder="Enter company business"
                className={`input input-bordered w-full ${errors.company_business ? "input-error" : ""}`}
              />
              {errors.company_business && <p className="text-red-500 text-sm mt-1">{errors.company_business}</p>}
            </div>

            <div className="form-control">
              <label className="label">
                <span className="label-text font-medium">Company Values</span>
              </label>
              <input
                type="text"
                value={company_values}
                onChange={(e) => setCompanyValues(e.target.value)}
                placeholder="Enter company values"
                className={`input input-bordered w-full ${errors.company_values ? "input-error" : ""}`}
              />
              {errors.company_values && <p className="text-red-500 text-sm mt-1">{errors.company_values}</p>}
            </div>

            <div className="form-control">
              <label className="label">
                <span className="label-text font-medium">Conversation Purpose</span>
              </label>
              <input
                type="text"
                value={conversation_purpose}
                onChange={(e) => setConversationPurpose(e.target.value)}
                placeholder="Enter purpose of conversation"
                className={`input input-bordered w-full ${errors.conversation_purpose ? "input-error" : ""}`}
              />
              {errors.conversation_purpose && <p className="text-red-500 text-sm mt-1">{errors.conversation_purpose}</p>}
            </div>

            <div className="form-control">
              <label className="label">
                <span className="label-text font-medium">Conversation Type</span>
              </label>
              <input
                type="text"
                value={conversation_type}
                onChange={(e) => setConversationType(e.target.value)}
                placeholder="Enter type of conversation"
                className={`input input-bordered w-full ${errors.conversation_type ? "input-error" : ""}`}
              />
              {errors.conversation_type && <p className="text-red-500 text-sm mt-1">{errors.conversation_type}</p>}
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
