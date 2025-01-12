import { useState } from "react";
import { Mic } from "lucide-react";
import AuthImagePattern from "../components/AuthImagePattern";
import {toast} from "react-hot-toast"
const HomePage = () => {
  const [formData, setFormData] = useState({
    salespersonName: "",
    salespersonRole: "",
    companyName: "",
    companyBusiness: "",
    companyValues: "",
    conversationPurpose: "",
    conversationType: "",
  });

  const [errors, setErrors] = useState({});
  const [isSubmitted, setIsSubmitted] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    const newErrors = {};
    Object.entries(formData).forEach(([key, value]) => {
      if (!value.trim()) {
        newErrors[key] = "This field is required.";
      }
    });

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
    } else {
      setErrors({});
      console.log("Form submitted:", formData);
      toast.success("Form submitted successfully!");
      setIsSubmitted(true); // Mark the form as submitted
    }
  };

  return (
    <div className="h-screen grid lg:grid-cols-2 ">
      {/* Left Side - Form or Icon */}
      <div className="flex flex-col justify-center items-center p-6 sm:p-12">
        <div className="w-full max-w-md space-y-8">
          <div className="flex justify-center">
            <p className="text-2xl font-semibold">VoiceBuddy</p>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-6">
            {[
              { label: "Salesperson Name", name: "salespersonName", type: "text", placeholder: "Enter salesperson name" },
              { label: "Salesperson Role", name: "salespersonRole", type: "text", placeholder: "Enter salesperson role" },
              { label: "Company Name", name: "companyName", type: "text", placeholder: "Enter company name" },
              { label: "Company Business", name: "companyBusiness", type: "text", placeholder: "Enter company business" },
              { label: "Company Values", name: "companyValues", type: "text", placeholder: "Enter company values" },
              { label: "Conversation Purpose", name: "conversationPurpose", type: "text", placeholder: "Enter purpose of conversation" },
              { label: "Conversation Type", name: "conversationType", type: "text", placeholder: "Enter type of conversation" },
            ].map(({ label, name, type, placeholder }) => (
              <div key={name} className="form-control">
                <label className="label">
                  <span className="label-text font-medium">{label}</span>
                </label>
                <input
                  type={type}
                  name={name}
                  value={formData[name]}
                  onChange={handleChange}
                  placeholder={placeholder}
                  className={`input input-bordered w-full ${errors[name] ? "input-error" : ""}`}
                />
                {errors[name] && <p className="text-red-500 text-sm mt-1">{errors[name]}</p>}
              </div>
            ))}

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
