import "./App.css";
import { Link } from "react-router-dom";

function Register() {
  return (
    <div>
      <h1>Register</h1>
      <Link to="/login">Login instead</Link>
    </div>
  );
}

export default Register;
