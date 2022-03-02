import React from "react";
import "./App.css";
import axios from "axios";
import { Link } from "react-router-dom";
import NavBar from "./components/NavBar";
import PlanOfAction from "./components/PlanOfAction";

function BrowseMentors() {
  const dummyAvatarUser =
    "https://images.unsplash.com/photo-1597586124394-fbd6ef244026?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=987&q=80";

  const userData = {
    firstName: "Jane",
    lastName: "Bruh",
    avatar: dummyAvatarUser,
  };
  
  return(
    <div className="fixed h-full w-full">
      <NavBar
        activeStr="Browse mentors"
        firstName={userData.firstName}
        lastName={userData.lastName}
        avatar={userData.avatar}
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

        <PlanOfAction />
      </div>
    </div>
  );
}

export default BrowseMentors;