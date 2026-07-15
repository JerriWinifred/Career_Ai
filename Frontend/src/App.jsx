import { useState } from "react";
import axios from "axios";
import "./App.css";
function App() {
  const [page, setPage] = useState("home");
  const [student, setStudent] = useState({
    name: "",
    email: "",
    course: "",
  });
  const [resume, setResume] = useState(null);
  const [resumeData, setResumeData] = useState(null);
  const [loading, setLoading] = useState(false);
  // Handle Form Input
  const handleChange = (e) => {
    setStudent({
      ...student,
      [e.target.name]: e.target.value,
    });
  };
  // Save Student
  const saveStudent = async () => {

  if (!student.name || !student.email || !student.course) {
    alert("Please fill all the fields.");
    return;
  }

  try {

    const res = await axios.post(
      "https://careerpilot-api-imgyd.onrender.com/students",
      student
    );

    alert(res.data.message);

    setPage("upload");

  } catch (err) {

    console.log(err);

    alert("Unable to save details.");

  }

};
  // Upload Resume
  const uploadResume = async () => {
    if (!resume) {
      alert("Please select a PDF Resume.");
      return;
    }
    setLoading(true);
    const formData = new FormData();
    formData.append("file", resume);
    formData.append("course", student.course);
    try {
      const res = await axios.post(
        "https://careerpilot-api-imgyd.onrender.com/upload-resume",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      setResumeData(res.data);
      setPage("result");
    } catch (err) {
  console.log(err);

  if (err.response) {
    console.log(err.response.data);
    console.log(err.response.status);
  }

  alert("Unable to save details.");
}finally {
      setLoading(false);
    }
  };
  return (
    <div className="app">
      {/* HOME */}
      {page === "home" && (
        <div className="hero">
          <h1>CareerPilot AI </h1>
          <h2>AI Powered Resume Evaluation Platform</h2>
          <p>
            Analyze your resume, discover missing skills,
            explore career opportunities, and get
            personalized learning recommendations.
          </p>
          <button onClick={() => setPage("details")}>
            Get Started
          </button>
        </div>
      )}
      {/* DETAILS */}
      {page === "details" && (
        <div className="hero">
          <h1>Welcome </h1>
          <h2>Enter Your Details</h2>
          <p>
            Fill in your details before uploading your resume.
          </p>
          <input
            type="text"
            name="name"
            placeholder="Full Name"
            value={student.name}
            onChange={handleChange}
          />
          <input
            type="email"
            name="email"
            placeholder="Email Address"
            value={student.email}
            onChange={handleChange}
          />
          <select
            name="course"
            value={student.course}
            onChange={handleChange}
          >
            <option value="">Select Your Course</option>
            <option>AI & DS</option>
            <option>Artificial Intelligence</option>
            <option>Machine Learning</option>
            <option>Data Science</option>
            <option>Computer Science</option>
            <option>Software Engineering</option>
            <option>Information Technology</option>
            <option>Information Systems</option>
            <option>Computer Engineering</option>
            <option>Cyber Security</option>
            <option>Human Computer Interaction</option>
            <option>Networking</option>
          </select>
          <button onClick={saveStudent}>
            Continue
          </button>
        </div>
      )}
      {/* UPLOAD */}
      {page === "upload" && (
        <div className="hero">
          <h1>📄 Resume Analyzer</h1>
          <h2>Hello, {student.name} 👋</h2>
          <p>
            Upload your resume and let CareerPilot AI analyze it.
          </p>
          <p>
            <strong>Course:</strong> {student.course}
          </p>
          <input
            type="file"
            accept=".pdf"
            onChange={(e) => setResume(e.target.files[0])}
          />
          {resume && (
  <p>
    <strong>Selected File:</strong> {resume.name}
  </p>
)}
          <button
            onClick={uploadResume}
            disabled={loading}
          >
            {loading ? "Analyzing Resume..." : "Analyze Resume"}
          </button>
          <button
  onClick={() => setPage("home")}
  className="secondary-btn"
>
  Back
</button>
        </div>
      )}
      {/* RESULT */}
{page === "result" && resumeData && (

<div className="result-page">

  <h1 className="report-title">🎯 AI Resume Report</h1>

  <p className="student-name">
    {student.name}
  </p>

  <p className="student-course">
    Course : <strong>{student.course}</strong>
  </p>

  {/* Resume Score */}

  <div className="report-card">

    <h2>⭐ Resume Score</h2>

    <h1 className="score-number">

{resumeData.resume_score}/100

</h1>

<div className="progress-bar">

<div

className="progress-fill"

style={{

width:`${resumeData.resume_score}%`

}}

></div>

</div>

<p className="resume-level">

{resumeData.resume_level}

</p>

  </div>

  {/* Matched Skills */}

  <div className="report-card">

    <h2>
      ✅ Matched Skills ({resumeData.matched_count})
    </h2>

    <div className="skills-container">

      {resumeData.matched_skills?.map((skill,index)=>(

        <span
          key={index}
          className="skill"
        >
          {skill}
        </span>

      ))}

    </div>

  </div>

  {/* Missing Skills */}

  <div className="report-card">

    <h2>
      ❌ Missing Skills ({resumeData.missing_count})
    </h2>

    <div className="skills-container">

      {resumeData.missing_skills?.map((skill,index)=>(

        <span
          key={index}
          className="missing-skill"
        >
          {skill}
        </span>

      ))}

    </div>

  </div>

  {/* Career Roles */}

  <div className="report-card">

    <h2>💼 Career Roles</h2>

    <ul className="role-list">

      {resumeData.career_roles?.map((role,index)=>(

        <li key={index}>
          {role}
        </li>

      ))}

    </ul>

  </div>

  {/* Learning Path */}

  <div className="report-card">

    <h2>📚 Learning Path</h2>

    <ol className="path-list">

      {resumeData.learning_path?.map((item,index)=>(

        <li key={index}>
          {item}
        </li>

      ))}

    </ol>

  </div>

  {/* AI Suggestion */}

  <div className="report-card">

    <h2>💡 AI Suggestion</h2>

    <p className="suggestion">
      {resumeData.suggestion}
    </p>

  </div>

  {/* Buttons */}

  <div className="button-group">

    <button
      className="secondary-btn"
      onClick={() => setPage("upload")}
    >
      ⬅ Analyze Another Resume
    </button>

    <button
      className="home-btn"
      onClick={() => {

        setResume(null);
        setResumeData(null);

        setStudent({
          name:"",
          email:"",
          course:""
        });

        setPage("home");

      }}
    >
      🏠 Back to Home
    </button>

  </div>

</div>

)}
    </div>
  );
}
export default App;