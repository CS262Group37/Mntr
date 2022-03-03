import React from "react";
import { BiMenu, BiMenuAltRight, BiUserCircle } from "react-icons/bi";
import { Link } from "react-router-dom";
import Avatar from "@mui/material/Avatar";
import UserMenu from "./UserMenu";

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
  // TODO get mentors from database
  const [menu, setMenu] = React.useState(false);
  const [settings, setSettings] = React.useState(true);

  const mentors: string[] = ["Mentor 1", "Mentor 2", "Mentor 3", "Mentor 4"];

  // Renders the dropdown menu button in the page title
  const renderButton = (menu: boolean) => {
    const css = "m-auto mr-8 text-4xl cursor-pointer";

    if (menu) {
      return <BiMenuAltRight className={css} onClick={() => setMenu(!menu)} />;
    }

    return <BiMenu className={css} onClick={() => setMenu(!menu)} />;
  };

  return (
    <div>
      <UserMenu visible={settings} />

      <div className="text-cultured font-display select-none overflow-visible h-auto">
        {/* Blue main navbar */}
        <div className="bg-blueBgWide h-20 bg-cover flex flex-row text-2xl">
          {/* Website name - dashboard link */}
          <Link
            to="/dashboard-mentee"
            className="text-5xl m-auto ml-8 font-bold"
          >
            Mntr
          </Link>

          {/* Navigation */}
          <div className="flex flex-row h-[100%]">
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
            <div
              className="m-auto rounded-full cursor-pointer"
              onClick={() => setSettings(!settings)}
            >
              <Avatar
                className="m-auto mr-6 ml-4"
                alt={props.firstName + " " + props.lastName}
                src={props.avatar}
                sx={{ width: 50, height: 50 }}
              />
            </div>
          </div>
        </div>

        {/* Red navbar - page title */}
        <div className="bg-firebrick flex flex-row text-2xl text-left">
          <h2 className="m-auto ml-8 text-left font-bold mt-3 mb-3">
            {props.activeStr}
          </h2>

          {props.activeStr === "My mentors" && renderButton(menu)}
        </div>

        {/* Dropdown menu */}
        <div
          className={
            "bg-firebrick flex flex-col text-2xl text-left  animate-growDown origin-top " +
            (menu ? "visible" : "hidden")
          }
        >
          {/* // TODO animate + implement functionality */}
          {props.activeStr === "My mentors" &&
            mentors.map((mentor) => {
              return (
                <Link
                  to="/dashboard-mentee"
                  className="p-auto ml-8 mt-3 mb-3 hover:font-bold"
                >
                  {mentor}
                </Link>
              );
            })}
        </div>
      </div>
    </div>
  );
};

export default NavBar;
