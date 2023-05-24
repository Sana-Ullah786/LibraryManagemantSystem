import React, { useState, useContext, useEffect } from "react";
import { useHistory } from "react-router-dom";
import { AuthContext, DecodedToken } from "../../contexts/AuthContext";
import { SignupData } from "../../CustomTypes";
import jwt_decode from "jwt-decode";
import { client } from "../../axios";
import "../style.css"; // Import the Genres CSS file

function Signup() {
  const { LoginFunction }: { LoginFunction: (arg0: DecodedToken) => void } =
    useContext(AuthContext);
  const { LogoutFunction }: { LogoutFunction: () => void } =
    useContext(AuthContext);
  const { isAuthenticated }: { isAuthenticated: boolean } =
    useContext(AuthContext);
  const [error, setError] = useState("");
  const history = useHistory();
  const [formData, setFormData] = useState<SignupData>({
    email: "",
    username: "",
    password: "",
    first_name: "",
    last_name: "",
    contact_number: "",
    address: "",
  });

  useEffect(() => {
    if (isAuthenticated) {
      LogoutFunction();
    }
  }, [isAuthenticated, LogoutFunction]);

  function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    // Call the signup function and pass the formData
    client
      .Signup(formData)
      .then((tokens) => {
        history.push("/login");
      })
      .catch((error) => {
        // Handle error and show an error message
        if (
          error.response &&
          error.response.data &&
          error.response.data.detail
        ) {
          const errorMessage = error.response.data.detail[0].msg;
          // Show the error message to the user (e.g., set it to a state variable to display in the UI)
          setError(errorMessage);
        } else {
          alert(error);
        }
      });
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prevFormData) => ({
      ...prevFormData,
      [name]: value,
    }));
  };

  return (
    <div className="background-image">
      <div className="signup-container">
        <form className="signup-form" onSubmit={handleSubmit}>
          <h1>Signup</h1>
          <div className="form-group">
            <label>Email:</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
            />
          </div>
          <div className="form-group">
            <label>Username:</label>
            <input
              type="text"
              name="username"
              value={formData.username}
              onChange={handleChange}
            />
          </div>
          <div className="form-group">
            <label>Password:</label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
            />
          </div>
          <div className="form-group">
            <label>First Name:</label>
            <input
              type="text"
              name="first_name"
              value={formData.first_name}
              onChange={handleChange}
            />
          </div>
          <div className="form-group">
            <label>Last Name:</label>
            <input
              type="text"
              name="last_name"
              value={formData.last_name}
              onChange={handleChange}
            />
          </div>
          <div className="form-group">
            <label>Contact Number:</label>
            <input
              type="text"
              name="contact_number"
              value={formData.contact_number}
              onChange={handleChange}
            />
          </div>
          <div className="form-group">
            <label>Address:</label>
            <input
              type="text"
              name="address"
              value={formData.address}
              onChange={handleChange}
            />
          </div>
          <div className="form-group">
            <button type="submit">Signup</button>
          </div>
        </form>
        <div className="error-message">{error}</div>
      </div>
    </div>
  );
}

export default Signup;
