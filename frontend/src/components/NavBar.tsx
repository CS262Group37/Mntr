import React from "react";
import { BiMenu, BiUserCircle } from "react-icons/bi";
import { Link } from "react-router-dom";

interface LinkProps {
  text: string;
  path: string;
  activeStr: string;
}

const NavBarLink: React.FC<LinkProps> = (props) => {
  console.log(props.text);
  console.log(props.activeStr);
  console.log(props.text === props.activeStr);

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

function NavBar(props: any) {
  const { activeStr } = props;

  return (
    <div className="text-cultured font-display flex flex-col">
      {/* Blue main navbar */}
      <div className="bg-blueBgWide h-20 bg-cover flex flex-row text-2xl">
        {/* Website name */}
        <h1 className="text-5xl m-auto ml-8 font-bold">Mntr</h1>

        {/* Navigation */}
        <div className="flex flex-row mr-8 h-[100%]">
          <NavBarLink
            text="My mentors"
            path="/dashboard-mentee"
            activeStr={activeStr}
          />
          <NavBarLink
            text="Browse mentors"
            path="/browse-mentors"
            activeStr={activeStr}
          />
          <NavBarLink
            text="Workshops"
            path="/workshops"
            activeStr={activeStr}
          />
          <BiUserCircle className="m-auto ml-8 text-4xl" />
        </div>
      </div>

      {/* Red navbar with dropdown menu */}
      {/* TODO dropdown menu */}
      <div className="bg-firebrick h-14 flex flex-row text-2xl">
        <h2 className="m-auto ml-8 text-left font-semibold">{activeStr}</h2>
        <BiMenu className="m-auto mr-8 text-4xl" />
      </div>
    </div>
  );
}

export default NavBar;
