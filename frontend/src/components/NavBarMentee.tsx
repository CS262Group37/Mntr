import React, { useEffect } from "react";
import axios from "axios";
import { BiMenu, BiMenuAltRight, BiUserCircle } from "react-icons/bi";
import { Link } from "react-router-dom";
import { Avatar, Popover } from "@mui/material";
import UserMenu from "./UserMenu";

interface UserData {
  id?: number;
  firstName: string;
  lastName: string;
  avatar: string;
  role: string;
  businessArea: string;
  topics?: string[];
}

interface NavBarProps {
  // firstName: string;
  // lastName: string;
  // avatar: string;
  activeStr: string;
  activeMentorId?: number;
  mentors?: UserData[];
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

const NavBarMentee: React.FC<NavBarProps> = (props) => {
  // TODO get mentors from database
  const [user, setUser] = React.useState<UserData>({firstName: "", lastName: "", avatar: "", role: "", businessArea: "", topics: []});
  const [menu, setMenu] = React.useState<boolean>(false);
  const [userMenu, setUserMenu] = React.useState<HTMLDivElement | null>(null);

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
      setUser(newUser);
    });
  }, []);

  const userMenuClick = (event: React.MouseEvent<HTMLDivElement>) => {
    setUserMenu(event.currentTarget);
  };

  const userMenuClose = () => {
    setUserMenu(null);
  };

  const userMenuOpen = Boolean(userMenu);
  const userMenuID = userMenuOpen ? "simple-popover" : undefined;

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
      {/* <UserMenu visible={userMenu} /> */}

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
              path="/workshops-mentee"
              activeStr={props.activeStr}
            />
            {/* Profile picture - display user menu on click */}
            <div
              className="m-auto mr-6 ml-4 rounded-full box-content cursor-pointer hover:border-imperialRed hover:border-2 hover:ml-[14px] hover:mr-[22px]"
              onClick={userMenuClick}
            >
              <Avatar
                className="m-auto"
                alt={user.firstName + " " + user.lastName}
                src={user.avatar}
                sx={{ width: 50, height: 50 }}
              />
            </div>
            <Popover
              id={userMenuID}
              open={userMenuOpen}
              anchorEl={userMenu}
              onClose={userMenuClose}
              anchorOrigin={{
                vertical: "bottom",
                horizontal: "right",
              }}
              transformOrigin={{
                vertical: "top",
                horizontal: "right",
              }}
            >
              <UserMenu user={user} />
            </Popover>
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

          {props.activeStr === "My mentors" &&
            props.mentors?.map((mentor) => {
              let css: string;
              if (mentor.id === props.activeMentorId) {
                css = "p-auto ml-8 mt-3 mb-3 font-bold"
              } else {
                css = "p-auto ml-8 mt-3 mb-3 hover:font-bold"
              }

              return (
                <Link
                  to={"/dashboard-mentee?mentor=" + mentor.id}
                  className={css}
                >
                  {mentor.firstName + " " + mentor.lastName}
                </Link>
              );
            })}
        </div>
      </div>
    </div>
  );
};

export default NavBarMentee;