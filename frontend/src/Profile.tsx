import React, { useEffect } from "react";
import axios from "axios";
import { BiMenu, BiMenuAltRight, BiUserCircle } from "react-icons/bi";
import { Link, useLocation } from "react-router-dom";
import { Avatar, Popover } from "@mui/material";

interface UserData {
  id?: number;
  email: string;
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

function useQuery() {
  const { search } = useLocation();

  return React.useMemo(() => new URLSearchParams(search), [search]);
}

function Profile() {
  const [user, setUser] = React.useState<UserData>();
  
  let query = useQuery();
  const userIdQuery = query.get("id");
  let userID: number = -1;

  if (userIdQuery != null)
    userID = parseInt(userIdQuery);

  useEffect(() => {
    var newUser: UserData = {email: "", firstName: "", lastName: "", avatar: "", role: "", businessArea: ""}
    var newTopics: string[] = [];
    var newRatings: Rating[] = [];

    axios.post("/api/users/get-user-data", { userID: userID }).then((res) => {
      newUser = {
        email: res.data.email,
        firstName: res.data.firstname,
        lastName: res.data.lastname,
        avatar: res.data.profilepicture,
        role: res.data.role,
        businessArea: res.data.businessarea,
      }
    });

    // Get 
    axios.post("/api/users/get-user-topics", { userID: userID }).then((res) => {
      const arr: string[] = [];
      res.data.map((t: any) => {
        arr.push(t.topic);
      });

      newTopics = arr;
    });

    // Get ratings
    if (newUser.role === "mentor") {
      axios.post("/api/users/get-user-ratings", { userID: userID }).then((res) => {
        // Sort alphabetically by skill
        res.data.sort((e1: any, e2: any) => {
          return e2.skill < e1.skill;
        })

        newRatings = res.data;
      });
    }

    setUser({
      id: userID,
      email: newUser.email,
      firstName: newUser.firstName,
      lastName: newUser.lastName,
      avatar: newUser.avatar,
      role: newUser.role,
      businessArea: newUser.businessArea,
      topics: newTopics,
      ratings: newRatings,
    })
  }, []);

  return (
    <div>
      <div className="text-cultured font-display select-none overflow-visible h-auto">
        <div className="bg-blueBgWide h-20 bg-cover flex flex-row text-2xl">
          
        </div>
      </div>
    </div>
  );
};

export default Profile;
