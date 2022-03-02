import React from "react";
import { BiMenu, BiUserCircle } from "react-icons/bi";
import { Link } from "react-router-dom";
import Avatar from "@mui/material/Avatar";

interface NavBarProps {
  firstName: string;
  lastName: string;
  avatar: string;
  activeStr: string;
}
interface LinkProps {
  text: string;
  path: string;
  activeStr: string;
}

const NavBarLink: React.FC<LinkProps> = (props) => {
  return (
    <Link
      to={props.path}
      className={
        "m-auto h-[100%] p-5 pt-6 pb-6 hover:bg-firebrick transition ease-in-out duration-300 " +
        (props.text === props.activeStr ? "bg-firebrick" : "bg-none")
      }
    >
      {props.text}
    </Link>
  );
};

const NavBar: React.FC<NavBarProps> = (props) => {
  return (
    <div className="text-cultured font-display">
      {/* Blue main navbar */}
      <div className="bg-blueBgWide h-20 bg-cover flex flex-row text-2xl">
        {/* Website name - dashboard link */}
        <Link to="/dashboard-mentee" className="text-5xl m-auto ml-8 font-bold">
          Mntr
        </Link>

        {/* Navigation */}
        <div className="flex flex-row mr-8 h-[100%]">
          <NavBarLink
            text="My mentors"
            path="/dashboard-mentee"
            activeStr={props.activeStr}
          />
          <NavBarLink
            text="Browse mentors"
            path="/browse-mentors"
            activeStr={props.activeStr}
          />
          <NavBarLink
            text="Workshops"
            path="/workshops"
            activeStr={props.activeStr}
          />
          {/* Profile picture */} 
          <Avatar
            className="m-auto"
            alt={props.firstName + " " + props.lastName}
            src={props.avatar}
            sx={{ width: 50, height: 50 }}
          />
        </div>
      </div>

      {/* Red navbar with dropdown menu */}
      {/* TODO dropdown menu */}
      <div className="bg-firebrick h-14 flex flex-row text-2xl">
        <h2 className="m-auto ml-8 text-left font-semibold">
          {props.activeStr}
        </h2>
        <BiMenu className="m-auto mr-8 text-4xl" />
      </div>
    </div>
  );
};

export default NavBar;
