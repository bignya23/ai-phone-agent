import { useState } from "react";
import HomePage from "./pages/Home";
import { Routes, Route } from "react-router-dom";
import { Toaster } from "react-hot-toast";
function App() {
  const [count, setCount] = useState(0);

  return (
    <>
      <div data-theme="synthwave" className="min-h-screen ">
        <Routes>
          <Route path="/" element={<HomePage />} />
        </Routes>
        <Toaster />
      </div>
    </>
  );
}

export default App;
