import axios from "axios";
import { useEffect, useState } from "react";
import NavBarMentee from "./components/NavBarMentee";
import NavBarMentor from "./components/NavBarMentor";

function Settings() {
  const [loggedInRole, setLoggedInRole] = useState<string>("");
  
  useEffect(() => {
    axios.get("/api/users/get-own-data").then((res) => {
      setLoggedInRole(res.data.role);
    });
  }, []);

  return (
    <div className="fixed h-full w-full">
      {loggedInRole === "mentee" && <NavBarMentee activeStr="Settings" />}
      {loggedInRole === "mentor" && <NavBarMentor activeStr="Settings" />}

      {/* Main flexbox */}
      <div className="h-full w-full font-display bg-cultured overflow-auto p-6 flex flex-col pb-40">
        {/* {mentors.map((mentor) => {
          return <MentorCard mentorData={mentor} />;
        })} */}
      </div>
    </div>
  );
}

export default Settings;