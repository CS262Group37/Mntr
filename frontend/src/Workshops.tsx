import React, { useEffect } from "react";
import "./App.css";
import axios from "axios";
import { Link } from "react-router-dom";
import NavBar from "./components/NavBarMentee";
import PlanOfAction from "./components/PlanOfAction";

interface UserData {
  id?: number;
  firstName: string;
  lastName: string;
  avatar: string;
  role: string;
  businessArea: string;
  topics?: string[];
  ratings?: Rating[];
}

interface Rating {
  skill: string;
  rating: number;
}

function Workshops() {
  const [user, setUser] = React.useState<UserData>({firstName: "", lastName: "", avatar: "", role: "", businessArea: "", topics: []});
  const [workshops, setWorkshops] = React.useState([]);

  // Get user data
  useEffect(() => {
    axios.get("/api/users/get-own-data").then((res) => {
      const newUser: UserData = {
        id: res.data.userid,
        firstName: res.data.firstname,
        lastName: res.data.lastname,
        avatar: res.data.profilepicture,
        role: res.data.role,
        businessArea: res.data.businessarea,
      }
      console.log(newUser);
      setUser(newUser);
    });
  }, []);

  useEffect(() => {
    axios.get("/api/workshop/get-workshops", {params: { userID: user.id, role: user.role } }).then((res) => {
      console.log(res.data);
    });    
  }, []);

  return(
    <div className="fixed h-full w-full">
      <NavBar
        activeStr="Workshops"
      />

      {/* Main flexbox */}
      <div className="flex flex-row items-stretch h-full font-display">
        {/* White half */}
        <div className="bg-cultured h-full w-2/3 m-auto flex text-prussianBlue fixed left-0 overflow-auto">
          {/* Main center flexbox */}
          <div className="w-3/5 m-auto flex flex-col text-prussianBlue justify-center space-y-10">
            <h2 className="text-4xl pt-[10%]">
              Welcome to{" "}
              <span className="font-bold text-firebrick">Mntr</span>
            </h2>
            <p className="text-2xl">
              Here's where you can learn a new skill or share your knowledge
            </p>

            {/* Registration link */}
            <p className="text-2xl m-auto pt-[10%]">
              Don't have an account yet?{" "}
              <span className="font-bold underline text-imperialRed">
                <Link to="/register">Register now!</Link>
              </span>
            </p>
          </div>
        </div>

        {/* <PlanOfAction /> */}
      </div>
    </div>
  );
}

export default Workshops;