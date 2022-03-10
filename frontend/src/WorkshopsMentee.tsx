import React, { useEffect } from "react";
import "./App.css";
import axios from "axios";
import { Link } from "react-router-dom";
import NavBarMentee from "./components/NavBarMentee";
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

function WorkshopsMentee() {
  const [user, setUser] = React.useState<UserData>({firstName: "", lastName: "", avatar: "", role: "", businessArea: "", topics: []});
  const [workshops, setWorkshops] = React.useState([]);

  // Get user data
  useEffect(() => {
    axios.get("/api/users/get-own-data").then(async (res) => {
      console.log(res.data);
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
      
      // await axios.get("/api/workshop/get-workshops", {params: { userID: user.id, role: user.role } }).then((res) => {
        //   console.log(res.data);
        //   // setWorkshops(res.data);
        // }); 
        // }).then(() => {
    //   console.log(user);
    //   axios.get("/api/workshop/get-workshops", {params: { userID: user.id, role: user.role } }).then((res) => {
      //     console.log(res.data);
      //   // setWorkshops(res.data);
      //   }); 
    });
    // console.log(user);
  }, []);

  useEffect(() => {
    if (user.id !== -1 && user.role !== "")
      axios.get("/api/workshop/get-workshops", {params: { userID: user.id, role: user.role } }).then((res) => {
        console.log(res.data);
      });    
  }, [user]);

  return(
    <div className="fixed h-full w-full">
      <NavBarMentee activeStr="Workshops" />

      {/* Main flexbox */}
      <div className="h-full w-full font-display bg-cultured overflow-auto p-6 flex flex-col pb-40">
        <h1>{user.firstName + user.lastName}</h1>
        {/* {mentors.map((mentor) => {
          return <MentorCard mentorData={mentor} />;
        })} */}
      </div>
    </div>
  );
}

export default WorkshopsMentee;